import csv
from datetime import datetime
# Import modified sensor modules
import mq3
import mq5
import mq7
import mq135
import mq4
import mq8

# Path to the output CSV file
csv_file_path = 'sensor_readings.csv'

# Initialize sensor objects
mq3_sensor = mq3.MQ3()
mq5_sensor = mq5.MQ5()
mq7_sensor = mq7.MQ7()
mq135_sensor = mq135.MQ135()
mq4_sensor = mq4.MQ4()
mq8_sensor = mq8.MQ8()

# Collect data from each sensor module
def collect_sensor_data():
    mq3_data = mq3_sensor.MQ_Percentage()
    mq5_data = mq5_sensor.MQ_Percentage()
    mq7_data = mq7_sensor.MQ_Percentage()
    mq135_data = mq135_sensor.MQ_Percentage()
    mq4_data = mq4_sensor.MQ_Percentage()
    mq8_data = mq8_sensor.MQ_Percentage()

    # Compile data into a single record, ensure order matches CSV format
    data_record = [
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
        mq3_data['ALCOHOL'], mq5_data['LPG'], mq7_data['CO'],
        mq135_data['CO2'], mq4_data['METHANE'], mq8_data['HYDROGEN']
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
