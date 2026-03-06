from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base


class ContestHistory(Base):
    __tablename__ = "contest_history"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("users.id"))

    platform = Column(String)

    contest_name = Column(String)

    rank = Column(Integer)

    problems_solved = Column(Integer)

    contest_date = Column(Date)