import requests
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from time import sleep
from datetime import datetime

# Database configuration
DATABASE = 'sqlite:///sensor_data.db'
Base = declarative_base()


# Define the SensorData model
class SensorData(Base):
    __tablename__ = 'sensor_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    Alcohol = Column(Float)
    Methane = Column(Float)
    NaturalGas = Column(Float)
    CO = Column(Float)
    H2 = Column(Float)
    CO2 = Column(Float)


# Create an engine and session
engine = create_engine(DATABASE)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# Die SQL-Suche innerhalb der Datenbank wurde generiert mit Hilfe von Blackbox: blackbox.ai, unterstützt mit
# docs.python.org/3/library/sqlite3.html


def fetch_and_store_data():
    # Get Route des Raspberry Pi
    get_route_url = 'http://192.168.232.156:5001/api/sensor-data'

    try:
        response = requests.get(get_route_url)
        response.raise_for_status()
        data = response.json()

        print(f"Received data: {data}")  # Debug print to check the structure of the received data

        # Angenommen die Daten sind in der richtigen Reihenfolge
        required_keys = ['timestamp', 'Alcohol', 'Methane', 'NaturalGas', 'CO', 'H2', 'CO2']
        if len(data) != len(required_keys):
            print(f'Error: Expected {len(required_keys)} values but got {len(data)} values.')
            return

        session = Session()
        try:
            sensor_data = SensorData(
                timestamp=datetime.fromisoformat(data[0]),
                Alcohol=float(data[1]),
                Methane=float(data[2]),
                NaturalGas=float(data[3]),
                CO=float(data[4]),
                H2=float(data[5]),
                CO2=float(data[6])
            )
            session.add(sensor_data)
            session.commit()
            print('Data fetched and stored successfully')
        except Exception as e:
            session.rollback()
            print(f'Error: {e}')
        finally:
            session.close()

    except requests.RequestException as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    while True:
        fetch_and_store_data()
        sleep(40)
