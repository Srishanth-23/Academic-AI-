from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class CodingProfile(Base):
    __tablename__ = "coding_profiles"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("users.id"))

    leetcode_username = Column(String, nullable=True)

    codechef_username = Column(String, nullable=True)

    codeforces_username = Column(String, nullable=True)