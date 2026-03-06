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