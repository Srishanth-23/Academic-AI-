from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from app.database import SessionLocal
from app.models.user import User, ParentStudent
from app.models.marks import Marks
from app.models.attendance import Attendance

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard/{parent_id}")
def parent_dashboard(parent_id: int, db: Session = Depends(get_db)):
    """
    Fetch dashboard data for a parent.
    Returns linked student details, marks, and attendance stats.
    """
    # 1. Verify parent exists
    parent = db.query(User).filter(User.id == parent_id, User.role == "parent").first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")

    # 2. Find linked students
    links = db.query(ParentStudent).filter(ParentStudent.parent_id == parent_id).all()
    if not links:
        return {"message": "No linked students found", "students": []}

    student_data = []
    
    for link in links:
        student = db.query(User).filter(User.id == link.student_id).first()
        if not student:
            continue
            
        # Fetch Marks
        marks = db.query(Marks).filter(Marks.student_id == student.id).all()
        marks_summary = [{"subject_id": m.subject_id, "score": m.marks_obtained, "max": m.total_marks} for m in marks]
        
        # Calculate overall attendance percentage efficiently
        # Assuming we just need present / total
        total_sessions = db.query(Attendance).filter(Attendance.student_id == student.id).count()
        present_sessions = db.query(Attendance).filter(
            Attendance.student_id == student.id, 
            Attendance.present == True
        ).count()
        
        attendance_percentage = 0
        if total_sessions > 0:
            attendance_percentage = round((present_sessions / total_sessions) * 100, 1)

        # In a real app we'd query the DB or call `predict_risk` from `app.ml.predict`
        # Using a mockup score to reflect the dashboard structure for now.
        risk_level = "Low"
        if attendance_percentage < 75:
            risk_level = "High"

        student_data.append({
            "student_id": student.id,
            "name": student.name,
            "overall_attendance": attendance_percentage,
            "marks_summary": marks_summary,
            "risk_level": risk_level,
        })

    return {
        "parent_name": parent.name,
        "students": student_data
    }
