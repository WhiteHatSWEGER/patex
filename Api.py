# api.py
from flask import jsonify
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# Initialize InfluxDB client
client = InfluxDBClient(url="http://localhost:8086", token="your-token", org="your-org")
write_api = client.write_api(write_options=SYNCHRONOUS)

app = Flask(__name__)

@app.route('/api/event-log', methods=['GET'])
def get_event_log():
    # Query InfluxDB for event log data
    query = "from(bucket: \"your-bucket\") |> range(start: -1h)"
    result = client.query_api().query(query)

    # Convert query result to a list of dictionaries
    event_log = []
    for table in result:
        for record in table.records:
            event_log.append({
                "measurement": record.name,
                "timestamp": record.time,
                "fields": record.fields
            })

    return jsonify(event_log)

@app.route('/api/event-log', methods=['POST'])
def add_event_log():
    # Parse JSON data from request
    data = request.get_json()

    # Create a point for each event log entry
    points = []
    for measurement in data:
        point = Point(measurement) \
            .tag("event_id", measurement) \
            .field("message", data[measurement]) \
            .time(datetime.utcnow(), write_precision="s")
        points.append(point)

    # Write points to InfluxDB
    write_api.write(bucket="your-bucket", record=points)

    return jsonify({"message": "Event log data received"})

if __name__ == '__main__':
    app.run(debug=True)
