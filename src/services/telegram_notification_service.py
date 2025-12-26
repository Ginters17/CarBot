import requests
from config.config_reader import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_SERVICE_IMPL

def sendTelegramMessage(car):
    message = (
        f"🚗 *New Car Found!*\n"
        f"Model: *{car['make']}* *{car['model']}* \n"
        f"Price: *{car['price']}*\n"
        f"Mileage: *{car['mileage']} km*\n"
        f"Year: *{car['year']}*\n"
        f"TA: *{car['ta']}*\n"
        f"Motor: *{car['motor']}*\n"
        f"🔗 [View Listing]({car['link']})"
    )
    
    if TELEGRAM_SERVICE_IMPL == "real":
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "photo": car['imageUrl'],
            "caption": message,
            "parse_mode": "Markdown"
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            print(f"Successfully sent telegram notification with listing to {'chat (local testing)' if int(TELEGRAM_CHAT_ID) > 0 else 'channel (prod)'}")
        else:
            print(f"Failed to send telegram notification. Error code {response.status_code}, {response.text}")

    else:
        print("Mock telegram service used")
