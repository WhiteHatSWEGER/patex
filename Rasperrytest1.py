import json
import time
from datetime import datetime
import requests
import random

# Funktion zum Lesen der Sensorwerte (Dummy-Daten für Testzwecke)
def read_sensor_values():
    # Hier könnten Sie Ihren tatsächlichen Code einfügen, um die Sensorwerte auszulesen
    # Für Testzwecke generieren wir hier zufällige Dummy-Daten
    co = round(random.uniform(0, 1), 2) # Kohlenmonoxid in ppm
    no2 = round(random.uniform(0, 1), 2) # Stickstoffdioxid in ppm
    so2 = round(random.uniform(0, 1), 2) # Schwefeldioxid in ppm
    pm25 = round(random.uniform(0, 1), 2) # Feinstaub PM2.5 in µg/m^3
    return {"CO": co, "NO2": no2, "SO2": so2, "PM2.5": pm25}

# Funktion zum Speichern der Sensorwerte in eine JSON-Datei
def save_sensor_data_to_json(data):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"sensor_data_{timestamp}.json"
    with open(filename, 'w') as file:
        json.dump(data, file)

# Funktion zum Senden der Sensorwerte an eine Webseite
def send_data_to_webpage(data):
    url = "http://example.com/receive_data"  # Ersetzen Sie "http://example.com/receive_data" durch die tatsächliche URL Ihrer Webseite
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Daten erfolgreich an die Webseite gesendet.")
    else:
        print("Fehler beim Senden der Daten an die Webseite:", response.text)

# Hauptfunktion zum Ausführen des Programms
def main():
    while True:
        sensor_data = read_sensor_values()
        save_sensor_data_to_json(sensor_data)
        print("Sensorwerte gespeichert:", sensor_data)
        send_data_to_webpage(sensor_data)
        time.sleep(60) # Intervall zum Lesen, Speichern und Senden der Sensorwerte (hier 60 Sekunden)

if __name__ == "__main__":
    main()
