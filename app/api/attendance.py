from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.attendance import CreateSession, MarkAttendance
from app.services.attendance_service import create_session, mark_attendance
from app.dependencies import get_db

from app.services.attendance_service import (
    create_session,
    mark_attendance,
    get_subject_attendance,
    get_overall_attendance
)

from app.schemas.attendance_override import UpdateAttendanceRequest
from app.services.teacher_attendance_service import get_class_roster_attendance, update_class_attendance


router = APIRouter()


@router.post("/create-session")
def create_class_session(session: CreateSession, db: Session = Depends(get_db)):
    return create_session(db, session)


@router.post("/mark")
def mark_student_attendance(data: MarkAttendance, db: Session = Depends(get_db)):
    return mark_attendance(db, data)

@router.get("/subject/{student_id}/{subject_id}")
def subject_attendance(student_id: int, subject_id: int, db: Session = Depends(get_db)):
    return get_subject_attendance(db, student_id, subject_id)


@router.get("/overall/{student_id}")
def overall_attendance(student_id: int, db: Session = Depends(get_db)):
    return get_overall_attendance(db, student_id)

@router.get("/class/{session_id}")
def class_roster_attendance(session_id: int, section_id: int = None, db: Session = Depends(get_db)):
    return get_class_roster_attendance(db, session_id, section_id)

@router.put("/update")
def execute_attendance_override(request: UpdateAttendanceRequest, faculty_id: int, db: Session = Depends(get_db)):
    # Assuming faculty_id comes from token in real implementation.
    # Passing directly here to align with current auth structure.
    return update_class_attendance(db, request, faculty_id)