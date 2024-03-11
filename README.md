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
