import json
import time
from datetime import datetime
import requests
import RPi.GPIO as GPIO


# Funktion zum Lesen der Sensorwerte
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.IN)
GPIO.setup(12,GPIO.OUT)
GPIO.output(12,False)

while True:
    button_state=GPIO.input(12)
    if button_state == False:
        GPIO.output(12,True)
    while GPIO.input(14) == False:
        time.sleep(0.2)
    else:
        GPIO.output(12,False)
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
