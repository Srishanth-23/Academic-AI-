"""Quick migration to create the notes table."""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            subject VARCHAR(100) NOT NULL,
            subject_code VARCHAR(20),
            file_url VARCHAR(500),
            file_type VARCHAR(20) DEFAULT 'pdf',
            uploaded_by INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT NOW()
        );
    """))
    conn.commit()
    print("✅ Notes table created (or already exists).")
