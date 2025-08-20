import requests

def fetch_remoteok_jobs():
    url = "https://remoteok.com/api"  #RemoteOK's public JSON endpoint (only returns up to 100 job listings)
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()  #stop if there's an error

    data = response.json()
    jobs = data[1:]  # Skip the first element (metadata)

    results = []
    for job in jobs:
        title = job.get("position", "").strip()
        job_url = job.get("url", "")
        description_html = job.get("description", "")
        results.append({"title": title, "url": job_url, "description": description_html})
    return results

if __name__ == "__main__":
    job_list = fetch_remoteok_jobs()
    print(f"Fetched {len(job_list)} job postings.\n")
    for i, job in enumerate(job_list, 1):
        print(f"Job {i}: {job['title']}")
        print(f"URL: {job['url']}")
        print(f"Description (first 500 chars):\n{job['description'][:500]}")
        print("—" * 50)
