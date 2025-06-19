from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

def fetch_volatility_data(url="https://slotcatalog.com/en/slots/top"):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    print("🌐 Launching headless browser...")
    driver.get(url)
    time.sleep(3)  # wait for JS to load

    games = []
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, "div.table-slot__row")
        for row in rows[:10]:  # scrape top 10 games
            try:
                title = row.find_element(By.CSS_SELECTOR, "div.name span").text
                rtp = row.find_element(By.CSS_SELECTOR, "div.rtp").text
                volatility = row.find_element(By.CSS_SELECTOR, "div.volatility span").get_attribute("title")
                games.append({"Title": title, "RTP": rtp, "Volatility": volatility})
            except Exception as e:
                continue
    finally:
        driver.quit()

    # Save to CSV
    df = pd.DataFrame(games)
    df.to_csv("scraped_volatility.csv", index=False)
    print("✅ Scraped data saved to scraped_volatility.csv")

if __name__ == "__main__":
    fetch_volatility_data()
