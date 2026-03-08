from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=False)  # e.g. "Data Structures"
    subject_code = Column(String(20), nullable=True)  # e.g. "CS301"
    file_url = Column(String(500), nullable=True)  # Google Drive / GDrive share link
    file_type = Column(String(20), default="pdf")  # pdf, doc, link, image
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    uploader = relationship("User")
