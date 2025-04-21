import requests
from api_module import get_records
from apscheduler.schedulers.background import BackgroundScheduler
import time

TELEGRAM_BOT_TOKEN = "7896268006:AAEsUer5UjVRAjC7atzBj2Lr4qEu3LSZDuE"
CHAT_ID = "1134443964"


def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)
        response_data = response.json()

        if response_data.get("ok"):  # Проверяем ответ от Telegram API
            print(f"Telegram alert sent: {message}")
        else:
            print(f"Failed to send Telegram alert: {response_data}")

    except Exception as e:
        print(f"Exception occurred: {e}")


def check_stock_levels(table_id, view_id):
    data = get_records(table_id, view_id)
    print(f"Data from table {table_id}: {data}")

    for record in data['data']['records']:
        fields = record.get("fields", {})
        warehouse_id = fields.get("id_warehouse", "Unknown")
        opening_stock = fields.get("opening_stock", 0)
        closing_stock = fields.get("closing_stock", 0)
        max_capacity = fields.get("max_capacity", 40000)

        # Логика дефицита
        if closing_stock < 0.1 * opening_stock:
            message = (
                f"❗ Дефицит запасов на складе '{warehouse_id}': "
                f"{closing_stock} единиц (менее 10% от начального значения)."
            )
            print(message)
            send_telegram_alert(message)

        # Логика профицита
        if closing_stock > max_capacity:
            message = (
                f"⚠️ Профицит запасов на складе (ID: {warehouse_id}): "
                f"{closing_stock} единиц (более максимальной вместимости)."
            )
            print(message)
            send_telegram_alert(message)


def schedule_stock_check():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_stock_levels,
        'interval',
        minutes=1,
        args=["dst1ZZZ5yvTFxgnc6K", "viwfWEny8fQc9"]
    )
    scheduler.start()


if __name__ == "__main__":
    schedule_stock_check()
    try:
        while True:
            time.sleep(1)  # Сон в 1 секунду, чтобы не нагружать процессор
    except (KeyboardInterrupt, SystemExit):
        print("Программа остановлена.")
