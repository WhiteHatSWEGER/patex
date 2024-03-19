import os
import json

class Api:
    def __init__(self, path_to_data):
        self.__path_to_data = path_to_data  # Use the provided path to data

    def get_sensors(self):
        sensors = []
        if os.path.exists(self.__path_to_data):
            with os.scandir(self.__path_to_data) as entries:
                for entry in entries:
                    sensors.append(entry.name)
        return sensors

    def add_sensor_data(self, sensor_id, data):
        if os.path.exists(self.__path_to_data):
            with open(self.__path_to_data + "/" + str(sensor_id) + ".txt", "a") as file:
                file.write(json.dumps(data) + "\n")
                return data