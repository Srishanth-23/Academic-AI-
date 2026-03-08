from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    unique_id = Column(String, unique=True, nullable=True) # E.g., Roll number, Staff ID
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False) # 'student', 'faculty', 'hod', 'parent'
    department = Column(String, nullable=True) # E.g., "CSE", "ECE"
    
    # Student specific
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)
    
    # Faculty / Advisor specific
    is_class_advisor = Column(Boolean, default=False)
    class_advisor_for_section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)

    # Relationships
    section = relationship("Section", back_populates="students", foreign_keys=[section_id])
    advisor_section = relationship("Section", back_populates="advisors", foreign_keys=[class_advisor_for_section_id])

    # Competitive programming profiles (stored server-side for cross-device sync)
    leetcode_username = Column(String, nullable=True)
    codechef_username = Column(String, nullable=True)
    codeforces_username = Column(String, nullable=True)

class ParentStudent(Base):
    __tablename__ = "parent_student"
    
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("users.id"))
    student_id = Column(Integer, ForeignKey("users.id"))