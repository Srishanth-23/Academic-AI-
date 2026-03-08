from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.dependencies import get_db
from app.models.user import User
from app.models.subject import Subject
from app.models.attendance import Attendance
from app.models.marks import Marks

router = APIRouter()

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    """
    Get system-wide statistics for the admin dashboard.
    """
    try:
        total_users = db.query(User).count()
        students = db.query(User).filter(User.role == 'student').count()
        faculty = db.query(User).filter(User.role == 'faculty').count()
        hods = db.query(User).filter(User.role == 'hod').count()
        parents = db.query(User).filter(User.role == 'parent').count()
        
        total_subjects = db.query(Subject).count()
        total_attendance_logs = db.query(Attendance).count()
        total_marks_recorded = db.query(Marks).count()
        
        return {
            "overview": {
                "total_users": total_users,
                "students": students,
                "faculty": faculty,
                "hods": hods,
                "parents": parents
            },
            "system": {
                "subjects": total_subjects,
                "attendance_logs": total_attendance_logs,
                "marks": total_marks_recorded
            },
            "status": "Healthy"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users")
def list_users(role: Optional[str] = None, db: Session = Depends(get_db)):
    """
    List all users with optional role filtering.
    """
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    
    users = query.all()
    return [{
        "id": u.id,
        "unique_id": u.unique_id,
        "name": u.name,
        "email": u.email,
        "role": u.role
    } for u in users]
