import requests
import json
import time
import csv
import websocket
import threading

# Endpoint and WebSocket server configurations
API_ENDPOINT = 'http://laptop-ip-address:5000/api/sensor-data'
WEBSOCKET_SERVER = 'ws://laptop-ip-address:5001/'


# Read the last row from CSV file which is considered the latest sensor data
def read_latest_sensor_data(csv_file_path):
    with open(csv_file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        last_row = None
        for row in csv_reader:
            last_row = row
        return last_row


# Websocket behavior definition for sending data directly to the website
def on_open(ws):
    def run(*args):
        csv_file_path = 'sensor_readings.csv'  # CSV file path on the Raspberry Pi
        while True:
            last_row = read_latest_sensor_data(csv_file_path)
            if last_row:
                # Create the data payload in the expected format
                # Assuming the CSV has columns: timestamp, temperature, humidity
                sensor_data = {
                    'timestamp': last_row[0],
                    'sensors': [
                        {'id': 'temperature', 'value': float(last_row[1])},
                        {'id': 'humidity', 'value': float(last_row[2])}
                    ]
                }

                # Send data to the Flask API for storage
                response = requests.post(API_ENDPOINT, json=sensor_data)
                if response.status_code == 201:
                    print("Data sent successfully to server")
                else:
                    print("Failed to send data: ", response.content)

                # Directly send data to the website via WebSocket for real-time updates
                ws.send(json.dumps(sensor_data))
            else:
                print("No data found in the CSV file.")

            time.sleep(60)  # Send data every 60 seconds

    threading.Thread(target=run).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WEBSOCKET_SERVER, on_open=on_open)
    ws.run_forever()
