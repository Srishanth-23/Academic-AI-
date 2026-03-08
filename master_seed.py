import os, bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

from app.models.user import User

def hp(pw):
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

users = [
    {
        "unique_id": "ADMIN001",
        "name": "System Administrator",
        "email": "admin@cit.edu",
        "password": "admin123",
        "role": "admin"
    },
    {
        "unique_id": "HOD001",
        "name": "Head of Department",
        "email": "hod@test.com",
        "password": "password123",
        "role": "hod"
    },
    {
        "unique_id": "FAC001",
        "name": "Dr. Faculty",
        "email": "faculty@test.com",
        "password": "password123",
        "role": "faculty"
    },
    {
        "unique_id": "STU001",
        "name": "Alex Student",
        "email": "student@test.com",
        "password": "password123",
        "role": "student"
    }
]

for user_data in users:
    if not db.query(User).filter(User.email == user_data["email"]).first():
        user = User(
            unique_id=user_data["unique_id"],
            name=user_data["name"],
            email=user_data["email"],
            hashed_password=hp(user_data["password"]),
            role=user_data["role"]
        )
        db.add(user)
        print(f"Created {user_data['role']}: {user_data['email']}")
    else:
        print(f"{user_data['role'].capitalize()} already exists: {user_data['email']}")

db.commit()
db.close()
print("Seeding complete.")
