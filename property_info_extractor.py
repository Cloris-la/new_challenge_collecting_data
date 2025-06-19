from patchright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from all_url import all_links
import csv

def extract_info(page,url) :
    try:
        page.goto(url)
        page.wait_for_timeout(3000)

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        #extract info through CSS
        locality = soup.find('h2',class_='section-title __full-address')
        return{"url":url,
            "locality":locality}
    except Exception as e :
        print(f"request {url} failed, mistake {e}")
        return{"url":url,
               "locality":"Error"}
#main program    
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    #read zimmoweb_links.txt file
    with open("zimmoweb_links.txt","r",encoding = "utf-8") as f :
        urls = [line.strip() for line in f if line.strip()]

    #write into CSV file
    with open("zimmoweb_data.csv","w",newline="",encoding="utf-8") as csvfile :
        fieldname = ["url","locality"]
        writer = csv.DictWriter(csvfile,fieldnames=fieldname)
        writer.writeheader

        for i, url in enumerate(urls,1) :
            print(f"the {i} property's url")
            data = extract_info(page,url)
            writer.writerow(data)
    browser.close()
    


        