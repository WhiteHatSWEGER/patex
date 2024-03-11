import json
import random
import time
import RPi.GPIO as GPIO

# Set up GPIO pins here
# Replace the pin numbers and sensor reading code with your actual setup

def read_sensor_data():
    sensor_data = {}
    for i in range(1, 10):
        sensor_name = f"Sensor{i}"
        measure = "Measure_{}".format(i)
        value = random.randint(0, 100)
        critical = random.choice([True, False])
        warning = random.choice([True, False])
        sensor_data[sensor_name] = {
            "Measure": measure,
            "Value": value,
            "Critical": critical,
            "Warning": warning,
            "TimeStamp": int(time.time()),
            "ID": random.randint(1, 10000)
        }
    return sensor_data

def main():
    while True:
        sensor_data = read_sensor_data()
        with open("static/sensor-data.json", "w") as f:
            json.dump(sensor_data, f)
        time.sleep(5)

if __name__ == "__main__":
    main()