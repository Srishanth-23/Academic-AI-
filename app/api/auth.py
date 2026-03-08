from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.schemas.user import UserCreate, UserLogin, ChangePasswordRequest
from app.services.auth_service import register_user, login_user
from app.dependencies import get_db
from app.models.user import User
from app.utils.security import hash_password, verify_password


router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    new_user = register_user(db, user)

    if not new_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    return {"message": "User created successfully"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    result = login_user(db, user.email, user.password)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": result["token"],
        "token_type": "bearer",
        "user_id": result["user_id"],
        "role": result["role"],
        "name": result["name"],
    }

@router.post("/change-password")
def change_password(data: ChangePasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
        
    user.hashed_password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}