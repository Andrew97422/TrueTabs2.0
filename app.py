from flask import Flask, render_template, jsonify, request
import logging
import prognose  # Ваш модуль прогнозирования
import api_module  # импортировать модуль API

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    # Отображение HTML страницы
    return render_template('index.html')

@app.route('/fetch-and-forecast', methods=['GET'])
def fetch_and_forecast():
    historical_table_id = request.args.get('historical_table_id', 'dstp2cytHJcQAMDAxH')
    historical_view_id = request.args.get('historical_view_id', 'viwofal30sRHo')

    try:
        # Получение исторических данных
        historical_data = api_module.get_records(historical_table_id, historical_view_id)['data']['records']
        logging.info("Historical data fetched successfully.")

        # Выполнение прогноза
        forecast_data = prognose.demand_forecasting(historical_data, future_months=12)
        logging.info("Forecasting completed.")

        return jsonify(forecast_data), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/submit-forecast', methods=['POST'])
def submit_forecast():
    forecast_table_id = request.json.get('forecast_table_id', 'dstF8u8naoVHdJEGYc')
    forecast_view_id = request.json.get('forecast_view_id', 'viwka5FrofH19')
    forecast_data = request.json.get('forecast_data', [])

    try:
        # Передача данных прогноза
        api_module.post_records(forecast_table_id, forecast_data, forecast_view_id)
        logging.info("Forecast data transmitted successfully.")
        return jsonify({"success": True}), 200
    except Exception as e:
        logging.error(f"An error occurred during forecast submission: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
