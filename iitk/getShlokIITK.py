import streamlit as st
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Mapping for Kanda names
kanda_mapping = {
    1: "Bala Kanda",
    2: "Ayodhya Kanda",
    3: "Aranya Kanda",
    4: "Kishkindha Kanda",
    5: "Sundara Kanda",
    6: "Yuddha Kanda",
    7: "Uttara Kanda"
}

# Function to scrape shlokas from the IIT Kanpur Valmiki Ramayan website
def scrape_shlokas(kanda, sarga):
    url = f"https://www.valmiki.iitk.ac.in/sloka?field_kanda_tid={kanda}&language=dv&field_sarga_value={sarga}"

    # Selenium WebDriver setup
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    # Dynamically locate chromedriver
    chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)

        # Wait for the page to load dynamically
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "views-row"))
        )

        # Extract page content
        soup = BeautifulSoup(driver.page_source, "lxml")

        # Extract shlokas from HTML
        shlokas = []
        rows = soup.find_all("div", class_="views-row")

        for i, row in enumerate(rows, 1):
            shloka_text = row.find("div", class_="field-name-field-shloka")
            transliteration = row.find("div", class_="field-name-field-transliteration")
            translation = row.find("div", class_="field-name-field-translation")
            explanation = row.find("div", class_="field-name-field-explanation")
            comments = row.find("div", class_="field-name-field-comments")

            shlokas.append({
                "kanda": kanda_mapping.get(kanda, "Unknown Kanda"),
                "sarga": sarga,
                "shloka": i,
                "shloka_text": shloka_text.text.strip() if shloka_text else "N/A",
                "transliteration": transliteration.text.strip() if transliteration else "N/A",
                "translation": translation.text.strip() if translation else "N/A",
                "explanation": explanation.text.strip() if explanation else "N/A",
                "comments": comments.text.strip() if comments else "N/A"
            })

        return shlokas

    except Exception as e:
        raise RuntimeError(f"Error while scraping: {str(e)}")

    finally:
        driver.quit()

# Streamlit UI
st.title("📜 Valmiki Ramayan Shloka Scraper")

kanda = st.selectbox("Select Kanda", list(kanda_mapping.keys()), format_func=lambda x: kanda_mapping[x])

# Dynamically set max Sarga based on Kanda (example values, adjust as needed)
max_sarga_mapping = {
    1: 77,  # Bala Kanda
    2: 119, # Ayodhya Kanda
    3: 75,  # Aranya Kanda
    4: 67,  # Kishkindha Kanda
    5: 68,  # Sundara Kanda
    6: 128, # Yuddha Kanda
    7: 111  # Uttara Kanda
}
max_sarga = max_sarga_mapping.get(kanda, 150)
sarga = st.number_input("Enter Sarga Number", min_value=1, max_value=max_sarga, step=1)

if st.button("Scrape Shlokas"):
    st.write(f"🔍 Fetching shlokas for {kanda_mapping[kanda]}, Sarga {sarga}...")
    
    try:
        data = scrape_shlokas(kanda, sarga)

        if data:
            st.json(data)

            # Save JSON file
            json_filename = f"shlokas_kanda{kanda}_sarga{sarga}.json"
            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            st.success(f"✅ Data saved as `{json_filename}`")
        else:
            st.error("❌ No data found for the given Kanda and Sarga.")

    except Exception as e:
        st.error(f"🚨 Error occurred: {str(e)}")