from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, func
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

from app.dependencies import get_db
from app.models.user import User
from app.database import Base

# ------- Inline model for daily attendance (separate from QR-session attendance) -------
class DailyAttendance(Base):
    __tablename__ = "daily_attendance"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    subject = Column(String, nullable=True)
    present = Column(Boolean, default=False)
    marked_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # faculty id

router = APIRouter()

# ---------- Add Student (faculty-accessible) ----------
class AddStudentRequest(BaseModel):
    name: str
    unique_id: str
    email: Optional[str] = None
    password: Optional[str] = None

@router.post("/add-student")
def add_student(data: AddStudentRequest, db: Session = Depends(get_db)):
    """Enroll a new student into the system (faculty-accessible)."""
    from app.utils.security import hash_password

    # Use roll number as default email if not provided
    email = data.email or f"{data.unique_id.lower()}@cit.ac.in"
    password = data.password or data.unique_id

    if db.query(User).filter(User.unique_id == data.unique_id).first():
        raise HTTPException(status_code=400, detail=f"Roll No '{data.unique_id}' already exists")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail=f"Email '{email}' already registered")

    student = User(
        name=data.name,
        unique_id=data.unique_id,
        email=email,
        hashed_password=hash_password(password),
        role="student",
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return {"message": f"Student '{data.name}' added successfully", "student_id": student.id}


# ---------- Pydantic ----------
class AttendanceUpdate(BaseModel):
    student_id: int
    present: bool
    date: Optional[str] = None  # YYYY-MM-DD
    subject: Optional[str] = None

class BulkAttendanceCreate(BaseModel):
    subject: str
    date: Optional[str] = None  # defaults to today
    faculty_id: Optional[int] = None


# ---------- Helpers ----------
def _parse_date(d: Optional[str]) -> date:
    return date.fromisoformat(d) if d else date.today()


def _ensure_records(db: Session, target_date: date, subject: str):
    """Create absent records for ALL students for a date+subject if not yet present."""
    students = db.query(User).filter(User.role == "student").all()
    for s in students:
        exists = db.query(DailyAttendance).filter(
            DailyAttendance.student_id == s.id,
            DailyAttendance.date == target_date,
            DailyAttendance.subject == subject,
        ).first()
        if not exists:
            db.add(DailyAttendance(student_id=s.id, date=target_date, subject=subject, present=False))
    db.commit()


# ---------- Endpoints ----------
@router.get("/daily")
def get_daily_attendance(
    subject: str = Query(...),
    target_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get full class attendance list for a given date and subject."""
    d = _parse_date(target_date)
    _ensure_records(db, d, subject)

    rows = (
        db.query(DailyAttendance, User)
        .join(User, User.id == DailyAttendance.student_id)
        .filter(DailyAttendance.date == d, DailyAttendance.subject == subject)
        .order_by(User.name)
        .all()
    )
    result = []
    for att, user in rows:
        result.append({
            "id": att.id,
            "student_id": user.id,
            "name": user.name,
            "unique_id": user.unique_id or "",
            "present": att.present,
            "date": d.isoformat(),
            "subject": att.subject,
        })
    present_count = sum(1 for r in result if r["present"])
    return {
        "date": d.isoformat(),
        "subject": subject,
        "total": len(result),
        "present": present_count,
        "absent": len(result) - present_count,
        "students": result,
    }


@router.patch("/daily/update")
def update_student_attendance(data: AttendanceUpdate, db: Session = Depends(get_db)):
    """Toggle a single student's present/absent for a specific date+subject."""
    d = _parse_date(data.date)
    record = db.query(DailyAttendance).filter(
        DailyAttendance.student_id == data.student_id,
        DailyAttendance.date == d,
        DailyAttendance.subject == data.subject,
    ).first()
    if not record:
        record = DailyAttendance(
            student_id=data.student_id, date=d,
            subject=data.subject, present=data.present
        )
        db.add(record)
    else:
        record.present = data.present
    db.commit()
    return {"message": "Updated", "present": data.present}


@router.get("/daily/dates")
def get_attendance_dates(subject: str = Query(...), db: Session = Depends(get_db)):
    """Return distinct dates that have records for a subject (for history view)."""
    dates = (
        db.query(DailyAttendance.date)
        .filter(DailyAttendance.subject == subject)
        .distinct()
        .order_by(DailyAttendance.date.desc())
        .limit(30)
        .all()
    )
    return {"dates": [d[0].isoformat() for d in dates]}


@router.post("/daily/mark-by-qr/{session_id}")
def copy_qr_to_daily(session_id: int, body: BulkAttendanceCreate, db: Session = Depends(get_db)):
    """After QR session ends, copy that session's attendance into daily_attendance table."""
    from app.models.attendance import Attendance
    from app.models.session import ClassSession

    session = db.query(ClassSession).filter(ClassSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    qr_records = db.query(Attendance).filter(Attendance.session_id == session_id).all()
    d = _parse_date(body.date)

    for rec in qr_records:
        existing = db.query(DailyAttendance).filter(
            DailyAttendance.student_id == rec.student_id,
            DailyAttendance.date == d,
            DailyAttendance.subject == body.subject,
        ).first()
        if existing:
            if rec.present:  # Only promote to present, never demote
                existing.present = True
        else:
            db.add(DailyAttendance(
                student_id=rec.student_id,
                date=d,
                subject=body.subject,
                present=rec.present,
                marked_by=body.faculty_id,
            ))
    db.commit()
    return {"message": f"Synced {len(qr_records)} QR attendance records to daily attendance"}
