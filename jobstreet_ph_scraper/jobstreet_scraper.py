#scrapes first 10,000 jobs in jobstreet and store in single JSON file

import json
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

options.add_argument("--headless=new")  # Uncomment to run chrome without visible window

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

base_url = "https://ph.jobstreet.com/jobs"
driver.get(base_url)

all_jobs = [] #create a list of dictionaries then save data to all_jobs.json
page_limit = 5  # how many pages to scrape
page_counter = 0

while page_counter < page_limit:
    page_counter += 1
    print(f"SCRAPING PAGE {page_counter}")

    # Wait for job cards (article tags) to load
    # WebDriverWait waits for a certain condition such as the presence of an element before proceeding (solution for lazy loaded elements)

    job_cards = WebDriverWait(driver, 15).until( #15 seconds is the maximum time it will wait before timing out
        EC.presence_of_all_elements_located((By.TAG_NAME, "article")) #waits for all article elements to load (job cards)
    )

    #once all cards have loaded:
    for idx, card in enumerate(job_cards, start=1):
        try:
            # Scroll to the card to ensure it's visible
            driver.execute_script("arguments[0].scrollIntoView(true);", card)
            time.sleep(0.5)

            # Click the card to load description
            card.click()

            # Extract title info from card (no need to wait as it is not lazy loaded)
            try:
                title = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").text
            except:
                title = None

            # Wait for description panel to load and extract description
            try:
                description_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation='jobAdDetails']"))
            )
                description = description_elem.text.strip()

            except:
                description = None
                
            try:
                # wait for element containing company name to load before scraping
                company_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "span[data-automation='advertiser-name']")
                    )
                )
                company = company_elem.text.strip()
            except:
                company = None

            try:
                # wait for element containing location to load before scraping
                location_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "span[data-automation='job-detail-location']")
                    )
                )
                location = location_elem.text.strip()
            except:
                location = None

            try:
                #no need to wait for salary as it is not lazy-loaded
                salary = card.find_element(By.CSS_SELECTOR, "span[data-automation='jobSalary']").text 
            except:
                salary = None #not all job cards show their salaries in jobstreet, expect to see nonetype salary values

                
            try:
                #same for the job link
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

with open("all_jobs.json", "w", encoding="utf-8") as myJson:
    json.dump(all_jobs, myJson, indent=4, ensure_ascii=False)
    #adds 4 indents for cleaner text
    #keeps non-ascii special chars intact

print("saved to all_jobs.json!")
print("printing all_jobs.json...")

#read json and load data into container
with open("all_jobs.json", "r", encoding="utf-8") as myJson:
    loaded_jobs = json.load(myJson) #loaded into loaded_jobs and becomes list of dictionaries

for idx, job in enumerate(loaded_jobs, start=1):
    print("-----------------------------------------------------")
    print(f"Job {idx}: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"Salary: {job['salary']}")
    print(f"URL: {job['link']}")
    print(f"Description: {job['description'][:100]}")





