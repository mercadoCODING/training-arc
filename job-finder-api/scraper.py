#web scraper

import requests #for http requests
from bs4 import BeautifulSoup #for parsing and extracting info from html content

url = "https://www.indeed.com/jobs?q=python+developer&l=" #target URL for scraping

headers = {
    "User-Agent": "Mozilla/5.0" #to prevent being flagged as a bot and being blocked by the website
}

response = requests.get(url, headers=headers) #get request and include headers to avoid being blocked 

soup = BeautifulSoup(response.content, "html.parser") # soup object will parse html content from response into a structured object

job_cards = soup.find_all("a", class_="tapItem") #soup will find all <a> tags with class name = 'tapItem' since indeed follows the same class name


for job in job_cards[:5]: #only first 5 listings for testing
    title = job.find("h2").text.strip() #finds <h2> tag inside job card, gets visible text and strips extra whitespace

    link = "https://www.indeed.com" + job["href"] #extracts URL from <a> tag job["href"] and concatenates to full link

    print(response.status_code)
    print(f"Job Title: {title}")
    print(f"Link: {link}\n")

print("finished!")








