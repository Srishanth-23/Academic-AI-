from pydantic import BaseModel
from datetime import date


class CodingActivityCreate(BaseModel):
    student_id: int
    platform: str
    date: date
    problems_solved: int