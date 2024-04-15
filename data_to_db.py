from sqlalchemy import Column, Integer, Float, String, DateTime, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class SensorData(Base):
    __tablename__ = 'sensor_data'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(String)
    timestamp = Column(DateTime)
    measure = Column(String)
    value_ppm = Column(Float)

class PercentData(Base):
    __tablename__ = 'percent_data'
    id = Column(Integer, primary_key=True)
    sensor_data_id = Column(Integer, ForeignKey('sensor_data.id'))
    timestamp = Column(DateTime)
    value_percent = Column(Float)
    sensor_data = relationship("SensorData", back_populates="percent_data")

class LogEntries(Base):
    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(String)
    timestamp = Column(DateTime)
    measure = Column(String)
    value_ppm = Column(Float)
    entry_type = Column(String)  # "Warning" or "Alert"

SensorData.percent_data = relationship("PercentData", order_by=PercentData.id, back_populates="sensor_data")


recommended_ppm = {
    'LPG': 1000, 'Propane': 2000, 'Methane': 500, 'Hydrogen': 2000, 'Smoke': 150,
    'Alcohol': 1000, 'Ethanol': 1000, 'Natural Gas': 1000, 'Butane': 1900,
    'CO': 9, 'H2': 1000, 'Flammable Gases': 1000, 'NH3': 25, 'NOx': 100, 'C6H6': 5, 'CO2': 1000
}

def calculate_percent_value(measure, value_ppm):
    """Calculate percent value relative to recommended ppm."""
    return (value_ppm / recommended_ppm[measure]) * 100

def create_log_entry(session, sensor_id, timestamp, measure, value_ppm, entry_type):
    """Create a log entry for a warning or alert."""
    log_entry = LogEntries(sensor_id=sensor_id, timestamp=timestamp, measure=measure, value_ppm=value_ppm, entry_type=entry_type)
    session.add(log_entry)

# Modify the processing function to include percent data and log entry creation
def process_csv_data(csv_reader):
    """Extended to handle percent data and log entries."""
    for row in csv_reader:
    # Previous steps: Extract data from row
        timestamp = extract_timestamp(row)
    measurements = extract_measurements(row)  # This would use your parsing logic for structured strings

    for measurement in measurements:
        value_ppm = measurement['value_ppm']
        measure = measurement['measure']
        sensor_id = measurement['sensor_id']

        # Calculate percent value
        percent_value = calculate_percent_value(measure, value_ppm)
        
        # Insert data into SensorData and PercentData tables
        sensor_data_entry = insert_into_SensorData(timestamp, sensor_id, measure, value_ppm)
        insert_into_PercentData(sensor_data_entry, percent_value)
        
        # Check for and handle warnings/alerts
        if percent_value >= 70:
            entry_type = "Warning" if percent_value < 100 and percent_value > 80  else "Alert"
            create_log_entry(sensor_id, timestamp, measure, value_ppm, entry_type)

# Committing changes to the database
session.commit()
