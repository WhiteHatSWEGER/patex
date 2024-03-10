import json
import time
from datetime import datetime
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
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename = "sensor_data.json"
    with open(filename, 'a') as file:
        json.dump({"timestamp": timestamp, "data": data}, file)
        file.write('\n')

# Hauptfunktion zum Ausführen des Programms
def main():
    while True:
        sensor_data = read_sensor_values()
        save_sensor_data_to_json(sensor_data)
        print("Sensorwerte gespeichert:", sensor_data)
        time.sleep(5) # Intervall zum Lesen und Speichern der Sensorwerte (hier 5 Sekunden)

if __name__ == "__main__":
    main()
