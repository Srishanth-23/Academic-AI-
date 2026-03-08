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

# Create HOD account if not exists
if not db.query(User).filter(User.email == 'hod@test.com').first():
    hod = User(
        unique_id='HOD001',
        name='Head of Department',
        email='hod@test.com',
        hashed_password=hp('password123'),
        role='hod'
    )
    db.add(hod)
    db.commit()
    print("Created HOD: hod@test.com / password123")
else:
    print("HOD already exists.")

db.close()
print("Done.")
