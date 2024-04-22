from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

# Define the base class
Base = declarative_base()


# SensorData model
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


# LogEntry model for logging warnings/errors
class LogEntry(Base):
    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sensor_name = Column(String)
    message = Column(String)
    message_type = Column(String)  # "Warning" or "Error"


# Database setup
engine = create_engine('sqlite:///sensors.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Thresholds for warnings and errors (example values)
THRESHOLDS = {
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


def log_warning_or_error(session, sensor_name, value):
    warning_threshold, error_threshold = THRESHOLDS.get(sensor_name, (0, 0))
    if value > error_threshold:
        message = f"Error: {sensor_name} reading {value} exceeds error threshold."
        message_type = "Error"
    elif value > warning_threshold:
        message = f"Warning: {sensor_name} reading {value} exceeds warning threshold."
        message_type = "Warning"
    else:
        return  # No action needed
    log_entry = LogEntry(sensor_name=sensor_name, message=message, message_type=message_type)
    session.add(log_entry)


def generate_and_insert_data(session):
    start_date = datetime.now() - timedelta(days=1)
    num_entries = 100

    for _ in range(num_entries):
        sensor_readings = {sensor: random.uniform(0, 100) for sensor in THRESHOLDS}
        new_entry = SensorData(timestamp=start_date, **sensor_readings)
        session.add(new_entry)

        for sensor_name, value in sensor_readings.items():
            log_warning_or_error(session, sensor_name, value)

        start_date += timedelta(minutes=5)  # Increment by 5 minutes for each entry

    session.commit()


if __name__ == '__main__':
    session = Session()
    generate_and_insert_data(session)
    print("Dummy data generated and inserted into the database, along with any warnings/errors.")
