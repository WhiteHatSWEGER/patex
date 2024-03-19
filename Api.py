# api.py
import sqlite3
import json
from flask import Flask, jsonify
# Connect to the local LibreOffice Base database
def get_db_connection():
    conn = sqlite3.connect('event_log.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/api/event-log', methods=['GET'])
def get_event_log():
    conn = get_db_connection()
    event_log = [dict(row) for row in conn.execute('SELECT * FROM event_log ORDER BY timestamp DESC')]
    conn.close()
    return jsonify(event_log)

@app.route('/api/event-log', methods=['POST'])
def add_event_log():
    # Parse JSON data from request
    data = request.get_json()

    # Connect to the local LibreOffice Base database
    conn = get_db_connection()

    # Insert event log data into the local LibreOffice Base database
    for measurement in data:
        conn.execute('INSERT INTO event_log (measurement, timestamp, message) VALUES (?, ?, ?)',
                     (measurement, datetime.now(), data[measurement]))
    conn.commit()
    conn.close()

    return jsonify({"message": "Event log data received"})

if __name__ == '__main__':
    app.run(debug=True)
