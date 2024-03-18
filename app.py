# app.py
from flask import Flask, jsonify
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# Initialize InfluxDB client
client = InfluxDBClient(url="http://localhost:8086", token="your-token", org="your-org")
write_api = client.write_api(write_options=SYNCHRONOUS)

app = Flask(__name__)

@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    # Query InfluxDB for sensor data
    query = "from(bucket: \"your-bucket\") |> range(start: -1h)"
    result = client.query_api().query(query)

    # Convert query result to a list of dictionaries
    sensor_data = []
    for table in result:
        for record in table.records:
            sensor_data.append({
                "measurement": record.name,
                "timestamp": record.time,
                "value": record.value,
                "fields": record.fields
            })

    return jsonify(sensor_data)

@app.route('/api/sensor-data', methods=['POST'])
def add_sensor_data():
    # Parse JSON data from request
    data = request.get_json()

    # Create a point for each sensor measurement
    points = []
    for measurement in data:
        point = Point(measurement) \
            .tag("sensor_id", measurement) \
            .field("value", data[measurement]) \
            .time(datetime.utcnow(), write_precision="s")
        points.append(point)

    # Write points to InfluxDB
    write_api.write(bucket="your-bucket", record=points)

    return jsonify({"message": "Sensor data received"})

if __name__ == '__main__':
    app.run(debug=True)
