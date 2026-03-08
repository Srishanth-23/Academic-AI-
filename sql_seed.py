import os, bcrypt
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

def hp(pw):
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

users = [
    ('ADMIN001', 'System Administrator', 'admin@cit.edu', hp('admin123'), 'admin'),
    ('HOD001', 'Head of Department', 'hod@test.com', hp('password123'), 'hod'),
    ('FAC001', 'Dr. Faculty', 'faculty@test.com', hp('password123'), 'faculty'),
    ('STU001', 'Alex Student', 'student@test.com', hp('password123'), 'student')
]

with engine.connect() as conn:
    for unique_id, name, email, hashed_password, role in users:
        # Check if user exists
        check = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email}).fetchone()
        if not check:
            conn.execute(text("""
                INSERT INTO users (unique_id, name, email, hashed_password, role)
                VALUES (:unique_id, :name, :email, :hashed_password, :role)
            """), {
                "unique_id": unique_id,
                "name": name,
                "email": email,
                "hashed_password": hashed_password,
                "role": role
            })
            print(f"Created {role}: {email}")
        else:
            print(f"{role.capitalize()} already exists: {email}")
    conn.commit()

print("SQL Seeding complete.")
