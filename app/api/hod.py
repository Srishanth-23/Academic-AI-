from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.dependencies import get_db
from app.models.user import User, ParentStudent
from app.schemas.user import UserCreate
from app.utils.security import hash_password
from jose import jwt, JWTError
from app.config import settings

router = APIRouter()

def get_current_user(token: str = Header(None), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Missing authorization token")
    if token.startswith("Bearer "):
        token = token[7:]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/create-user")
def create_user(user_data: UserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "hod":
        raise HTTPException(status_code=403, detail="Only HOD can create accounts")

    # Check if email is already taken
    existing_user_by_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if unique_id is already taken
    existing_user_by_id = db.query(User).filter(User.unique_id == user_data.unique_id).first()
    if existing_user_by_id:
        raise HTTPException(status_code=400, detail="Unique ID already registered")

    new_user = User(
        unique_id=user_data.unique_id,
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"{user_data.role} created successfully", "user_id": new_user.id}
