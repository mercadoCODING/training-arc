#scrapes first 10,000 jobs in jobstreet and store in single JSON file

#title, link, and salary works, the rest don't, all null.

import json
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Setup Chrome with webdriver-manager
options = Options()
options.add_argument("--start-maximized") #starts chrome maximized to avoid clickable errors with responsive layouts
options.add_argument("--headless=new")  # Uncomment to run chrome without visible window

#Use Linux path if it exists (for cloud hosting), otherwise fall back to Windows (for local testing)
if os.path.exists("/usr/bin/chromedriver"):
    CHROME_DRIVER_PATH = "/usr/bin/chromedriver" #Point directly to the ChromeDriver path (installed in docker image)
else:
    from webdriver_manager.chrome import ChromeDriverManager
    CHROME_DRIVER_PATH = ChromeDriverManager().install()

driver = webdriver.Chrome(
    service=Service(CHROME_DRIVER_PATH),
    options=options
)

#bunch of settings to avoid bot detection by the website
stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

base_url = "https://ph.jobstreet.com/jobs"
driver.get(base_url)

all_jobs = [] #create a list of dictionaries then save data to all_jobs.json
job_limit = 3  # how many jobs to scrape
job_counter = 0
page_counter = 0

while job_counter < job_limit:
    page_counter += 1
    print(f"SCRAPING PAGE {page_counter}")

    # Wait for job cards (article tags) to load
    # WebDriverWait waits for a certain condition such as the presence of an element before proceeding (solution for lazy loaded elements)

    job_cards = WebDriverWait(driver, 30).until( #30 seconds is the maximum time it will wait before timing out
        EC.presence_of_all_elements_located((By.TAG_NAME, "article")) #waits for all article elements to load (job cards)
    )

    #once all cards have loaded:
    for idx, card in enumerate(job_cards, start=1):

        if job_counter < job_limit:
            job_counter += 1
        else:
            break

        try:
            # Scroll to the card to ensure it's visible
            driver.execute_script("arguments[0].scrollIntoView(true);", card)
            time.sleep(0.5)

            # Click the card to load description
            card.click()

            # Extract title info from card (no need to wait as it is not lazy loaded)
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']") #save html element
                title = title_elem.text.strip() #strip html tags and save text to company variable
            except:
                title = None

            # Wait for description panel to load and extract description (use WebDriverWait and presence_of_elem... for JS-loaded elements)
            # use find_element for static DOM elements
            try:
                description_elem = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation='jobAdDetails']"))
            )
                description = description_elem.text.strip() #strip html tags from element and save text to description variable

            except:
                description = None
                
            try:
                company_elem =  card.find_element(By.CSS_SELECTOR, "span[data-automation='advertiser-name']") 
                company = company_elem.text.strip() 
            except:
                company = None

            try:
                location_elem = card.find_element(By.CSS_SELECTOR, "span[data-automation='job-detail-location']")
                location = location_elem.text.strip()
            except:
                location = None

            try:
                #no need to wait for salary as it is not lazy-loaded
                salary_elem = card.find_element(By.CSS_SELECTOR, "span[data-automation='jobSalary']")
                salary = salary_elem.text.strip()
            except:
                salary = None #not all job cards show their salaries in jobstreet, expect to see nonetype salary values

                
            try:
                #same for the job link
                link_elem = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']")
                link = link_elem.get_attribute("href")
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





