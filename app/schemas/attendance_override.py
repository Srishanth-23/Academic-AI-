from pydantic import BaseModel
from typing import List

class AttendanceOverride(BaseModel):
    student_id: int
    present: bool

class UpdateAttendanceRequest(BaseModel):
    session_id: int
    overrides: List[AttendanceOverride]
