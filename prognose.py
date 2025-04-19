import api_module

TABLE_ID = "your_table_id_here"
VIEW_ID = "your_view_id_here"


def demand_forecasting(data):
    """
    Прогнозирование спроса на товары.
    """
    forecast_records = []
    for record in data:
        fields = record.get("fields", {})
        forecast_record = {
            "fields": {
                "date": fields["date"],
                "id_good": fields["id_good"] if "id_good" in fields else "",
                "id_warehouse": fields["id_warehouse"] if "id_warehouse" in fields else "",
                "forecast_ordered": fields["forecast_ordered"] * 1.1 if "forecast_ordered" in fields else "",
                "forecast_shipped": fields["forecast_shipped"] * 0.9 if "forecast_shipped" in fields else "",
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


def main_process(historical_table_id, historical_view_id, forecast_table_id, forecast_view_id):
    historical_data = fetch_historical_data(historical_table_id, historical_view_id)
    forecast = demand_forecasting(historical_data)
    transmit_forecast_data(forecast, forecast_table_id, forecast_view_id)
    print("Main process completed.")