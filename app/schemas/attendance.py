from pydantic import BaseModel


class CreateSession(BaseModel):
    subject_id: int
    faculty_id: int


class MarkAttendance(BaseModel):
    session_id: int
    student_id: int