import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from kanda_chapter_map import kanda_chapter_map

BASE_URL = "https://valmikiramayan.net/utf8"
MISSING_LOG_FILE = "missing_content_urls.txt"

# Map for custom frame file prefixes
kanda_frame_prefix_map = {
    "baala": "bala",
    "kish": "kishkindha"
    # Add more if needed
}

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_soup(driver, url):
    driver.get(url)
    time.sleep(2)
    return BeautifulSoup(driver.page_source, 'html.parser')

def save_html(kanda, sarga, html):
    folder = os.path.join("data", kanda)
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{kanda}_{sarga}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

def log_missing_url(url):
    with open(MISSING_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def get_actual_content_url(driver, frame_url):
    driver.get(frame_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    frame = soup.find('frame', {'name': 'main'})
    if frame and frame.get('src'):
        return frame['src']
    return None

def scrape():
    driver = setup_driver()

    for kanda, total_chapters in kanda_chapter_map.items():
        for sarga in range(1, total_chapters + 1):
            sarga_path = f"sarga{sarga}"

            # Apply prefix mapping if exists, else use kanda name
            frame_prefix = kanda_frame_prefix_map.get(kanda, kanda)
            frame_file = f"{frame_prefix}_{sarga}_frame.htm"
            frame_url = f"{BASE_URL}/{kanda}/{sarga_path}/{frame_file}"
            print(f"🔎 Accessing frame page: {frame_url}")

            try:
                content_path = get_actual_content_url(driver, frame_url)
                if not content_path:
                    print(f"❌ No content frame found: {frame_url}")
                    log_missing_url(frame_url)
                    continue

                content_url = f"{BASE_URL}/{kanda}/{sarga_path}/{content_path}"
                print(f"✅ Scraping content: {content_url}")
                soup = get_soup(driver, content_url)
                save_html(kanda, sarga, soup.prettify())
                print(f"💾 Saved HTML for {kanda} - Sarga {sarga}")
            except Exception as e:
                print(f"❗ Error at {frame_url} -> {e}")
                log_missing_url(frame_url)

    driver.quit()

if __name__ == "__main__":
    scrape()
