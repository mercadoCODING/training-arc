# Headless JobStreet scraper with enhanced stealth - optimized for cloud deployment

import json
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Variables and counters
all_jobs = []  # List to store all scraped jobs
job_limit = 5000  # Number of pages to scrape
job_counter = 0
page_counter = 1

# ENHANCED STEALTH CHROME OPTIONS
options = Options()
options.add_argument("--headless=new")  # Headless mode
options.add_argument("--no-sandbox")  # Required for Docker/cloud environments
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("--disable-gpu")  # Not needed in headless mode
options.add_argument("--window-size=1920,1080")  # Set consistent window size
options.add_argument("--start-maximized")

# CRITICAL ANTI-DETECTION OPTIONS
options.add_argument("--disable-blink-features=AutomationControlled")  # Remove automation flags
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Remove "Chrome is being controlled" banner
options.add_experimental_option('useAutomationExtension', False)  # Disable automation extension

# Realistic user agent (Linux-based for cloud servers)
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Additional stealth options
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")

# Explicitly tell Selenium where Chrome is
options.binary_location = "/usr/bin/google-chrome"

# HIDE WEBDRIVER PROPERTY (MOST CRITICAL!)
def hideDriverProperty(driver):
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        
        // Override plugins to avoid headless detection
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        
        // Override languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
        
        // Chrome runtime
        window.chrome = {
            runtime: {}
        };
        
        // Permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
    '''
    })

def restartDriver():
    global driver
    driver.quit()

    # wait 2 seconds for linux to kill the driver and release resources before creating new driver
    time.sleep(2) # we can use psutil instead to actually wait for the process to be killed
                  
    driver = webdriver.Chrome(options=options) #create new driver with options
    hideDriverProperty(driver) # for stealth

def createJobUrl(page_number):
    return f"https://ph.jobstreet.com/jobs?page={page_number}"

#initialize webdriver
driver = webdriver.Chrome(options=options)
hideDriverProperty(driver) # for stealth

# START SCRAPING
base_url = createJobUrl(page_counter)

print("=" * 80)
print("ENHANCED STEALTH SCRAPER - Starting...")
print("=" * 80)

driver.get(base_url)

# Human-like delay after page load
time.sleep(random.uniform(3, 5))

# Debug info
print("\n[DEBUG] Initial page load:")
print(f"  Page title: {driver.title}")
print(f"  Current URL: {driver.current_url}")
#driver.save_screenshot("debug.png") remove screenshots, increases memory usage in the cloud
print(f"  Screenshot saved: debug.png")
print(f"  Page source length: {len(driver.page_source)} characters")

# Check if we got blocked
if "Access Denied" in driver.page_source or len(driver.page_source) < 5000:
    print("\n⚠️  WARNING: Possible bot detection!")
    print("  Page source preview:")
    print(driver.page_source[:1000])
else:
    print("  ✓ Page loaded successfully\n")

print("=" * 80)
print("Starting job extraction...")
print("=" * 80)

while job_counter < job_limit:
    print(f"\n[PAGE {page_counter}] Scraping...")

    # Wait for job cards (article tags) to load
    try:
        #initializes a job_cards list of WebELements (pointers to the article tags)
        job_cards = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
        )
        print(f"  ✓ Found {len(job_cards)} job cards")
    except Exception as e:
        print(f"  ✗ Timeout waiting for job cards: {e}")
        print(f"  Current URL: {driver.current_url}")
        #driver.save_screenshot(f"error_page_{page_counter}.png") remove screenshots, increases memory usage in the cloud
        break

    # Process each job card
    for idx, card in enumerate(job_cards, start=1):
        if job_counter < job_limit:
            job_counter += 1
        else:
            break
        try:
            # Human-like smooth scroll to card
            driver.execute_script("""
                arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});
            """, card)
            
            # Random human-like delay
            time.sleep(random.uniform(0.5, 1.0))

            # Click the card to load description
            card.click()
            
            # Small delay after click
            time.sleep(random.uniform(0.3, 0.7))

            # Extract title
            try:
                title = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").text
            except:
                title = None

            # Wait for and extract description
            try:
                description_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation='jobAdDetails']"))
                )
                description = description_elem.text.strip()
            except:
                description = None
                
            # Wait for and extract company name
            try:
                company_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "span[data-automation='advertiser-name']")
                    )
                )
                company = company_elem.text.strip()
            except:
                company = None

            # Wait for and extract location
            try:
                location_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "span[data-automation='job-detail-location']")
                    )
                )
                location = location_elem.text.strip()
            except:
                location = None

            # Extract salary (not always available)
            try:
                salary = card.find_element(By.CSS_SELECTOR, "span[data-automation='jobSalary']").text 
            except:
                salary = None

            # Extract job link
            try:
                link = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").get_attribute("href")
            except:
                link = None 

            # Append job data to list
            all_jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "link": link,
                "description": description
            })

            print(f"  ✓ [{idx}/{len(job_cards)}] {title}")
        except Exception as e:
            print(f"  ✗ [{idx}/{len(job_cards)}] Failed: {e}")
            continue

    # Restart the driver every 10 pages to avoid memory leaks then move to the next page
    if page_counter % 10 == 0:
        print("Restarting driver to free up resources...")
        restartDriver()

    page_counter += 1

    # navigate to next page
    driver.get(createJobUrl(page_counter))

driver.quit()

# ============================================
# SAVE RESULTS
# ============================================
output_file = "all_jobs.json"
with open(output_file, "w", encoding="utf-8") as myJson:
    json.dump(all_jobs, myJson, indent=4, ensure_ascii=False)

print("\n" + "=" * 80)
print(f"✓ SCRAPING COMPLETE!")
print(f"✓ Successfully saved {len(all_jobs)} jobs to {output_file}")
print("=" * 80)

if all_jobs:
    print("\n📋 Preview of scraped jobs:")
    print("=" * 80)

    # Display preview of scraped data
    for idx, job in enumerate(all_jobs[:3], start=1):  # Show first 3 jobs
        print(f"\n🔹 Job {idx}:")
        print(f"  Title: {job['title']}")
        print(f"  Company: {job['company']}")
        print(f"  Location: {job['location']}")
        print(f"  Salary: {job['salary']}")
        print(f"  URL: {job['link']}")
        if job['description']:
            print(f"  Description: {job['description'][:100]}...")
        else:
            print(f"  Description: N/A")

    if len(all_jobs) > 3:
        print(f"\n... and {len(all_jobs) - 3} more jobs")
else:
    print("\n⚠️  No jobs were scraped!")
    print("Check debug.png and error screenshots for details.")

print("\n" + "=" * 80)


# ============================================
# UPLOAD TO GOOGLE CLOUD STORAGE
# ============================================
try:
    from google.cloud import storage

    # Get bucket name from environment variable (set in Cloud Run)
    bucket_name = os.getenv("BUCKET_NAME", "my-jobstreet-bucket")

    # Use timestamp to avoid overwriting files
    from datetime import datetime
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    destination_blob = f"scrapes/all_jobs_{timestamp}.json"

    print(f"\n📤 Uploading {output_file} to gs://{bucket_name}/{destination_blob} ...")

    # Initialize GCS client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)

    # Upload the file
    blob.upload_from_filename(output_file)

    print(f"✓ Uploaded successfully to GCS as {destination_blob}")

except Exception as e:
    print(f"⚠️  Failed to upload to GCS: {e}")