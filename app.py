# app.py
import sqlite3
import json
from flask import Flask, render_template

# Connect to the local LibreOffice Base database
def get_db_connection():
    conn = sqlite3.connect('sensor_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Connect to the local LibreOffice Base database
def get_event_log_connection():
    conn = sqlite3.connect('event_log.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    sensor_data = [dict(row) for row in conn.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 100')]
    conn.close()

    conn = get_event_log_connection()
    event_log = [dict(row) for row in conn.execute('SELECT * FROM event_log ORDER BY timestamp DESC LIMIT 100')]
    conn.close()

    return render_template('index.html', sensor_data=sensor_data, event_log=event_log)

if __name__ == '__main__':
    app.run(debug=True)
