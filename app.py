from flask import Flask, render_template, jsonify, request
import prognose  # Ваш модуль прогнозирования

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run-forecast', methods=['GET'])
def run_forecast():
    # Получение параметров для исторических данных
    historical_table_id = request.args.get('historical_table_id', type=str)
    historical_view_id = request.args.get('historical_view_id', type=str)

    # Получение параметров для данных прогноза
    forecast_table_id = request.args.get('forecast_table_id', type=str)
    forecast_view_id = request.args.get('forecast_view_id', type=str)

    # historical_table_id = 'dstp2cytHJcQAMDAxH'
    # historical_view_id = 'viwofal30sRHo'

    # forecast_table_id = 'dstF8u8naoVHdJEGYc'
    # forecast_view_id = 'viwka5FrofH19'

    # Проверка наличия всех необходимых параметров
    if not all([historical_table_id, historical_view_id, forecast_table_id, forecast_view_id]):
        return jsonify({"error": "Missing one or more parameters"}), 400

    try:
        # Запуск основного процесса с переданными параметрами
        result = prognose.main_process(historical_table_id, historical_view_id, forecast_table_id, forecast_view_id)
        print(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

#historical_table_id = 'dstp2cytHJcQAMDAxH'
#historical_view_id = 'viwofal30sRHo'

#forecast_table_id = 'dstF8u8naoVHdJEGYc'
#forecast_view_id = 'viwka5FrofH19'