import os
import sys

# Add the project root to the python path
sys.path.append(os.getcwd())

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.news import News, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        if db.query(News).count() > 0:
            print("News already seeded.")
            return
        
        initial_news = [
            News(title="🎓 End Semester Examinations – April 2026", summary="The April 2026 End Semester Examinations are scheduled from 8th April to 30th April 2026. Carry hall tickets.", category="Exam", source="CIT Examinations Cell", type="cit"),
            News(title="🏆 Nakshatra 2026 – Annual Technical Symposium", summary="CIT's flagship symposium returns on 22nd & 23rd March. Register for Paper Presentation, Hackathon, and more.", category="Event", source="CIT Student Affairs", type="cit"),
            News(title="📚 NPTEL Enrollment Open – Swayam Portal", summary="Enroll in NPTEL online courses via Swayam portal before 18th March. Earn extra credits recognized by AICTE.", category="Academic", source="CIT Academic Section", type="cit"),
            News(title="Google Releases Gemini 2.0 Ultra", summary="Google DeepMind has released Gemini 2.0 Ultra, featuring improved multimodal reasoning capabilities.", category="AI", source="TechCrunch", type="tech", url="https://techcrunch.com"),
            News(title="Meta open-sources Llama 4 Turbo", summary="Meta AI has open-sourced Llama 4 Turbo, claiming 3x lower latency while maintaining accuracy.", category="AI", source="The Verge", type="tech", url="https://theverge.com")
        ]
        
        db.add_all(initial_news)
        db.commit()
        print("Initial news data seeded successfully.")
    except Exception as e:
        print(f"Error seeding news: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
