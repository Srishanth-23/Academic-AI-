import os, bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Use the same logic as seed_hod.py
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    # Fallback to a common local path if env is not set (for safety)
    DATABASE_URL = "sqlite:///./academic_performance.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

from app.models.user import User

def hp(pw):
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Create Admin account if not exists
if not db.query(User).filter(User.email == 'admin@cit.edu').first():
    admin = User(
        unique_id='ADMIN001',
        name='System Administrator',
        email='admin@cit.edu',
        hashed_password=hp('admin123'),
        role='admin'
    )
    db.add(admin)
    db.commit()
    print("Created Admin: admin@cit.edu / admin123")
else:
    print("Admin already exists.")

db.close()
print("Done.")
