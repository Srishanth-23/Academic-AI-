from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class BLELog(Base):

    __tablename__ = "ble_logs"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(String, nullable=False)

    rssi = Column(Integer)

    scanner_id = Column(String)

    detected_at = Column(DateTime, default=datetime.utcnow)