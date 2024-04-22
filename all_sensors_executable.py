from mq2 import MQ2
from mq3 import MQ3
from mq4 import MQ4
from mq135 import MQ135
from mq6 import MQ6
from mq7 import MQ7
from mq8 import MQ8
from mq9 import MQ9
import csv
import time

# Maximum recommended ppm values for specific gases
max_ppm_thresholds = {
    'CO': 9,       # Example thresholds
    'LPG': 1000,   # Adjust according to your needs
    'SMOKE': 1200,
    'ALCOHOL': 400,
    # Add other gases and their thresholds here
}

# Sensor initialization
sensors = {
    'MQ2': MQ2(),
    'MQ3': MQ3(),
    'MQ4': MQ4(),
    'MQ135': MQ135(),
    'MQ6': MQ6(),
    'MQ7': MQ7(),
    'MQ8': MQ8(),
    'MQ9': MQ9(),
}

filename = "mq_sensors_log.csv"

# Create CSV header
headers = ['Timestamp']
for sensor_name in sensors.keys():
    for gas in max_ppm_thresholds.keys():
        headers.append(f'{sensor_name}_{gas}_ppm')
        headers.append(f'{sensor_name}_{gas}_PercentOfMax')

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

try:
    print("Press CTRL+C to abort.\n")
    
    while True:
        data_row = [time.strftime('%Y-%m-%d %H:%M:%S')]  # Include current timestamp
        for sensor_name, sensor in sensors.items():
            readings = sensor.MQPercentage()  # Assume this returns ppm readings for all gases
            for gas, max_ppm in max_ppm_thresholds.items():
                ppm_value = readings.get(gas, 0)  # Default to 0 if gas not in readings
                percent_of_max = (ppm_value / max_ppm) * 100
                data_row.extend([ppm_value, percent_of_max])
                
        # Write data row to csv file
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_row)
        
        time.sleep(58)  # Sleep for 58 seconds before next measurement
    
except KeyboardInterrupt:
    print("\nMeasurement stopped by User")
except Exception as e:
    print(f"\nError occurred: {e}")
