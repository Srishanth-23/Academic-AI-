from pydantic import BaseModel
from typing import Optional


class MarksCreate(BaseModel):
    student_id: int
    subject_id: int
    assessment_type: str

    score: Optional[float] = None
    max_score: Optional[float] = None

    grade: Optional[str] = None