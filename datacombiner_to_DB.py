from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import requests
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)

Base = declarative_base()


class SensorData(Base):
    __tablename__ = 'sensor_data'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    MQ2_LPG = Column(Float)
    MQ2_Propane = Column(Float)
    MQ2_Methane = Column(Float)
    MQ2_Hydrogen = Column(Float)
    MQ2_Smoke = Column(Float)
    MQ3_Alcohol = Column(Float)
    MQ3_Ethanol = Column(Float)
    MQ4_Methane = Column(Float)
    MQ4_NaturalGas = Column(Float)
    MQ5_NaturalGas = Column(Float)
    MQ5_LPG = Column(Float)
    MQ6_LPG = Column(Float)
    MQ6_Butane = Column(Float)
    MQ6_Propane = Column(Float)
    MQ7_CO = Column(Float)
    MQ8_H2 = Column(Float)
    MQ9_CO = Column(Float)
    MQ9_FlammableGases = Column(Float)
    MQ135_NH3 = Column(Float)
    MQ135_NOx = Column(Float)
    MQ135_C6H6 = Column(Float)
    MQ135_Smoke = Column(Float)
    MQ135_CO2 = Column(Float)


class LogEntry(Base):
    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sensor_name = Column(String)
    message = Column(String)
    message_type = Column(String)  # "Warning" or "Error"


engine = create_engine('sqlite:///sensors.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

THRESHOLDS = {
    # Include your threshold values here
    'MQ2_LPG': (75, 90),
    'MQ2_Propane': (75, 90),
    'MQ2_Methane': (75, 90),
    'MQ2_Hydrogen': (75, 90),
    'MQ2_Smoke': (75, 90),
    'MQ3_Alcohol': (75, 90),
    'MQ3_Ethanol': (75, 90),
    'MQ4_Methane': (75, 90),
    'MQ4_NaturalGas': (75, 90),
    'MQ5_NaturalGas': (75, 90),
    'MQ5_LPG': (75, 90),
    'MQ6_LPG': (75, 90),
    'MQ6_Butane': (75, 90),
    'MQ6_Propane': (75, 90),
    'MQ7_CO': (75, 90),
    'MQ8_H2': (75, 90),
    'MQ9_CO': (75, 90),
    'MQ9_FlammableGases': (75, 90),
    'MQ135_NH3': (75, 90),
    'MQ135_NOx': (75, 90),
    'MQ135_C6H6': (75, 90),
    'MQ135_Smoke': (75, 90),
    'MQ135_CO2': (75, 90),
}


def receive_sensor_data():
    response = requests.get('http://127.0.0.2:5001/api/read-sensor-csv')  # Ensure this is the correct URL

    if response.status_code == 200:
        sensor_data_list = response.json()  # Assuming this returns a list of sensor data dictionaries
        session = Session()
        try:
            for data in sensor_data_list:
                # Check if entry with this timestamp already exists
                timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S')  # Adjust the format as per your data
                try:
                    existing_entry = session.query(SensorData).filter(SensorData.timestamp == timestamp).one()
                    print(f"Entry with timestamp {timestamp} already exists.")
                except NoResultFound:
                    # Entry does not exist, safe to add
                    data['timestamp'] = timestamp  # Replace string timestamp with datetime object
                    sensor_data_entry = SensorData(**data)
                    session.add(sensor_data_entry)
            session.commit()
            return jsonify({'message': 'Data from CSV processed and stored successfully'}), 200
        except Exception as e:
            session.rollback()
            return jsonify({'error': 'Failed to process or insert data into database', 'details': str(e)}), 500
        finally:
            session.close()
    else:
        return jsonify({'error': 'Failed to fetch data from CSV'}), response.status_code


if __name__ == '__main__':
    app.run(host='127.0.0.2', port=5001, debug=True)
