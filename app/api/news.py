from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import SessionLocal
from app.models.news import News

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_news(type: Optional[str] = "cit", db: Session = Depends(get_db)):
    """Fetch all news of a certain type (cit or tech)."""
    return db.query(News).filter(News.type == type).order_by(News.date.desc()).all()

@router.post("/seed")
def seed_news(db: Session = Depends(get_db)):
    """Seed initial news data if table is empty."""
    if db.query(News).count() > 0:
        return {"message": "News already seeded"}
    
    initial_news = [
        News(title="🎓 End Semester Examinations – April 2026", summary="April 2026 End Sem exams start April 8. Carry hall tickets.", category="Exam", source="CIT Exam Cell", type="cit"),
        News(title="🏆 Nakshatra 2026 – Annual Technical Symposium", summary="CIT's symposium returns March 22-23. Prize pool ₹2L+.", category="Event", source="CIT Student Affairs", type="cit"),
        News(title="Google Releases Gemini 2.0 Ultra", summary="Gemini 2.0 Ultra features multimodal reasoning, released today.", category="AI", source="TechCrunch", type="tech", url="https://techcrunch.com")
    ]
    db.add_all(initial_news)
    db.commit()
    return {"message": "Initial news data seeded."}
