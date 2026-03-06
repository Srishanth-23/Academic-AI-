from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class StudentDevice(Base):

    __tablename__ = "student_devices"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, nullable=False)

    device_id = Column(String, unique=True, nullable=False)

    device_model = Column(String)

    registered_at = Column(DateTime, default=datetime.utcnow)