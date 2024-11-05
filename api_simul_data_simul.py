from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Simulate data functions
def get_temperature():
    return round(random.uniform(15.0, 30.0), 2)  # Celsius

def get_humidity():
    return round(random.uniform(30.0, 90.0), 2)  # Percentage

def get_air_pressure():
    return round(random.uniform(980.0, 1050.0), 2)  # hPa

def get_dew_point():
    return round(random.uniform(5.0, 20.0), 2)  # Celsius

# Define routes for each data point
@app.route('/temperature', methods=['GET'])
def temperature():
    return jsonify(temperature=get_temperature(), timestamp=time.time())

@app.route('/humidity', methods=['GET'])
def humidity():
    return jsonify(humidity=get_humidity(), timestamp=time.time())

@app.route('/air_pressure', methods=['GET'])
def air_pressure():
    return jsonify(air_pressure=get_air_pressure(), timestamp=time.time())

@app.route('/dew_point', methods=['GET'])
def dew_point():
    return jsonify(dewpoint=get_dew_point(), timestamp=time.time())

# Combined endpoint
@app.route('/all', methods=['GET'])
def all_data():
    return jsonify(
        temperature=get_temperature(),
        humidity=get_humidity(),
        air_pressure=get_air_pressure(),
        dew_point=get_dew_point(),
        timestamp=time.time()
    )

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
