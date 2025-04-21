import requests

TELEGRAM_BOT_TOKEN = "7896268006:AAEsUer5UjVRAjC7atzBj2Lr4qEu3LSZDuE"
CHAT_ID = "1134443964"
MESSAGE_TEXT = "Test message from bot"

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": MESSAGE_TEXT
}

response = requests.post(url, data=payload)
print(response.json())
