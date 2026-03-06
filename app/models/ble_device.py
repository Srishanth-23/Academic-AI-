from sqlalchemy import Column, Integer, String
from app.database import Base

class BLEDevice(Base):

    __tablename__ = "ble_devices"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer)

    device_id = Column(String, unique=True)

    device_name = Column(String)