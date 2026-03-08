import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    try:
        conn.execute(text('ALTER TABLE users ADD COLUMN unique_id VARCHAR(255) UNIQUE;'))
        print("unique_id added")
    except Exception as e:
        print("Warning:", e)

print("Migration Script Complete.")
