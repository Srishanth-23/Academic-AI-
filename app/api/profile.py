from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.dependencies import get_db
from app.models.user import User

router = APIRouter()


class CodingProfileUpdate(BaseModel):
    leetcode_username: Optional[str] = None
    codechef_username: Optional[str] = None
    codeforces_username: Optional[str] = None


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    unique_id: Optional[str] = None


@router.get("/profile/{user_id}")
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Get a user's profile including their saved coding platform usernames."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "unique_id": user.unique_id,
        "leetcode_username": user.leetcode_username or "",
        "codechef_username": user.codechef_username or "",
        "codeforces_username": user.codeforces_username or "",
    }


@router.patch("/profile/{user_id}")
def update_profile_details(user_id: int, data: ProfileUpdate, db: Session = Depends(get_db)):
    """Update general user profile details (name, unique_id)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.name is not None:
        user.name = data.name.strip() if data.name else user.name
    if data.unique_id is not None:
        uid = data.unique_id.strip() if data.unique_id else ""
        if uid:
            # Check if unique_id is already taken by another user
            existing = db.query(User).filter(User.unique_id == uid, User.id != user_id).first()
            if existing:
                raise HTTPException(status_code=400, detail="This ID is already registered to another user.")
            user.unique_id = uid

    db.commit()
    db.refresh(user)
    return {
        "message": "Profile updated successfully",
        "name": user.name,
        "unique_id": user.unique_id
    }


@router.patch("/profile/{user_id}/coding")
def update_coding_usernames(user_id: int, data: CodingProfileUpdate, db: Session = Depends(get_db)):
    """Save or update coding platform usernames for a user (cross-device sync)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.leetcode_username is not None:
        user.leetcode_username = data.leetcode_username.strip() if data.leetcode_username else None
    if data.codechef_username is not None:
        user.codechef_username = data.codechef_username.strip() if data.codechef_username else None
    if data.codeforces_username is not None:
        user.codeforces_username = data.codeforces_username.strip() if data.codeforces_username else None

    db.commit()
    db.refresh(user)
    return {
        "message": "Coding usernames updated",
        "leetcode_username": user.leetcode_username or "",
        "codechef_username": user.codechef_username or "",
        "codeforces_username": user.codeforces_username or "",
    }


@router.get("/profile/by-email")
def get_profile_by_email(email: str = Query(...), db: Session = Depends(get_db)):
    """Get user profile by email (used after login when only email is stored)."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "unique_id": user.unique_id,
        "leetcode_username": user.leetcode_username or "",
        "codechef_username": user.codechef_username or "",
        "codeforces_username": user.codeforces_username or "",
    }
