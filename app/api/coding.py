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

from app.services.coding_proxy_service import (
    fetch_leetcode_stats,
    fetch_codeforces_stats,
    fetch_codechef_stats
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


# Fetch live competitive programming stats from 3rd party APIs
@router.get("/stats/{platform}/{username}")
async def get_live_coding_stats(platform: str, username: str):
    platform = platform.lower()
    if platform == "leetcode":
        return await fetch_leetcode_stats(username)
    elif platform == "codeforces":
        return await fetch_codeforces_stats(username)
    elif platform == "codechef":
        return await fetch_codechef_stats(username)
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Unsupported platform. Use leetcode, codeforces, or codechef.")