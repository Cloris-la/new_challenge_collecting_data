from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from tqdm import tqdm
import csv

# function tranfers to soup and extracts each page's url, return a list of all links
def extract_links(page):
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", class_="property-results_container")
    search_results = container.find_all("div", class_="property-item") if container else []
    links = []
    for search_result in search_results:
        link = search_result.find("a", class_="property-item_link")
        if link and "href" in link.attrs:
            links.append("https://www.zimmo.be" + link["href"])
    return links

all_links = []
# main program for request pages which maintain 21 properties / page
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) #launch browser first
    page = browser.new_page()

    page.wait_for_timeout(2000) #timeout 2 seconds

    for i in tqdm(range(1, 3)):  # loop 2 pages
        url = f'https://www.zimmo.be/fr/rechercher/?search=eyJmaWx0ZXIiOnsic3RhdHVzIjp7ImluIjpbIkZPUl9TQUxFIiwiVEFLRV9PVkVSIl19LCJ6aW1tb0NvZGUiOnsibm90SW4iOlsiTDgwTjUiLCJLTUQ4MCIsIkw0RVhHIiwiTDBBUjIiXX19LCJzb3J0aW5nIjpbeyJ0eXBlIjoiUkFOS0lOR19TQ09SRSIsIm9yZGVyIjoiREVTQyJ9XSwicGFnaW5nIjp7ImZyb20iOjE3LCJzaXplIjoyMX19&p={i}#gallery'    
        page.goto(url)
        page.wait_for_timeout(2000)
        link = extract_links(page)
        all_links.extend(link)

    browser.close()

# using set to automatically remove same link and tranfer to a list
all_links = list(set(all_links))
# saving all links into a txt file
with open("zimmoweb_links.txt", "w", encoding="utf-8") as f:
    for link in all_links:
        f.write(link + "\n")

print(f"🎉 共保存了 {len(all_links)} 个房产链接")


# =============== extract_property_info=======================

# get features under ul.main_features
def extract_main_features (soup) :
    data = {'Type':"N/A",
            "Surf.habitable":"N/A",
            "Chambre":"N/A",
            'Salles de bain':"N/A",
            'Construit en':"N/A",
            'PEB':'N/A',
            'Obligation de rénovation':"N/A",
            'RC':"N/A"}
    features = {}
    feature_list = soup.find('ul',class_='main-features')
    if feature_list :
        for li in feature_list :
            lable = li.find('strong')
            value = li.find('span')
            if lable and value :
                key = lable.get_text(strip = True)
                val = value.get_text(strip = True)
                if key == "Type" :
                    data['Type'] = val
                elif key == 'Surf.habitable':
                    data['Surf.habitable'] = val
                elif key == "Chambre" :
                    data['Chambre'] = val
                elif key == 'Salles de bain':
                    data['Salles de bain'] = val
                elif key == 'Construit en':
                    data['Construit en'] = val
                elif key == 'PEB':
                    data['PEB'] = val
                elif key == 'Obligation de rénovation':
                    data['Obligation de rénovation'] = val
                elif key == 'RC':
                    data['RC'] = val
    return data

def extract_property_info(page,url) :
    try:
        page.goto(url,timeout = 2000)
        page.wait_for_timeout(3000)
        soup = BeautifulSoup(page.content(),'html.parser')

        # CSS selector
        locality = soup.find('h2',class_='section-title __full-address')
        #price = soup.find('span',class_='feature-value ')
        features = extract_main_features(soup)
        return{
            "url":url,
            "type":features['Type'],
            "Surf.habitable":features['Surf.habitable'],
            "Chambre":features['Chambre'],
            'Salles de bain':features['Salles de bain'],
            'Construit en':features['Construit en'],
            'PEB':features['PEB'],
            'Obligation de rénovation':features['Obligation de rénovation'],
            'RC':features['RC']
        }

    except Exception as e:
        print(f"{e}")

## ===== 调试 extract_property_info 函数 =====
print("\n🚀 正在测试 extract_property_info ...")

# 读取前几条链接进行测试
with open("zimmoweb_links.txt", "r", encoding="utf-8") as f:
    test_links = [line.strip() for line in f.readlines()[:3]]  # 测试前3条链接

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for i, url in enumerate(test_links, 1):
        print(f"\n🔍 正在提取第 {i} 条：{url}")
        info = extract_property_info(page, url)
        if info:
            for k, v in info.items():
                print(f"{k}: {v}")

    browser.close()