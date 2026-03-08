from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.marks import Marks
from app.models.attendance import Attendance
from app.models.coding_activity import CodingActivity
from app.models.subject import Subject
from app.models.enrollment import Enrollment
from sqlalchemy import func
from app.ml.predict import predict_risk
from app.ml.predict_cgpa import predict_cgpa
from app.services.weak_subject_service import detect_weak_subjects
from app.services.momentum_service import calculate_momentum
from app.services.recommendation_service import generate_recommendations
from app.services.notification_service import check_and_trigger_momentum_alert

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard/{student_id}")
def get_student_dashboard(student_id: int, db: Session = Depends(get_db)):
    # Verify student exists
    student = db.query(User).filter(User.id == student_id, User.role == "student").first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Fetch Attendance
    total_sessions = db.query(Attendance).filter(Attendance.student_id == student_id).count()
    present_sessions = db.query(Attendance).filter(
        Attendance.student_id == student_id,
        Attendance.present == True
    ).count()

    attendance_percentage = 0
    if total_sessions > 0:
        attendance_percentage = round((present_sessions / total_sessions) * 100, 1)

    # Fetch Marks for ML
    marks = db.query(Marks).filter(Marks.student_id == student_id).all()
    marks_list = [(m.marks_obtained / m.total_marks) * 100 for m in marks if m.total_marks > 0]
    avg_marks = sum(marks_list) / len(marks_list) if marks_list else 0

    # Subject-wise Stats
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == student_id).all()
    detailed_subjects = []
    for enr in enrollments:
        subj = db.query(Subject).filter(Subject.id == enr.subject_id).first()
        if not subj: continue
        
        # Subject Attendance
        subj_total = db.query(Attendance).filter(Attendance.student_id == student_id, Attendance.subject_id == subj.id).count()
        subj_present = db.query(Attendance).filter(Attendance.student_id == student_id, Attendance.subject_id == subj.id, Attendance.present == True).count()
        subj_att_pct = round((subj_present / subj_total * 100), 1) if subj_total > 0 else 0
        
        # Subject Marks (latest internal)
        subj_mark = db.query(Marks).filter(Marks.student_id == student_id, Marks.subject_id == subj.id).order_by(Marks.id.desc()).first()
        subj_mark_pct = round((subj_mark.marks_obtained / subj_mark.total_marks * 100), 1) if subj_mark and subj_mark.total_marks > 0 else 0
        
        detailed_subjects.append({
            "name": subj.name,
            "internalMarks": subj_mark_pct,
            "attendance": subj_att_pct
        })

    # Fetch Real Coding Activity Score
    # We'll sum the problems solved and normalize it (e.g., 100 problems = 100 score, capped at 100)
    total_problems = db.query(func.sum(CodingActivity.problems_solved)).filter(
        CodingActivity.student_id == student_id
    ).scalar() or 0
    
    # Normalize: Each 5 problems solved gives a 10 point boost to "Coding Score", max 100
    coding_activity_score = min(int((total_problems / 50) * 100), 100) if total_problems > 0 else 50 # Default 50 if none

    # Get Momentum
    momentum_data = calculate_momentum(
        attendance_percentage,
        avg_marks,
        coding_activity_score
    )
    
    momentum_score = momentum_data.get("momentum_score", 65)
    
    # Trigger AI Alerts if momentum is low
    check_and_trigger_momentum_alert(db, student_id, momentum_score)

    return {
        "student_id": student.id,
        "name": student.name,
        "score": momentum.get("momentum_score", 65),
        "trend": momentum.get("trend", "stable"),
        "attendance": attendance_percentage,
        "coding_score": coding_activity_score,
        "problems_solved": total_problems,
        "subjects": detailed_subjects or [
            {"name": 'Computer Networks', "internalMarks": 34, "attendance": 85},
            {"name": 'Operating Systems', "internalMarks": 42, "attendance": 95}
        ], # Fallback to mock only if no enrollments
        "alerts": [] 
    }


@router.post("/insight")
def student_insight(data: dict):

    attendance = data["attendance"]
    marks = data["marks"]
    coding_activity = data["coding_activity"]
    previous_cgpa = data["previous_cgpa"]
    subjects = data["subjects"]

    risk = predict_risk(attendance, marks, coding_activity)
    cgpa = predict_cgpa(attendance, marks, coding_activity, previous_cgpa)

    weak = detect_weak_subjects(subjects)

    momentum = calculate_momentum(
        attendance,
        marks,
        coding_activity
    )

    recommendations = generate_recommendations(
        weak["weak_subjects"],
        momentum["momentum_score"],
        coding_activity
    )

    return {
        "risk": risk,
        "predicted_cgpa": cgpa,
        "weak_subjects": weak["weak_subjects"],
        "momentum_score": momentum["momentum_score"],
        "trend": momentum["trend"],
        "recommendations": recommendations["recommendations"]
    }