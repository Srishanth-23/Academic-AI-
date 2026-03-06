from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class CodingSkills(Base):
    __tablename__ = "coding_skills"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("users.id"))

    topic = Column(String)

    solved_count = Column(Integer)