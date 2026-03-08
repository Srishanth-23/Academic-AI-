import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
print(f"Connecting to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT name, email, role FROM users LIMIT 20;"))
        rows = result.fetchall()
        print("\n--- Users Found ---")
        for row in rows:
            print(f"Name: {row[0]}, Email: {row[1]}, Role: {row[2]}")
except Exception as e:
    print(f"Error: {e}")
