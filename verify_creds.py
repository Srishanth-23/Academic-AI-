import os, bcrypt
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

def verify_password(password: str, hashed: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

email = "student@test.com"
password = "password123"

with engine.connect() as conn:
    result = conn.execute(text("SELECT hashed_password FROM users WHERE email = :email"), {"email": email}).fetchone()
    if result:
        hashed = result[0]
        is_valid = verify_password(password, hashed)
        print(f"User: {email}")
        print(f"Hashed Password: {hashed}")
        print(f"Verification Result: {'SUCCESS' if is_valid else 'FAILED'}")
    else:
        print(f"User {email} not found in DB.")
