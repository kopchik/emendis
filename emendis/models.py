from sqlalchemy import TIMESTAMP, Column, Float, Integer, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, index=True)
    timestamp = Column(TIMESTAMP, index=True)
    dwell_time = Column(Float)
    __table_args__ = (UniqueConstraint("sensor_id", "timestamp"),)

    # TODO: default ordering doesn't work
    # __mapper_args__ = {
    #     "order_by": "timestamp",
    # }
