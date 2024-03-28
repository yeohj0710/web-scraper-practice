from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv


def scrape_page(keyword):
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://www.wanted.co.kr/jobsfeed")
    time.sleep(1)

    page.click("button.Aside_searchButton__Xhqq3")
    time.sleep(1)

    page.get_by_placeholder("검색어를 입력해 주세요.").fill(keyword)
    time.sleep(1)

    page.keyboard.down("Enter")
    time.sleep(1)

    page.click("a#search_tab_position")
    time.sleep(1)

    for _ in range(4):
        page.keyboard.down("End")
        time.sleep(1)

    content = page.content()

    playwright.stop()

    soup = BeautifulSoup(content, "html.parser")

    jobs = soup.find_all("div", class_="JobCard_container__FqChn")

    jobs_db = []

    for job in jobs:
        link = f"https://www.wanted.co.kr{job.find('a')['href']}"
        title = job.find("strong", class_="JobCard_title__ddkwM").text
        company = job.find("span", class_="JobCard_companyName__vZMqJ").text

        job = {
            "title": title,
            "company": company,
            "link": link,
        }

        jobs_db.append(job)

    return jobs_db


def file_write(jobs_db, keyword):
    file_name = f"dynamic-scraper-wanted-jobs-{keyword}.csv"
    file = open(file_name, "w", encoding="utf-8", newline="")
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Link"])

    for job in jobs_db:
        writer.writerow(job.values())

    file.close()

    return file_name


keyword = input("검색어를 입력해 주세요. (ex: flutter): ")

jobs_db = scrape_page(keyword)

print(f"총 {len(jobs_db)}건의 채용공고가 있어요.")

file_name = file_write(jobs_db, keyword)

print(f"{file_name}가 생성되었습니다.")
