from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

class Api:
    def __init__(self, url, token, organization, bucket):
        self.__url = url
        self.__token = token
        self.__organization = organization
        self.__bucket = bucket

        self.__client = InfluxDBClient(url=self.__url, token=self.__token)
        self.__client.switch_database(self.__bucket)
        self.__write_api = self.__client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))

    def get_sensors(self):
def get_sensors(self):
    query = "SELECT * FROM gas_measurement"
    result = self.__client.query_api().query(query)
    sensors = []
    for table in result.raw["series"]:
        for row in table["values"]:
            sensors.append(dict(zip(row[0], row[1:])))
    return sensors

    def add_sensor_data(self, location, data):
        point = (
            Point("gas_measurement")
            .tag("location", location)
            .field("gas_1", data["gas_1"])
            .field("gas_2", data["gas_2"])
            # Add more fields for other gases as needed
            .time_precision(WritePrecision.MS)
        )

        self.__write_api.write(bucket=self.__bucket, record=point)
