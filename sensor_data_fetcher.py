import smbus
import time
import random
import json

# Set up the I2C interface
bus = smbus.SMBus(1)  # Use 0 for Raspberry Pi version 1, 1 for Raspberry Pi version 2 and newer

# Define the sensor type, address, and register addresses
SENSOR_TYPE = 0x04  # Replace with your sensor type
SENSOR_ADDRESS = 0x23  # Replace with your sensor address
REGISTER_ADDRESS_START = 0x00  # Replace with your sensor's register address for the start of the data
REGISTER_ADDRESS_END = 0x09  # Replace with your sensor's register address for the end of the data

def read_i2c_sensor(bus, sensor_type, sensor_address, register_address_start, register_address_end):
    data = []
    for address in range(register_address_start, register_address_end + 1):
        value = bus.read_byte_data(sensor_address, address)
        data.append(value)
    return data

def calculate_percentage(actual_value, max_value):
    if actual_value >= max_value:
        return 100
    return int(round((actual_value / max_value) * 100))

def collect_sensor_data():
    sensor_data = {}
    sensor_data["Info"] = {
        "TimeStamp": int(time.time()),
        "ID": random.randint(1, 10000)
    }

    # Replace the following lines with the actual sensor data collection
    data = read_i2c_sensor(bus, SENSOR_TYPE, SENSOR_ADDRESS, REGISTER_ADDRESS_START, REGISTER_ADDRESS_END)

    MEASURES = [
        ("CO2", 1000),
        ("NO2", 200),
        ("Butan", 50),
        ("Propean", 100),
        ("Alkohol", 200),
        ("Rauch", 100),
        ("NO", 50),
        ("CO", 50),
        ("O3", 100)
    ]

    for i, (measure, max_value) in enumerate(MEASURES):
        value = data[i]
        warning_threshold = max_value * 0.9
        critical_threshold = max_value

        percent = calculate_percentage(value, max_value)
        critical = percent >= critical_threshold
        warning = percent >= warning_threshold

        sensor_data[f"Sensor{i + 1}"] = {
            "Measure": measure,
            "Value": percent,
            "Critical": critical,
            "Warning": warning
        }

    return sensor_data

def main():
    while True:
        sensor_data = collect_sensor_data()
        current_time = int(time.time())
        one_hour_ago = current_time - 60 * 60

        # Filter the sensor data based on the one-hour time window
        filtered_sensor_data = []
        for entry in sensor_data:
            timestamp = entry['Info']['TimeStamp']
            if one_hour_ago <= timestamp <= current_time:
                filtered_sensor_data.append(entry)

        # Append the filtered sensor data to the corresponding file
        for entry in filtered_sensor_data:
            sensor_id = entry['Info']['ID']
            file_path = os.path.join(path_to_data, f"{sensor_id}.txt")
            with open(file_path, 'a') as f:
                f.write(json.dumps(entry) + "\n")

        time.sleep(5)

if __name__ == "__main__":
    main()
