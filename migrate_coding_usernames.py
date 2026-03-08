"""Migration: add leetcode_username, codechef_username, codeforces_username to users table."""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))

with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS leetcode_username VARCHAR(100),
        ADD COLUMN IF NOT EXISTS codechef_username VARCHAR(100),
        ADD COLUMN IF NOT EXISTS codeforces_username VARCHAR(100);
    """))
    conn.commit()
    print("✅ Coding username columns added to users table.")
