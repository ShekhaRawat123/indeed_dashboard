from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions  as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time 
import json
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
KEYWORDS = ["data scraping" , "web automation"]
LOCATION = ["India "]
BASE_URL = "https://www.indeed.com/jobs"
try:
    with open("data.json" ,  "r") as f:
        old_jobs =  json.load(f)
except:
        old_jobs= []

driver = uc.Chrome(options=options)

time.sleep(5)

def  is_duplicate(new_jobs):
     for job in old_jobs:
          if (job["title"] == new_jobs["title"]
           and job['company']  == new_jobs["company"]
          and job['location'] ==  new_jobs["location"]
          ):
               return True
     return False
     
new_jobs = []
for keyword in KEYWORDS :
     url  = f"{BASE_URL}?q={keyword.replace(' ' ,'+')}&l={LOCATION[0]}"
     driver.get(url) 
     time.sleep(3)

     WebDriverWait(driver, 25).until(
     EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
      )
     
     html = driver.page_source
     soup = BeautifulSoup(html, "html.parser")
        

# job_cards = soup.find_all("div" , class_= ["slider_container", "css-nqpl5t", "eu4oa1w0"])
     job_cards = soup.select("div.slider_container.css-nqpl5t.eu4oa1w0")

     

     for card in job_cards[0:10]:
          title = card.select_one("h2.jobTitle")
          company = card.select_one("span.css-1h7lukg.eu4oa1w0")
          location = card.select_one("div.css-1restlb.eu4oa1w0")
          link_tag = card.select_one("a[data-jk], a.tapItem")


          job_Data= {
               "title" : title.get_text(strip= True) if title else "no title",
               "company" : company.get_text(strip= True) if company else "no company name ",
                "location" : location.get_text(strip=True) if location else "no location",
                "link" : link_tag["href"] if link_tag and link_tag.has_attr("href") else "no link"
          }  


          if  not is_duplicate(job_Data) :
               new_jobs.append(job_Data) 
               print (f"  title={job_Data['title']}, company= {job_Data['company']} location = {job_Data['location']}")
          else:
               print(f"dulicate jon {job_Data['link']}")

          print("-"* 60)
all_job =  new_jobs + old_jobs

with open("data.json" , "w" , encoding= "utf-8")  as f:
     json.dump(all_job, f, ensure_ascii=False, indent=4)


print(f"\n✅ {len(new_jobs)} new jobs added.")
print(" Data saved successfully in 'data.json'")


driver.quit()