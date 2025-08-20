#web scraper for remoteok
#receive html file and parse using beautifulsoup
#can also choose to receive json and parse json for stability in the case the webpage changes html structure.

import requests #for http requests
from bs4 import BeautifulSoup #for parsing and extracting info from html content

base_url = f"https://ph.jobstreet.com/jobs?page=" #base URL for scraping
#append page numbers when no more job cards found

headers = {
    "User-Agent": "Mozilla/5.0" #to prevent being flagged as a bot and being blocked by the website
}

page = 1 #start at page 1

while page <= 5:
    complete_url = base_url + str(page)
    response = requests.get(complete_url, headers=headers) # get request and include headers to avoid being blocked
    soup = BeautifulSoup(response.content, "html.parser") # soup object will parse html content from response into a structured object

    job_cards = soup.find_all("article") #soup will find all <td> tags with class name = class_ since remoteok follows the same class name
    job_cards_n = len(job_cards) #find number of job cards found
    print(job_cards_n)
        

    for job in job_cards:
        
        anchor_tag = job.find("a")

        if anchor_tag: #not every td element is a job card, check if anchor and h2 tags exist first for filtering


            job_url = "https://ph.jobstreet.com"+anchor_tag["href"]

            job_page_response = requests.get(job_url, headers=headers) #overwrite response with new url to scrape job description
            job_page_soup = BeautifulSoup(job_page_response.content, "html.parser") #overwrite soup object with new response content

            title = job_page_soup.find("h1").text.strip()
            job_section = job_page_soup.find("section")
            job_desc = job_section.find_all("p")
            
            print(f"job: {title}")
            print(f"url: {job_url}")
            print(f"job description: {job_desc}")
            print("------------")
        else:
            continue
    
    page += 1 #next page
    
print("finished!")








