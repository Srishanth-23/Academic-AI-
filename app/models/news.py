from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    category = Column(String(50), nullable=False) # Exam, Event, Academic, etc.
    date = Column(DateTime, default=datetime.utcnow)
    source = Column(String(100), nullable=False)
    url = Column(String(255), nullable=True)
    type = Column(String(20), default="cit") # "cit" or "tech"
