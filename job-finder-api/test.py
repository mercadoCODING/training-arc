#web scraper
#receive html file and parse using beautifulsoup
#can also choose to receive json and parse json for stability in the case the webpage changes html structure.

import requests #for http requests
from bs4 import BeautifulSoup #for parsing and extracting info from html content

base_url = f"https://remoteok.com/?tags=dev&action=get_jobs&offset=" #base URL for scraping (incomplete)
# added 'tags=dev&action=get_jobs&offset=20' because of lazy loading issue in using 'https://remoteok.com/remote-dev-jobs'
# offset = the number of jobs to be skipped, to load further jobs
# append offsets in offset= to traverse the job cards in the website

headers = {
    "User-Agent": "Mozilla/5.0" #to prevent being flagged as a bot and being blocked by the website
}

job_counter = 0

while job_counter < 10000:
    complete_url = base_url + str(job_counter) #append the number of jobs found in offset to skip those jobs in the html and load new ones to solve lazy loading issue
    response = requests.get(complete_url, headers=headers) #get request and include headers to avoid being blocked
    soup = BeautifulSoup(response.content, "html.parser") # soup object will parse html content from response into a structured object

    job_cards = soup.find_all("td", class_= "company position company_and_position") #soup will find all <td> tags with class name = class_ since remoteok follows the same class name

    if not job_cards:  # stop if no jobs found
        break

    for job in job_cards:
        
        job_counter += 1 #increment counter
        anchor_tag = job.find("a")
        title_tag = anchor_tag.find("h2") #finds <h2> tag inside job card, gets visible text and strips extra whitespace
        #link = "https://www.indeed.com" + job["href"] #extracts URL from <a> tag job["href"] and concatenates to full link

        if anchor_tag and title_tag: #not every td element is a job card, check if anchor and h2 tags exist first for filtering

            title = title_tag.text.strip()
            job_url = "https://www.remoteok.com"+anchor_tag["href"]
            print(f"job {job_counter+1}: {title}")
            print(f"url: {job_url}")
            print("------------")
        else:
            continue

print(f"found {job_counter} jobs!")
print("finished!")








