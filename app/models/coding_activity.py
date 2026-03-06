from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base


class CodingActivity(Base):
    __tablename__ = "coding_activity"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("users.id"))

    platform = Column(String)

    date = Column(Date)

    problems_solved = Column(Integer)