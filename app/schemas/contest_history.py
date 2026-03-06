from pydantic import BaseModel
from datetime import date


class ContestHistoryCreate(BaseModel):
    student_id: int
    platform: str
    contest_name: str
    rank: int
    problems_solved: int
    contest_date: date