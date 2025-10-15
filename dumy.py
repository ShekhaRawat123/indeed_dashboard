import undetected_chromedriver as uc

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json, time, contextlib



KEYWORDS = ["data scraping", "web automation"]
LOCATION = ["India"]
BASE_URL = "https://www.indeed.com/jobs"

# 🔹 Load old data (if exists)
try:
    with open("data.json", "r", encoding="utf-8") as f:
        old_jobs = json.load(f)
except:
    old_jobs = []

# Helper: check duplicate
def is_duplicate(new_job):
    for job in old_jobs:
        if (
            job["title"] == new_job["title"]
            and job["company"] == new_job["company"]
            and job["location"] == new_job["location"]
        ):
            return True
    return False


driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 25)
new_jobs = []

for keyword in KEYWORDS:
    url = f"{BASE_URL}?q={keyword.replace(' ', '+')}&l={LOCATION[0]}"
    driver.get(url)
    time.sleep(5)

    # Wait for job cards
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "job_seen_beacon")))

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(3)

    job_cards = soup.select("div.job_seen_beacon")

    for card in job_cards[:10]:  # limit to first 10 jobs per keyword
        title = card.select_one("h2.jobTitle")
        company = card.select_one("span.companyName")
        location = card.select_one("div.companyLocation")
        link_tag = card.select_one("a[data-jk]")

        job_data = {
            "keyword": keyword,
            "title": title.get_text(strip=True) if title else "No title",
            "company": company.get_text(strip=True) if company else "No company",
            "location": location.get_text(strip=True) if location else "No location",
             "job_link": link_tag['href'] if link_tag  and link_tag.has_attr("href") else "  LINK  not available"
        }

        # ✅ Skip if duplicate
        if not is_duplicate(job_data):
            new_jobs.append(job_data)
            print(f"{job_data['title']} | {job_data['company']} | {job_data['location']}")
        else:
            print(f"⚠️ Skipped duplicate: {job_data['title']}")

    print("-" * 60)

# 🔹 Merge old + new (only unique)
all_jobs = old_jobs + new_jobs

# 🔹 Save final data
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=4)

with contextlib.suppress(Exception):
    driver.quit()


print(f"\n✅ {len(new_jobs)} new jobs added.")
print("📁 Data saved successfully in 'data.json'")

