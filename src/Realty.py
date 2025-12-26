from services.telegram_notification_service import sendTelegramMessage
from services.scraper_service import getCarListings
from services.smart_filter_service import filterListings

def main():
    print("🔍 Scraping car listings...")
    listings = getCarListings()
    print(f"Scraped {len(listings)} new listings.")
    filteredListings = filterListings(listings)
    print(f"Found {len(filteredListings)} new listings with matching criteria.")
    
    for listing in filteredListings:
        sendTelegramMessage(listing)

if __name__ == "__main__":
    main()
