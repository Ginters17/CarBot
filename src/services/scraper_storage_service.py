import os
import json
from google.cloud import storage
from google.oauth2 import service_account
from config.config_reader import GCP_SERVICE_ACCOUNT_KEY, GCS_SERVICE_IMPL

# Initialize and return Google Cloud Services client
def get_gcs_client():
        credentials_info = json.loads(GCP_SERVICE_ACCOUNT_KEY)
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        return storage.Client(credentials=credentials)

# Download and return viewed listings from GCS as a set
def load_viewed_listings(bucket_name, file_name="car_scraped_links.txt"):
    if(GCS_SERVICE_IMPL == "mock"):
        print("Mock GCS service used")
        return get_mock_listings()
    
    try:
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        if blob.exists():
            content = blob.download_as_text()
            listings = set(content.strip().split('\n')) if content.strip() else set()
            return listings
        else:
            return set()
    except Exception as e:
        print(f"Error loading viewed listings: {e}")
        return set()

# Save links to GCS with append or overwrite mode
#   mode="a" -> append to existing links
#   mode="w" -> overwrite all links
def save_viewed_listings(new_links, bucket_name, file_name="car_scraped_links.txt", mode="a"):
    if(GCS_SERVICE_IMPL == "mock"):
        return
    
    try:
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        
        if mode == "w":
            content = '\n'.join(new_links)
        else:
            existing_links = load_viewed_listings(bucket_name, file_name)
            existing_links.update(new_links)
            content = '\n'.join(existing_links)
        
        blob.upload_from_string(content)
        
    except Exception as e:
        print(f"Error saving viewed listings: {e}")

def get_mock_listings():
    return {
        "https://www.ss.com/msg/lv/transport/cars/audi/a6/gphim.html",
        "https://www.ss.com/msg/lv/transport/cars/audi/a6/chojb.html",
        "https://www.ss.com/msg/lv/transport/cars/audi/a6/aopok.html",
        "https://www.ss.com/msg/lv/transport/cars/volkswagen/touran/bcxxnx.html",
        "https://www.ss.com/msg/lv/transport/cars/volkswagen/touareg/bienfj.html",
        "https://www.ss.com/msg/lv/transport/cars/bmw/x3/dhijh.html",
        "https://www.ss.com/msg/lv/transport/cars/volkswagen/golf-4/bdfbhm.html"
    }