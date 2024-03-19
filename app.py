# app.py
import sqlite3
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to the local LibreOffice Base database
def get_db_connection():
    conn = sqlite3.connect('sensor_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    conn = get_db_connection()
    sensor_data = []
    for row in conn.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC'):
        sensor_data.append({
            "measurement": row['measurement'],
            "timestamp": row['timestamp'],
            "value": row['value'],
            "fields": dict(row)
        })
    conn.close()
    return jsonify(sensor_data)

@app.route('/api/sensor-data', methods=['POST'])
def add_sensor_data():
    conn = get_db_connection()
    data = request.get_json()
    for measurement in data:
        conn.execute('INSERT INTO sensor_data (measurement, timestamp, value) VALUES (?, ?, ?)',
                     (measurement, datetime.now(), data[measurement]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Sensor data received"})

if __name__ == '__main__':
    app.run(debug=True)
