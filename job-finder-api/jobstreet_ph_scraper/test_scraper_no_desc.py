from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome with webdriver-manager
options = Options()
options.add_argument("--start-maximized") #starts chrome maximized to avoid clickable errors with responsive layouts

# options.add_argument("--headless=new")  # uncomment to run without opening a window

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Start scraping
base_url = "https://ph.jobstreet.com/jobs"

driver.get(base_url)

all_jobs = []

counter = 0

while counter < 3:
    
    counter +=1
    try:
        # wait until job cards (articles) are present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
        )

        job_cards = driver.find_elements(By.TAG_NAME, "article")

        for card in job_cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").text
            except:
                title = None

            try:
                company = card.find_element(By.CSS_SELECTOR, "span[class='_1lns5ab0 _6c7qzn50 od4ez80 od4ez81 od4ez81t od4ez88 _1lwlriv4']").text
            except:
                company = None

            try:
                location = card.find_element(By.CSS_SELECTOR, "span[class='_1lns5ab0 _6c7qzn50 od4ez80 od4ez81 od4ez81t od4ez86 _1lwlriv4']").text
            except:
                location = None

            try:
                salary = card.find_element(By.CSS_SELECTOR,"span[data-automation='jobSalary']").text
            except:
                salary = None

            try:
                link = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").get_attribute("href")
            except:
                link = None

            all_jobs.append({
                "title": title,
                "company": company,
                "salary": salary,
                "location": location,
                "link": link
            })

        print(f"Scraped {len(job_cards)} jobs on this page")

        #Try to click "Next" button
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next']")
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(2)  # wait a bit for next page to load
        except:
            print("No more pages found.")
            break

    except Exception as e:
        print("Error:", e)
        break

driver.quit()

#Print results
for job in all_jobs:
    print(job)
