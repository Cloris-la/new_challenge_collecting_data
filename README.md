🏠 Zimmo.be Belgium - Real Estate Data Scraper
A robust Python web scraper designed to extract comprehensive real estate listing data from Zimmo.be, one of Belgium's leading property platforms. This tool captures detailed property information for market analysis, research, and investment purposes.

✨ Features
Dual-Phase Extraction: First collects property listing URLs, then extracts detailed information from each listing

Comprehensive Data Capture: Extracts 10+ data points per property including type, size, rooms, construction year, and energy efficiency ratings

Pagination Handling: Automatically navigates through search result pages to collect all available listings

Duplicate Prevention: Uses set operations to automatically remove duplicate URLs

Structured Output: Saves data in both raw text format and structured CSV format

Progress Tracking: Utilizes tqdm for visual progress indication during scraping

📋 Data Points Captured
Category	Data Fields
Property Identification	URL, Property Type
Size & Layout	Living Area (Surf.habitable), Bedrooms (Chambre), Bathrooms (Salles de bain)
Construction Details	Construction Year (Construit en)
Energy Efficiency	EPC Rating (PEB), Renovation Obligation (Obligation de rénovation), RC Rating
Location	Full Address (Locality)
🛠️ Tech Stack
Python 3

Playwright - Browser automation and web scraping

BeautifulSoup4 - HTML parsing and data extraction

tqdm - Progress bar visualization

CSV - Standard library for data export

📦 Project Structure
text
zimmo-scraper/
├── all_url.py                 # Main script to extract property URLs
├── property_info_extractor.py # Script to extract detailed property info
├── zimmoweb_links.txt        # Generated file containing property URLs
├── zimmoweb_data.csv         # Generated file containing property data
└── README.md                 # This file
🔧 Installation & Setup
Clone or download the project files

Install required dependencies

bash
pip install playwright beautifulsoup4 tqdm
Install Playwright browsers

bash
playwright install
🚀 Usage
Phase 1: Extract Property URLs
Run the main script to collect property listing URLs:

bash
python all_url.py
This will:

Launch a browser window (set headless=True in code to run in background)

Navigate through search result pages

Extract all property listing URLs

Save unique URLs to zimmoweb_links.txt

Display progress with a visual progress bar

Phase 2: Extract Property Details
Uncomment and modify the extraction code in property_info_extractor.py to process the saved URLs:

python
# Uncomment and modify this section in property_info_extractor.py
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Read saved URLs
    with open("zimmoweb_links.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    # Write to CSV file
    with open("zimmoweb_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["url", "locality", "price", "property_type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, url in enumerate(urls, 1):
            print(f"Processing property {i}")
            data = extract_info(page, url)
            writer.writerow(data)
    
    browser.close()
⚠️ Important Notes
Legal Compliance: Always review Zimmo.be's terms of service and robots.txt before scraping

Rate Limiting: The script includes delays between requests (2000-3000ms) to avoid overwhelming the server

Error Handling: The code includes try-catch blocks to handle potential extraction errors gracefully

Data Accuracy: Verify the CSS selectors regularly as website structure may change over time

🔍 Customization
The script can be easily modified to:

Change search parameters: Modify the URL in all_url.py to target different property filters

Add new data fields: Update the extraction functions to capture additional property information

Adjust scraping speed: Modify the wait times between requests

Enable headless mode: Set headless=True for browser automation without a visible window

📊 Output Files
zimmoweb_links.txt: Contains all unique property URLs, one per line

zimmoweb_data.csv: Structured data containing all extracted property information

🤝 Contributing
Feel free to fork this project and submit pull requests for:

Additional data fields

Improved error handling

Performance optimizations

Support for other real estate websites

📄 License
This project is provided for educational and research purposes. Please use responsibly and in compliance with Zimmo.be's terms of service.

Disclaimer: This tool is intended for educational purposes only. Users are responsible for ensuring their compliance with applicable laws and website terms of service.

