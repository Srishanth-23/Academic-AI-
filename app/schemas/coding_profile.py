from pydantic import BaseModel
from typing import Optional


class CodingProfileCreate(BaseModel):
    student_id: int
    leetcode_username: Optional[str] = None
    codechef_username: Optional[str] = None
    codeforces_username: Optional[str] = None