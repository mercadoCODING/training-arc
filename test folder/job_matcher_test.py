# test file only, not used within app

from sentence_transformers import SentenceTransformer, util
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

#load pretrained sentence transformer model
#model = SentenceTransformer('all-MiniLM-L6-v2') #faster and lightweight
model = SentenceTransformer('all-mpnet-base-v2') #more accurate


#sample resumes:

resume = """ Software engineer, developer, and problem-solver with a curiosity and passion for learning."""

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

job_descriptions = [] #create a list disctionaries with keys title and description
page_limit = 5  # how many pages to scrape
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
                link = card.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']").get_attribute("href")
            except:
                link = None

            job_descriptions.append({"description":description, "title": title, "link": link})

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


resume_embedding = model.encode(resume, convert_to_tensor=True) #convert resume into tensors/embeddings

job_embeddings= model.encode([f"{job['title']}: {job['description']}" for job in job_descriptions], convert_to_tensor=True) 

#first param unpacks the values of keys title and description from job_descriptions into one list (combines title and description into one string for conversion)
#encode method then converts text into tensors/embeddings
#job_embeddings is technically only one tensor (not a list of embeddings), but each row of the tensor is one job embedding, so it acts like a list

cosine_scores = util.cos_sim(resume_embedding, job_embeddings) #compute for cosine similarity and store in a single tensor
#similarly to job_embeddings, cosine_scores acts as a list of scores but is a tensor where each row is a cosine score.

for idx, (job_title, url, cosine_score) in enumerate(zip([f"{job['title']}" for job in job_descriptions], [f"{job['link']}" for job in job_descriptions], cosine_scores[0])):
    print(f"Job {idx}: {job_title}")
    print(f"Cosine similarity: {cosine_score}")
    print(f"URL: {url}\n")