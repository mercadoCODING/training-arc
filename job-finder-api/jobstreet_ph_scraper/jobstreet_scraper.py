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

# options.add_argument("--headless=new")  # Uncomment to run chrome without visible window

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

base_url = "https://ph.jobstreet.com/jobs"
driver.get(base_url)

all_jobs = [] #create a list of dictionaries
page_limit = 1  # how many pages to scrape
page_counter = 0

while page_counter < page_limit:
    page_counter += 1
    print(f"SCRAPING PAGE {page_counter}")

    # Wait for job cards to load
    job_cards = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
    )

    for idx, card in enumerate(job_cards, start=1):
        try:
            # Scroll to the card to ensure it's visible
            driver.execute_script("arguments[0].scrollIntoView(true);", card)
            time.sleep(0.5)

            # Click the card to load description
            card.click()

            # Wait for description panel to load and extract description
            description_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation='jobAdDetails']"))
            )
            description = description_elem.text.strip()

            # Extract job info from card
            try:
                title = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").text
            except:
                title = None

            try:
                company = card.find_element(
                    By.CSS_SELECTOR,
                    "span._1lns5ab0._6c7qzn50.od4ez80.od4ez81.od4ez81t.od4ez88._1lwlriv4"
                ).text
            except:
                company = None

            try:
                location = card.find_element(
                    By.CSS_SELECTOR,
                    "span._1lns5ab0._6c7qzn50.od4ez80.od4ez81.od4ez81t.od4ez86._1lwlriv4"
                ).text
            except:
                location = None

            try:
                salary = card.find_element(By.CSS_SELECTOR, "span[data-automation='jobSalary']").text
            except:
                salary = None

            try:
                link = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").get_attribute("href")
            except:
                link = None

            all_jobs.append({ #append all details to job dictionary
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "link": link,
                "description": description
            })

            print(f"Scraped job {idx}: {title}")

        except Exception as e:
            print(f"Failed to scrape job card {idx}: {e}")
            continue

    # Try to go to next page
    try:
        next_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next']"))
        )   
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(2) #wait for page to load
    except:
        print("No more pages.")
        break

driver.quit()

# Print results
for i, job in enumerate(all_jobs, start=1):
    print(f"{i}. {job['title']} \nCompany: {job['company']} \nLocation: {job['location']} \n Salary: {job['Salary']}")
    print(f"Description: {job['description'][:500]}...\n") 
