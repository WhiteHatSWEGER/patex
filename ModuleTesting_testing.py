import unittest
from unittest.mock import patch, MagicMock
import csv
from _r_app import read_latest_sensor_data, on_open, API_ENDPOINT
from data_to_csv import collect_sensor_data, write_data_to_csv
from mq9 import MQ9


class TestClient(unittest.TestCase):

    def test_read_latest_sensor_data(self):
        # Test reading latest sensor data from CSV file
        csv_file_path = 'sensor_readings.csv'
        data = read_latest_sensor_data(csv_file_path)
        self.assertIsNotNone(data)

    @patch('requests.post')
    @patch('app.read_latest_sensor_data', return_value=['2024-05-02 12:00:00', '25.0', '50.0'])
    def test_on_open(self, mock_read_latest_sensor_data, mock_requests_post):
        # Test on_open method behavior
        ws = MagicMock()
        on_open(ws)
        self.assertTrue(mock_read_latest_sensor_data.called)
        self.assertTrue(mock_requests_post.called)

    def test_collect_sensor_data(self):
        # Test collecting sensor data
        data_record = collect_sensor_data()
        self.assertIsNotNone(data_record)
        self.assertEqual(len(data_record), 21)  # Assuming there are 9 sensors

    def test_write_data_to_csv(self):
        # Test writing data to CSV file
        data_record = ['2024-05-02 12:00:00', '25.0', '50.0']  # Sample data record
        write_data_to_csv(data_record)
        # Check if data is successfully written to CSV file and can be read back
        with open('sensor_readings.csv', mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
            self.assertIn(data_record, rows)

    def test_MQ9_MQRead(self):
        # Test MQ9 sensor read functionality
        mq9_sensor = MQ9()
        rs, raw_value = mq9_sensor.MQRead()
        self.assertIsNotNone(rs)
        self.assertIsNotNone(raw_value)

    def test_API_ENDPOINT(self):
        # Test the API endpoint is set correctly
        self.assertEqual(API_ENDPOINT, 'http://laptop-ip-address:5000/api/sensor-data')

    @patch('requests.post')
    def test_post_data_to_server(self, mock_requests_post):
        # Test posting data to the server
        sensor_data = {'timestamp': '2024-05-02 12:00:00', 'sensors': [{'id': 'temperature', 'value': 25.0},
                                                                        {'id': 'humidity', 'value': 50.0}]}
        mock_requests_post.return_value.status_code = 201
        response = on_open.post_data_to_server(sensor_data)
        self.assertTrue(mock_requests_post.called)
        self.assertEqual(response.status_code, 201)

    def test_invalid_csv_file_path(self):
        # Test behavior when an invalid CSV file path is provided
        csv_file_path = 'invalid_path.csv'
        data = read_latest_sensor_data(csv_file_path)
        self.assertIsNone(data)

    def test_invalid_data_record(self):
        # Test behavior when an invalid data record is provided for writing to CSV
        data_record = ['invalid_timestamp', 'invalid_temperature', 'invalid_humidity']
        with self.assertRaises(ValueError):
            write_data_to_csv(data_record)

    def test_MQ9_Calibration(self):
        # Test calibration of MQ9 sensor
        mq9_sensor = MQ9()
        Ro = mq9_sensor.MQ9_Calibration()
        self.assertIsNotNone(Ro)

    def test_MQ9_MQPercentage(self):
        # Test MQPercentage method of MQ9 sensor
        mq9_sensor = MQ9()
        percentages = mq9_sensor.MQPercentage()
        self.assertIsNotNone(percentages)


if __name__ == '__main__':
    unittest.main()
