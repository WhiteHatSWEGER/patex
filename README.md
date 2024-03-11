# patex

html - functions

Sie haben in Ihrem Code zwei separate Funktionen zum Abrufen und Aktualisieren von Daten verwendet: fetchEventData() und fetchSensorData(). Die fetchEventData()-Funktion gibt Dummy-Daten zurück, während die fetchSensorData()-Funktion die tatsächlichen Sensordaten abruft.

Um die Ereignisdaten in der Tabelle anzuzeigen, wird die Funktion updateEventTable() aufgerufen. Diese Funktion erstellt eine neue Zeile für jedes Ereignis in den abgerufenen Daten und fügt sie der Tabelle hinzu.

Um die Sensordaten in der Tabelle anzuzeigen, wird die Funktion updateTable() aufgerufen. Diese Funktion erstellt eine neue Zeile für jedes Sensordatum in den abgerufenen Daten und fügt sie der Tabelle hinzu.

Die Funktion updateTable() wird alle 5 Sekunden mit der setInterval()-Funktion aktualisiert, um die neuesten Sensordaten anzuzeigen.

Die fetchSensorData()-Funktion verwendet die fetch()-Methode, um die Sensordaten von einer JSON-Datei namens sensor-data.json abzurufen. Die fetch()-Methode gibt eine Promise zurück, die beim Abschluss der Anfrage aufgelöst wird. Die await-Anweisung wird verwendet, um auf die Auflösung der Promise zu warten, bevor die Daten verarbeitet werden.

Die fetchEventData()-Funktion gibt Dummy-Daten zurück, die als Array von Objekten dargestellt sind. Jedes Objekt enthält die Eigenschaften level, timestamp, und message.

Die updateEventTable()-Funktion erstellt eine neue Zeile für jedes Ereignis in den abgerufenen Daten und fügt sie der Tabelle hinzu. Die Zeile enthält drei Zellen: eine für die Ereignisstufe, eine für den Zeitstempel und eine für die Ereignismeldung. Die Zellen werden mit den entsprechenden Eigenschaften aus dem Ereignisobjekt gefüllt.

Die updateTable()-Funktion erstellt eine neue Zeile für jedes Sensordatum in den abgerufenen Daten und fügt sie der Tabelle hinzu. Die Zeile enthält vier Zellen: eine für den Sensornamen, eine für den Wert, eine für die Einheit und eine für die Zeit. Die Zellen werden mit den entsprechenden Eigenschaften aus dem Sensordatumobjekt gefüllt.

Der Code enthält auch einen Chart, der die Stundendaten darstellt. Der Chart wird mit der Chart.js-Bibliothek erstellt. Die hourly-data-chart-ID wird verwendet, um den Chart-Bereich im HTML-Dokument zu identifizieren. Die Chartdaten werden direkt in der data-Eigenschaft des Chart-Objekts angegeben.

Die updateTable()-Funktion wird alle 5 Sekunden mit der setInterval()-Funktion aktualisiert, um die neuesten Sensordaten anzuzeigen.

Die fetchSensorData()-Funktion verwendet die fetch()-Methode, um die Sensordaten von einer JSON-Datei namens sensor-data.json abzurufen. Die fetch()-Methode gibt eine Promise zurück, die beim Abschluss der Anfrage aufgelöst wird. Die await-Anweisung wird verwendet, um auf die Auflösung der Promise zu warten, bevor die Daten verarbeitet werden.

Die fetchEventData()-Funktion gibt Dummy-Daten zurück, die als Array von Objekten dargestellt sind. Jedes Objekt enthält die Eigenschaften level, timestamp, und message.

Die updateEventTable()-Funktion erstellt eine neue Zeile für jedes Ereignis in den abgerufenen Daten und fügt sie der Tabelle hinzu. Die Zeile enthält drei Zellen: eine für die Ereignisstufe, eine für den Zeitstempel und eine für die Ereignismeldung. Die Zellen werden mit den entsprechenden Eigenschaften aus dem Ereignisobjekt gefüllt.




######################################################################################################################################################

To run your Flask application on a Raspberry Pi, you should follow these steps:

    Install the latest version of Raspberry Pi OS (previously called Raspbian) on your Raspberry Pi.

    Connect to your Raspberry Pi via SSH or directly using a keyboard and monitor.

    Update your Raspberry Pi's package list and upgrade the system packages:

sudo apt update

sudo apt upgrade

Install Python 3 and pip:

sudo apt install python3 python3-pip

Create a new directory for your project:

mkdir my_project

cd my_project

Create a new Python file for your Flask application, e.g., app.py.

Save your updated HTML code in a file named index.html in a folder called templates.

Save your JSON data in a file named sensor-data.json in a folder called static.

In your app.py, create a Flask app instance and set up a route for the main page:

python

from flask import Flask, render_template

import json


app = Flask(__name__)


@app.route('/')

def home():

    with open('static/sensor-data.json') as f:

        sensor_data = json.load(f)

    return render_template('index.html', sensor_data=sensor_data)


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')

Install the required packages:

pip3 install flask chart.js

Run your Flask application:

    python3 app.py

Now your Flask application should be running on your Raspberry Pi, and you can access it using a web browser on the same network by entering the Raspberry Pi's IP address in the address bar.

Make sure to replace the file paths in the app.py example with the actual paths on your Raspberry Pi.
