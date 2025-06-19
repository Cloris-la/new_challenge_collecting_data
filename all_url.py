from patchright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from tqdm import tqdm

#function of extracting all url links
def extract_links(page) :
    #parse the website
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", class_="property-results_container")
    results = container.find_all("div", class_="property-item") if container else []
    links = []
    for result in results:
        link = result.find("a", class_= "property-item_link")
        if link:
            links.append("https://www.zimmo.be" + link['href'])
    return links

all_links = []
with sync_playwright() as p:
    
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for i in tqdm(range (1,10)): 
        # request i pages
        url = f"https://www.zimmo.be/fr/rechercher/?search=eyJmaWx0ZXIiOnsic3RhdHVzIjp7ImluIjpbIkZPUl9TQUxFIiwiVEFLRV9PVkVSIl19LCJ6aW1tb0NvZGUiOnsibm90SW4iOlsiTDNNMzAiLCJMM0o5QSIsIkwyWThOIiwiTDYwUEEiXX19LCJzb3J0aW5nIjpbeyJ0eXBlIjoiUkFOS0lOR19TQ09SRSIsIm9yZGVyIjoiREVTQyJ9XSwicGFnaW5nIjp7ImZyb20iOjAsInNpemUiOjE3fX0%3D&p={i}#gallery"
        #open the i page
        page.goto(url)
        page.wait_for_timeout(2000)
        links = extract_links(page)
        
        all_links.extend(links)

    browser.close()
    #using set to remove those same links and then transfer to a list
all_links = list(set(all_links))
#saving this list
with open("zimmoweb_links.txt","w", encoding="utf-8") as f :
    for links in all_links :
        f.write(links +'\n')
print(f"requested {len(all_links)} links")

                