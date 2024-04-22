from flask import Flask, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)


@app.route('/api/read-sensor-csv', methods=['GET'])
def read_sensor_csv():
    try:
        # Assuming the CSV file is in the same directory as this script
        df = pd.read_csv('sensor_data.csv')
        # Convert the DataFrame to a list of dictionaries for easy JSON serialization
        data = df.to_dict(orient='records')
        # Convert strings to datetime objects
        for entry in data:
            entry['timestamp'] = datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S')
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
