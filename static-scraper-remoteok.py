# Scraper for scraping remoteok.com

import requests
from bs4 import BeautifulSoup
from pprint import pprint


def scrape_page(keyword):
    response = requests.get(
        f"https://remoteok.com/remote-{keyword}-jobs",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        },
    )

    soup = BeautifulSoup(response.content, "html.parser")

    jobs = soup.find("table", id="jobsboard").find_all(attrs={"data-company": True})

    all_jobs = []

    for job in jobs:
        title = job.find("h2").text.strip()
        company = job.find("h3").text.strip()
        tags = job.find("td", class_="tags").find_all("h3")
        tags = [tag.text.strip() for tag in tags]
        region = job.find("div", class_="location").text
        salary = job.find("div", class_="location").next_sibling.text
        url = "https://remoteok.com" + job.find("a")["href"]

        job_data = {
            "title": title,
            "company": company,
            "tags": tags,
            "region": region,
            "salary": salary,
            "url": url,
        }

        all_jobs.append(job_data)

    return all_jobs


keywords = ["flutter", "python", "golang"]

for keyword in keywords:
    all_jobs = scrape_page(keyword)

    print(f"---- {keyword} jobs list ----")
    pprint(all_jobs)  # formatted object output
    print()
