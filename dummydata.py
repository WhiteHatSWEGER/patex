import csv
from datetime import datetime, timedelta
import random

# Parameters for dummy data generation
num_entries = 100  # Number of data entries to generate
start_date = datetime.now() - timedelta(days=1)  # Starting from 1 day ago
sensor_measures = {
    'MQ2': ['LPG', 'Propane', 'Methane', 'Hydrogen', 'Smoke'],
    'MQ3': ['Alcohol', 'Ethanol'],
    'MQ4': ['Methane', 'Natural Gas'],
    'MQ5': ['Natural Gas', 'LPG'],
    'MQ6': ['LPG', 'Butane', 'Propane'],
    'MQ7': ['CO'],
    'MQ8': ['H2'],
    'MQ9': ['CO', 'Flammable Gases'],
    'MQ135': ['NH3', 'NOx', 'C6H6', 'Smoke', 'CO2']
}
csv_file_path = 'sensor_data_array_like_dummy.csv'  # Output CSV file

def generate_sensor_data():
    """Generate dummy data for all measures of each sensor, structuring them as an array-like string."""
    sensor_data = {}
    for sensor, measures in sensor_measures.items():
        measures_data = []
        for measure in measures:
            value = round(random.uniform(0, 100), 2)  # Generate a dummy sensor value
            measures_data.append(f"{measure}:{value}")
        sensor_data[sensor] = '[' + ', '.join(measures_data) + ']'
    return sensor_data

def generate_dummy_data():
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        # Header row: Timestamp and sensor IDs
        header = ['timestamp'] + list(sensor_measures.keys())
        writer.writerow(header)
        
        for i in range(num_entries):
            timestamp = start_date + timedelta(minutes=10*i)  # Incremental timestamps, every 10 minutes
            sensor_data = generate_sensor_data()
            
            # Organize the row data, keeping sensor measurements grouped
            row = [timestamp] + [sensor_data[sensor] for sensor in sensor_measures.keys()]
            writer.writerow(row)

if __name__ == '__main__':
    generate_dummy_data()
    print(f"Dummy data generated and stored in {csv_file_path}")
