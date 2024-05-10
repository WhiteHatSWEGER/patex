import csv
import random
from datetime import datetime, timedelta
from time import sleep

# Configuration
output_file = 'basic.csv'  # Existing CSV file
time_interval = timedelta(seconds=30)  # Time interval between data points

# Gas types and their value ranges
gas_types = ['Alcohol', 'Methane', 'NaturalGas', 'CO', 'H2', 'CO2']
value_ranges = {
    'Alcohol': (50, 60),
    'Methane': (60, 70),
    'NaturalGas': (70, 80),
    'CO': (80, 90),
    'H2': (90, 100),
    'CO2': (100, 120)
}

# Function to generate a random value within a specified range
def generate_random_value(value_range):
    return random.uniform(*value_range)


while True:
    # Get the last timestamp from the existing CSV file
    try:
        with open(output_file, 'r') as csvfile:
            last_row = list(csv.reader(csvfile))[-1]
            last_timestamp = datetime.strptime(last_row[0], '%Y-%m-%d %H:%M:%S')
    except (FileNotFoundError, IndexError):
        last_timestamp = datetime.now() - time_interval

    # Generate a new row of data
    new_timestamp = last_timestamp + time_interval
    new_row = [new_timestamp.strftime('%Y-%m-%d %H:%M:%S')]
    new_row.extend(generate_random_value(value_ranges[gas]) for gas in gas_types)

    # Append the new row to the CSV file
    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_row)
    print(f'New row appended to {output_file}')
    sleep(30)
