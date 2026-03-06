from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.coding_profile import CodingProfileCreate
from app.schemas.coding_activity import CodingActivityCreate
from app.schemas.contest_history import ContestHistoryCreate

from app.services.coding_service import (
    create_coding_profile,
    add_daily_activity,
    add_contest_result
)

router = APIRouter()


# Create coding profile for a student
@router.post("/profile")
def create_profile(data: CodingProfileCreate, db: Session = Depends(get_db)):
    return create_coding_profile(db, data)


# Add daily coding activity
@router.post("/activity")
def add_activity(data: CodingActivityCreate, db: Session = Depends(get_db)):
    return add_daily_activity(db, data)


# Add contest performance
@router.post("/contest")
def add_contest(data: ContestHistoryCreate, db: Session = Depends(get_db)):
    return add_contest_result(db, data)