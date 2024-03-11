from flask import Flask, render_template
import json
import time

app = Flask(__name__)

import json
import time
import requests

# ...

def send_sensor_data():
    sensor_data = {
        "id": 1,
        "timestamp": int(time.time()),
        "sensor_values": [
            {
                "sensor_name": "Sensor1",
                "value": 10,
                "unit": "unit1"
            },
            # ... Add more sensor data here
        ]
    }
    response = requests.post(
        "http://localhost:5000/sensor-data",  # Replace with your Flask app's URL
        json=sensor_data
    )
    if response.status_code == 200:
        print("Sensor data sent successfully")
    else:
        print(f"Error sending sensor data: {response.status_code} - {response.text}")

# Call the send_sensor_data function periodically
while True:
    send_sensor_data()
    time.sleep(5)

@app.route('/api/sensors')
def get_sensors():
    api = Api("path/to/sensor/data")  # Replace with the path to your sensor data
    return jsonify(api.get_sensors())

@app.route('/api/sensor-data', methods=['POST'])
def add_sensor_data():
    api = Api("path/to/sensor/data")  # Replace with the path to your sensor data
    data = request.get_json()
    sensor_id = data.get('sensor_id')
    sensor_data = data.get('sensor_data')
    return jsonify(api.add_sensor_data(sensor_id, sensor_data))

@app.route('/')
def home():
    with open('static/sensor-data.json') as f:
        sensor_data = json.load(f)
    return render_template('index.html', sensor_data=sensor_data)

@app.route('/data')
def get_data():
    with open('static/sensor-data.json') as f:
        sensor_data = json.load(f)
    return json.dumps(sensor_data)

@app.route('/sensor-data', methods=['POST'])

def handle_sensor_data():
    data = request.get_json()
    id = data.get('id')
    timestamp = data.get('timestamp')
    sensor_values = data.get('sensor_values', [])


    # Process the sensor data here
    # Store it in a database or use it as needed

    return jsonify({'message': 'Sensor data received'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
