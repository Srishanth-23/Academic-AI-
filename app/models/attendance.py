from sqlalchemy import Column, Integer, ForeignKey, Boolean
from app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("class_sessions.id"))

    student_id = Column(Integer, ForeignKey("users.id"))

    present = Column(Boolean, default=False)