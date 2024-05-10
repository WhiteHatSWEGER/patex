import csv
from datetime import datetime
# Import sensor modules
import mq2
import mq3
import mq4
import mq5
import mq6
import mq7
import mq8
import mq9
import mq135

# Path to the output CSV file
csv_file_path = 'sensor_readings.csv'


# Collect data from each sensor module
def collect_sensor_data():
    # Example assuming each module has a get_data() function returning a dict of readings
    # Adjust these calls according to your module functions and returned data structures
    mq3_data = mq3.get_data()
    mq4_data = mq4.get_data()
    mq5_data = mq5.get_data()
    mq7_data = mq7.get_data()
    mq8_data = mq8.get_data()
    mq135_data = mq135.get_data()

    # Compile data into a single record, ensure order matches CSV format
    data_record = [
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
        mq3_data['Alcohol'],
        mq4_data['Methane'],
        mq5_data['NaturalGas'],
        mq7_data['CO'],
        mq8_data['H2'],
        mq135_data['CO2'],
    ]
    return data_record


# Write data to the CSV file
def write_data_to_csv(data_record):
    with open(csv_file_path, mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data_record)


def main():
    data_record = collect_sensor_data()
    write_data_to_csv(data_record)
    print(f"Data recorded at {data_record[0]}")


if __name__ == '__main__':
    main()
