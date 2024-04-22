from mq2 import MQ2
from mq3 import MQ3
from mq4 import MQ4
# from mq5 import MQ5
from mq135 import MQ135
from mq6 import MQ6
from mq7 import MQ7
from mq8 import MQ8
from mq9 import MQ9
import csv
import time

filename = "mq_sensors_log.csv"

# Initialize sensors
sensors = {
    'MQ2': MQ2(),
    'MQ3': MQ3(),
    'MQ4': MQ4(),
    # 'MQ5': MQ5(),
    'MQ135': MQ135(),
    'MQ6': MQ6(),
    'MQ7': MQ7(),
    'MQ8': MQ8(),
    'MQ9': MQ9(),
}

# Create header row in new CSV file
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    headers = ['Timestamp'] + [f'Raw_value_{name}' for name in sensors.keys()]
    writer.writerow(headers)

try:
    print("Press CTRL+C to abort.\n")

    while True:
        data_row = [time.strftime('%Y-%m-%d %H:%M:%S')]  # Include current timestamp
        for name, sensor in sensors.items():
            measurement = sensor.MQPercentage()
            data_row.append(measurement["RAW_VALUE"])  # Append RAW_VALUE for each sensor
            
        # Write data row to csv file
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_row)
        
        time.sleep(58)  # Adjust the sleep time as needed
    
# Handle script interruption
except KeyboardInterrupt:
    print("Measurement stopped by User")
    with open(filename, 'r') as file:
        print(file.read())
except Exception as e:
    print(f"\nAbort by user or error: {e}")
