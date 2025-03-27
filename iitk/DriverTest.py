from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode (no UI)

service = Service("chromedriver.exe")  # Path to chromedriver
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.valmiki.iitk.ac.in")
print(driver.page_source)
driver.quit()
