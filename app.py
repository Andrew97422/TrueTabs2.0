from flask import Flask, render_template, jsonify, request
import prognose  # Ваш модуль прогнозирования

app = Flask(__name__)


@app.route('/run-forecast', methods=['GET'])
def run_forecast():
    #historical_table_id = request.args.get('historical_table_id', type=str)
    #historical_view_id = request.args.get('historical_view_id', type=str)

    #forecast_table_id = request.args.get('forecast_table_id', type=str)
    #forecast_view_id = request.args.get('forecast_view_id', type=str)

    historical_table_id = 'dstp2cytHJcQAMDAxH'
    historical_view_id = 'viwofal30sRHo'

    forecast_table_id = 'dstF8u8naoVHdJEGYc'
    forecast_view_id = 'viwka5FrofH19'

    #if not all([historical_table_id, historical_view_id, forecast_table_id, forecast_view_id]):
    #    return jsonify({"error": "Missing one or more parameters"}), 400

    try:
        prognose.main_process(historical_table_id, historical_view_id, forecast_table_id, forecast_view_id, 12)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
