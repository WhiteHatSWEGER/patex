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
    # Instantiate each sensor class
    mq2 = MQ2()
    mq3 = MQ3()
    mq4 = MQ4()
    mq5 = MQ5()
    mq6 = MQ6()
    mq7 = MQ7()
    mq8 = MQ8()
    mq9 = MQ9()
    mq135 = MQ135()

    # Call MQPercentage method on each sensor instance
    mq2_data = mq2.MQPercentage()
    mq3_data = mq3.MQPercentage()
    mq4_data = mq4.MQPercentage()
    mq5_data = mq5.MQPercentage()
    mq6_data = mq6.MQPercentage()
    mq7_data = mq7.MQPercentage()
    mq8_data = mq8.MQPercentage()
    mq9_data = mq9.MQPercentage()
    mq135_data = mq135.MQPercentage()

    # Compile data into a single record, ensure order matches CSV format
    data_record = [
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
        mq2_data['LPG'], mq2_data['Propane'], mq2_data['Methane'], mq2_data['Hydrogen'], mq2_data['Smoke'],
        mq3_data['Alcohol'], mq3_data['Ethanol'],
        mq4_data['Methane'], mq4_data['NaturalGas'],
        mq5_data['NaturalGas'], mq5_data['LPG'],
        mq6_data['LPG'], mq6_data['Butane'], mq6_data['Propane'],
        mq7_data['CO'],
        mq8_data['H2'],
        mq9_data['CO'], mq9_data['FlammableGases'],
        mq135_data['NH3'], mq135_data['NOx'], mq135_data['C6H6'], mq135_data['Smoke'], mq135_data['CO2']
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
