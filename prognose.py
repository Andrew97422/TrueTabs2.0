from datetime import datetime
from random import random, randint

from dateutil.relativedelta import relativedelta
import api_module

TABLE_ID = "your_table_id_here"
VIEW_ID = "your_view_id_here"


def demand_forecasting(data, future_months=1):
    """
    Создает прогноз спроса, начиная с месяца, следующего за последним в исторических данных.
    """
    forecast_records = []

    # Найти максимальную дату в исторических данных
    max_date = None
    for record in data:
        fields = record.get("fields", {})
        timestamp = fields["date"] / 1000
        current_date = datetime.fromtimestamp(timestamp)
        if max_date is None or current_date > max_date:
            max_date = current_date

    print(f"Max date in historical data: {max_date.strftime('%Y-%m-%d')}")

    # Начнем прогноз с месяца, следующего за последним месяцем в данных
    if max_date is not None:
        start_date = max_date + relativedelta(months=1)

        for month in range(future_months):
            record = data[randint(0, len(data) - 1)]

            fields = record.get("fields", {})
            id_good = fields.get("id_good", "")
            id_warehouse = fields.get("id_warehouse", "")

            forecast_date = start_date + relativedelta(months=month)
            forecast_date_millis = int(forecast_date.timestamp() * 1000)

            forecast_record = {
                "fields": {
                    "date": forecast_date_millis,
                    "id_good": id_good,
                    "id_warehouse": id_warehouse,
                    "forecast_ordered": fields.get("units_ordered", 0) * 1.1,
                    "forecast_shipped": fields.get("units_shipped", 0) * 0.9,
                }
            }
            forecast_records.append(forecast_record)

    result = {"records": forecast_records, "fieldKey": "name"}
    return result


def fetch_historical_data(historical_table_id, historical_view_id):
    """
    Получение исторических данных из API
    """
    data = api_module.get_records(historical_table_id, historical_view_id)
    return data['data']['records']


def transmit_forecast_data(forecast, forecast_table_id, forecast_view_id):
    """
    Передача данных прогноза в API
    """
    api_module.post_records(forecast_table_id, forecast['records'], forecast_view_id)


def main_process(historical_table_id, historical_view_id, forecast_table_id, forecast_view_id, future_months=1):
    historical_data = fetch_historical_data(historical_table_id, historical_view_id)
    forecast = demand_forecasting(historical_data, future_months)
    transmit_forecast_data(forecast, forecast_table_id, forecast_view_id)
    print("Main process completed.")