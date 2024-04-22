import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
Base = declarative_base()


class SensorData(Base):
    __tablename__ = 'sensor_data'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    # MQ2 Sensor columns
    MQ2_LPG = Column(Float)
    MQ2_Propane = Column(Float)
    MQ2_Methane = Column(Float)
    MQ2_Hydrogen = Column(Float)
    MQ2_Smoke = Column(Float)
    # MQ3 Sensor columns for Alcohol and Ethanol
    MQ3_Alcohol = Column(Float)
    MQ3_Ethanol = Column(Float)
    # MQ4 Sensor columns for Methane and Natural Gas
    MQ4_Methane = Column(Float)
    MQ4_NaturalGas = Column(Float)
    # MQ5 Sensor columns for Natural Gas and LPG
    MQ5_NaturalGas = Column(Float)
    MQ5_LPG = Column(Float)
    # MQ6 Sensor columns for LPG, Butane, and Propane
    MQ6_LPG = Column(Float)
    MQ6_Butane = Column(Float)
    MQ6_Propane = Column(Float)
    # MQ7 Sensor column for CO
    MQ7_CO = Column(Float)
    # MQ8 Sensor column for H2
    MQ8_H2 = Column(Float)
    # MQ9 Sensor columns for CO and Flammable Gases
    MQ9_CO = Column(Float)
    MQ9_FlammableGases = Column(Float)
    # MQ135 Sensor columns for NH3, NOx, C6H6, Smoke, and CO2
    MQ135_NH3 = Column(Float)
    MQ135_NOx = Column(Float)
    MQ135_C6H6 = Column(Float)
    MQ135_Smoke = Column(Float)
    MQ135_CO2 = Column(Float)
    # Add other sensors following the same pattern...


engine = create_engine('sqlite:///sensors.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def generate_and_insert_data():
    session = Session()
    start_date = datetime.now() - timedelta(days=1)
    num_entries = 100

    for _ in range(num_entries):
        new_entry = SensorData(
            timestamp=start_date,
            # MQ2 Sensor measures
            MQ2_LPG=random.uniform(0, 100),
            MQ2_Propane=random.uniform(0, 100),
            MQ2_Methane=random.uniform(0, 100),
            MQ2_Hydrogen=random.uniform(0, 100),
            MQ2_Smoke=random.uniform(0, 100),
            # MQ3 Sensor measures for Alcohol and Ethanol
            MQ3_Alcohol=random.uniform(0, 100),
            MQ3_Ethanol=random.uniform(0, 100),
            # MQ4 Sensor measures for Methane and Natural Gas
            MQ4_Methane=random.uniform(0, 100),
            MQ4_NaturalGas=random.uniform(0, 100),
            # MQ5 Sensor measures for Natural Gas and LPG
            MQ5_NaturalGas=random.uniform(0, 100),
            MQ5_LPG=random.uniform(0, 100),
            # MQ6 Sensor measures for LPG, Butane, and Propane
            MQ6_LPG=random.uniform(0, 100),
            MQ6_Butane=random.uniform(0, 100),
            MQ6_Propane=random.uniform(0, 100),
            # MQ7 Sensor measure for CO
            MQ7_CO=random.uniform(0, 100),
            # MQ8 Sensor measure for H2
            MQ8_H2=random.uniform(0, 100),
            # MQ9 Sensor measures for CO and Flammable Gases
            MQ9_CO=random.uniform(0, 100),
            MQ9_FlammableGases=random.uniform(0, 100),
            # MQ135 Sensor measures for NH3, NOx, C6H6, Smoke, and CO2
            MQ135_NH3=random.uniform(0, 100),
            MQ135_NOx=random.uniform(0, 100),
            MQ135_C6H6=random.uniform(0, 100),
            MQ135_Smoke=random.uniform(0, 100),
            MQ135_CO2=random.uniform(0, 100),
            # Add other measures following the same pattern...
        )
        session.add(new_entry)
        start_date += timedelta(minutes=5)  # Increment by 5 minutes for each entry

    session.commit()
    session.close()


if __name__ == '__main__':
    generate_and_insert_data()
    print("Dummy data generated and inserted into the database.")
