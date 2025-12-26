from dotenv import load_dotenv
import os

load_dotenv()

def get_env_list(name, default=""):
    return [x.strip().lower() for x in os.getenv(name, default).split(",") if x.strip()]

def get_env_int(name):
    return int(os.getenv(name))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_SERVICE_IMPL = os.getenv("TELEGRAM_SERVICE_IMPL", "mock")
SS_BASE_URL = os.getenv("SS_BASE_URL")
SS_LISTINGS_URL = os.getenv("SS_LISTINGS_URL")
GCP_SERVICE_ACCOUNT_KEY = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
GCS_SERVICE_IMPL = os.getenv("GCS_SERVICE_IMPL")
CAR_FILTER_MAKE = get_env_list("CAR_FILTER_MAKE")
CAR_FILTER_MODEL = get_env_list("CAR_FILTER_MODEL")
CAR_FILTER_MAX_PRICE= get_env_int("CAR_FILTER_MAX_PRICE")
CAR_FILTER_MIN_PRICE= get_env_int("CAR_FILTER_MIN_PRICE")
CAR_FILTER_MIN_YEAR= get_env_int("CAR_FILTER_MIN_YEAR")
CAR_FILTER_TRANSMISSION= get_env_int("CAR_FILTER_TRANSMISSION")