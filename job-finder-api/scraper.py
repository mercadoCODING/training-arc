#web scraper

import requests #for http requests
from bs4 import BeautifulSoup #for parsing and extracting info from html content

url = "https://remoteok.com/remote-dev-jobs?page=10" #target URL for scraping

headers = {
    "User-Agent": "Mozilla/5.0" #to prevent being flagged as a bot and being blocked by the website
}

response = requests.get(url, headers=headers) #get request and include headers to avoid being blocked 

soup = BeautifulSoup(response.content, "html.parser") # soup object will parse html content from response into a structured object

job_cards = soup.find_all("td", class_= "company position company_and_position") #soup will find all <a> tags with class name = 'tapItem' since indeed follows the same class name


for job in job_cards: #only first 5 listings for testing

    anchor_tag = job.find("a")
    title_tag = anchor_tag.find("h2") #finds <h2> tag inside job card, gets visible text and strips extra whitespace
    #link = "https://www.indeed.com" + job["href"] #extracts URL from <a> tag job["href"] and concatenates to full link

    if anchor_tag and title_tag: #not every td element is a job card, check if anchor and h2 tags exist first for filtering

        title = title_tag.text.strip()
        print(title)
    else:
        continue





    '''anchor = job.find("a")
    if anchor:  # make sure <a> tag was found
        title_tag = anchor.find("h2")
        if title_tag:  # make sure <h2> tag was found inside <a>
            title = title_tag.get_text(strip=True)
            print(f"Job Title: {title}")x
        else:
            print("No <h2> tag found.")
    else:
        print("No <a> tag found.")'''

print("finished!")








