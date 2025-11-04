import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# -----------------------------------
# SETUP
# -----------------------------------
options = Options()
options.add_argument("--headless")  # required for Cloud Run (headless mode)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")


# Use Linux path if available (for Cloud Run), else use webdriver-manager locally
if os.path.exists("/usr/bin/chromedriver"):
    CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
else:
    from webdriver_manager.chrome import ChromeDriverManager
    CHROME_DRIVER_PATH = ChromeDriverManager().install()

driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

driver.set_window_size(1920, 1080)

# -----------------------------------
# SCRAPER CONFIG
# -----------------------------------
base_url = "https://ph.jobstreet.com/jobs"
driver.get(base_url)
time.sleep(3)  # allow JS to initialize

all_jobs = []
page_limit = 5
page_counter = 0

def scroll_page():
    """Scrolls through the page to trigger lazy-loaded job cards."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(5):  # scroll 5 times
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# -----------------------------------
# MAIN LOOP
# -----------------------------------
while page_counter < page_limit:
    page_counter += 1
    print(f"SCRAPING PAGE {page_counter}")

    scroll_page()

    try:
        job_cards = WebDriverWait(driver, 25).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
        )
    except TimeoutException:
        print("⚠️ No job cards found. Retrying scroll...")
        scroll_page()
        continue

    for idx, card in enumerate(job_cards, start=1):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", card)
            time.sleep(0.5)
            card.click()
            time.sleep(1)

            title = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").text
            link = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").get_attribute("href")

            try:
                description_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation='jobAdDetails']"))
                )
                description = description_elem.text.strip()
            except TimeoutException:
                description = None

            try:
                company = driver.find_element(By.CSS_SELECTOR, "span[data-automation='advertiser-name']").text
            except:
                company = None

            try:
                location = driver.find_element(By.CSS_SELECTOR, "span[data-automation='job-detail-location']").text
            except:
                location = None

            try:
                salary = card.find_element(By.CSS_SELECTOR, "span[data-automation='jobSalary']").text
            except:
                salary = None

            all_jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "link": link,
                "description": description
            })

            print(f"✅ Scraped job {idx}: {title}")

        except Exception as e:
            print(f"❌ Failed to scrape job card {idx}: {e}")
            continue

    # Next page navigation
    try:
        next_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next']"))
        )
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(3)
    except TimeoutException:
        print("🚫 No more pages found.")
        break

driver.quit()

# -----------------------------------
# SAVE RESULTS
# -----------------------------------
with open("all_jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, indent=4, ensure_ascii=False)

print(f"💾 Saved {len(all_jobs)} jobs to all_jobs.json")

# Optional: print sample output
for idx, job in enumerate(all_jobs[:5], start=1):
    print(f"\n--- Job {idx} ---")
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"Salary: {job['salary']}")
    print(f"Link: {job['link']}")
