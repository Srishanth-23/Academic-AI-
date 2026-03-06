from sqlalchemy import Column, Integer, ForeignKey, String, Float
from app.database import Base


class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("users.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))

    assessment_type = Column(String, nullable=False)

    score = Column(Float, nullable=True)

    max_score = Column(Float, nullable=True)

    grade = Column(String, nullable=True)