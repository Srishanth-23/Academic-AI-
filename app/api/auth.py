from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import register_user, login_user
from app.dependencies import get_db


router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    new_user = register_user(db, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    return {"message": "User created successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    token = login_user(db, user.email, user.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": token, "token_type": "bearer"}