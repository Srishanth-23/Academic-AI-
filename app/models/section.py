from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False) # e.g., "CSE-A", "CSE-B"
    department = Column(String(100), nullable=False) # e.g., "Computer Science"
    batch_year = Column(Integer, nullable=False) # e.g., 2026

    # Relationships
    students = relationship("User", back_populates="section", foreign_keys="User.section_id")
    advisors = relationship("User", back_populates="advisor_section", foreign_keys="User.class_advisor_for_section_id")
