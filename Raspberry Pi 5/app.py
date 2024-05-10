import csv
from flask import jsonify, Flask
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app, origins='*')
swagger = Swagger(app)

# Read the last row from CSV file which is considered the latest sensor data
def read_latest_sensor_data(csv_file_path):
    with open(csv_file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        last_row = None
        for row in csv_reader:
            last_row = row
        return last_row

# Websocket behavior definition for sending data directly to the website
@app.route('/api/sensor-data', methods=['GET'])
def sensor_data():
    """
    Get the latest sensor data
    ---
    responses:
      200:
        description: The latest sensor data
        schema:
          type: array
          items:
            type: string
    """
    data = read_latest_sensor_data("/home/kali/Documents/patex-raspi5-mod/basic.csv")
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
