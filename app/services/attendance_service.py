from sqlalchemy.orm import Session
from app.models.session import ClassSession
from app.models.attendance import Attendance
from sqlalchemy import func


def create_session(db: Session, session_data):

    session = ClassSession(
        subject_id=session_data.subject_id,
        faculty_id=session_data.faculty_id
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def mark_attendance(db: Session, data):

    attendance = Attendance(
        session_id=data.session_id,
        student_id=data.student_id,
        present=True
    )

    db.add(attendance)
    db.commit()

    return {"message": "Attendance marked"} 

def get_subject_attendance(db: Session, student_id: int, subject_id: int):
    
    total_classes = (
        db.query(ClassSession)
        .filter(ClassSession.subject_id == subject_id)
        .count()
    )

    attended = (
        db.query(Attendance)
        .join(ClassSession, Attendance.session_id == ClassSession.id)
        .filter(
            Attendance.student_id == student_id,
            ClassSession.subject_id == subject_id,
            Attendance.present == True
        )
        .count()
    )

    percentage = 0
    if total_classes > 0:
        percentage = (attended / total_classes) * 100

    return {
        "student_id": student_id,
        "subject_id": subject_id,
        "total_classes": total_classes,
        "attended": attended,
        "attendance_percentage": round(percentage, 2)
    }


def get_overall_attendance(db: Session, student_id: int):

    total_classes = (
        db.query(Attendance)
        .filter(Attendance.student_id == student_id)
        .count()
    )

    attended = (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student_id,
            Attendance.present == True
        )
        .count()
    )

    percentage = 0
    if total_classes > 0:
        percentage = (attended / total_classes) * 100

    return {
        "student_id": student_id,
        "total_classes": total_classes,
        "attended": attended,
        "overall_attendance": round(percentage, 2)
    }