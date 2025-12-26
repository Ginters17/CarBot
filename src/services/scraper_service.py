import os
import requests
import re
from bs4 import BeautifulSoup
from config.config_reader import SS_BASE_URL, SS_LISTINGS_URL, CAR_FILTER_MAX_PRICE, CAR_FILTER_MIN_PRICE, CAR_FILTER_MIN_YEAR, CAR_FILTER_TRANSMISSION
from services.scraper_storage_service import load_viewed_listings, save_viewed_listings

BUCKET_NAME = "ss-scraper"
SCRAPED_LINKS_FILE = "car_scraped_links.txt"

def getCarListings():
    page_num = 1
    end_reached = False
    all_new_links = set()

    session, headers = createScraperSession()

    while not end_reached:
        url = getPageUrl(page_num)

        response = session.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        scraped_links = load_viewed_listings(BUCKET_NAME, SCRAPED_LINKS_FILE)
        new_links = []

        for row in soup.select("tr[id^=tr_]"):
            a_tag = row.select_one("a[href^='/msg/']")
            if a_tag:
                href = a_tag.get("href")
                full_url = SS_BASE_URL + href
                if full_url in scraped_links:
                    end_reached = True
                    break
                else:
                    new_links.append(full_url)

        all_new_links.update(new_links)

        if end_reached or page_num >= 3: # Safe guard lol
            break

        page_num += 1

    # When only few links found append to already scraped links, otherwise overwrite all scraped links.
    # Because if overwrite with e.g. 1 link and it gets removed then will incorrectly scrape all pages.
    if len(all_new_links) < 3:
        save_viewed_listings(all_new_links, BUCKET_NAME, SCRAPED_LINKS_FILE, "a")
    else:
        save_viewed_listings(all_new_links, BUCKET_NAME, SCRAPED_LINKS_FILE, "w")

    enrichedListings = [enrichLink(link) for link in all_new_links]
    return list(enrichedListings)

def getPageUrl(page_num):
    if page_num == 1:
        return SS_LISTINGS_URL
    else:
        base_url = SS_LISTINGS_URL.rsplit('/', 1)[0]
        return f"{base_url}/page{page_num}.html"

def enrichLink(link):
    response = requests.get(link)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    price = extractPrice(soup)
    image_url = extractImageUrl(soup)
    make = extractMake(link)
    model = extractModel(link)
    year = extractYear(soup)
    motor = extractMotor(soup)
    transmission = extractTransmission(soup)
    mileage = extractMileage(soup)
    ta = extractTA(soup)

    return {
        "link": link,
        "price": price,
        "imageUrl": image_url,
        "make": make,
        "model": model,
        "year": year,
        "motor": motor,
        "transmission": transmission,
        "mileage": mileage,
        "ta": ta
    }

def extractPrice(soup):
    el = soup.select_one("#tdo_8")
    return el.get_text(strip=True) if el else None

def extractMake(link):
    match = re.search(r"/transport/cars/([^/]+)/([^/]+)/", link)
    return match.group(1) if match else None

def extractModel(link):
    match = re.search(r"/transport/cars/([^/]+)/([^/]+)/", link)
    return match.group(2) if match else None

def extractYear(soup):
    el = soup.select_one("#tdo_18")
    return el.get_text(strip=True) if el else None

def extractMotor(soup):
    el = soup.select_one("#tdo_15")
    return el.get_text(strip=True) if el else None

def extractTransmission(soup):
    el = soup.select_one("#tdo_35")
    return el.get_text(strip=True) if el else None

def extractMileage(soup):
    el = soup.select_one("#tdo_16")
    if not el:
        return None
    return int(el.get_text(strip=True).replace(" ", ""))

def extractTA(soup):
    el = soup.select_one("#tdo_223")
    return el.get_text(strip=True) if el else None

def extractImageUrl(soup):    
    img_tag = soup.select_one("img.pic_thumbnail.isfoto")
    if img_tag and img_tag.get("src"):
        img_url = img_tag["src"]
        if img_url.startswith("/"):
            img_url = "https://www.ss.com" + img_url
        return img_url
    return None

def createScraperSession():
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.ss.com/lv/transport/cars/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'lv,en;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    # Visit the main page to establish session
    session.get(SS_LISTINGS_URL, headers=headers)
    
    # Prepare search data
    search_data = {
        'topt[8][min]': CAR_FILTER_MIN_PRICE,   # Price min (field ID 8)
        'topt[8][max]': CAR_FILTER_MAX_PRICE,   # Price max
        'topt[18][min]': CAR_FILTER_MIN_YEAR,  # Year min (field ID 18)
        'topt[18][max]': '',  # Year max
        'topt[15][min]': '',  # Engine size min (field ID 15)
        'topt[15][max]': '',  # Engine size max
        'opt[34]': '',        # Make (field ID 34)
        'opt[35]': CAR_FILTER_TRANSMISSION,        # Transmission (field ID 35)
        'opt[32]': '',        # Body type (field ID 32)
        'opt[17]': '',        # Fuel type (field ID 17)
    }
    
    # Submit the filter form to create session state
    session.post(
        SS_LISTINGS_URL,
        headers=headers,
        data=search_data,
        allow_redirects=True
    )
    
    return session, headers