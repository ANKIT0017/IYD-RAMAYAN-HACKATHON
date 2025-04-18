import os
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# List of fixed URLs
corrected_urls = [
    "https://valmikiramayan.net/utf8/baala/sarga25/bala_5F25_frame.htm",
    "https://valmikiramayan.net/utf8/baala/sarga40/bala_5F40_frame.htm",
    "https://valmikiramayan.net/utf8/ayodhya/sarga25/ayodhya_5F25_frame.htm",
    "https://valmikiramayan.net/utf8/ayodhya/sarga40/ayodhya_5F40_frame.htm",
    "https://valmikiramayan.net/utf8/aranya/sarga25/aranya_5F25_frame.htm",
    "https://valmikiramayan.net/utf8/aranya/sarga40/aranya_5F40_frame.htm",
    "https://valmikiramayan.net/utf8/sundara/sarga25/sundara_5F25_frame.htm",
    "https://valmikiramayan.net/utf8/sundara/sarga40/sundara_5F40_frame.htm",
    "https://valmikiramayan.net/utf8/yuddha/sarga25/yuddha_5F25_frame.htm",
    "https://valmikiramayan.net/utf8/yuddha/sarga40/yuddha_5F40_frame.htm",
    "https://valmikiramayan.net/utf8/kish/sarga25/kishkindha_5F25_frame.htm",
    "https://valmikiramayan.net/utf8/kish/sarga40/kishkindha_5F40_frame.htm"
]

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def save_html(kanda, sarga, html):
    folder = os.path.join("data", kanda)
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{kanda}_{sarga}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

def get_content_frame_url(driver, frame_url):
    driver.get(frame_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    frame = soup.find('frame', {'name': 'main'})
    return frame['src'] if frame and frame.get('src') else None

def scrape_fixed():
    driver = setup_driver()

    for url in corrected_urls:
        print(f"🔎 Scraping fixed URL: {url}")

        try:
            # Parse kanda and sarga
            parts = urlparse(url).path.strip("/").split("/")
            kanda = parts[1]
            sarga = int(parts[2].replace("sarga", "").strip())

            content_path = get_content_frame_url(driver, url)
            if not content_path:
                print(f"❌ No content found in frame for: {url}")
                continue

            content_url = f"https://valmikiramayan.net/utf8/{kanda}/sarga{sarga}/{content_path}"
            print(f"➡️  Extracting content from: {content_url}")

            driver.get(content_url)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            save_html(kanda, sarga, soup.prettify())
            print(f"💾 Saved HTML for {kanda} - Sarga {sarga}")

        except Exception as e:
            print(f"❗ Failed at {url} -> {e}")

    driver.quit()

if __name__ == "__main__":
    scrape_fixed()
