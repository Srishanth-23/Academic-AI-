from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.attendance import Attendance
from app.models.session import ClassSession
from app.models.user import User
from app.models.enrollment import Enrollment
from app.schemas.attendance_override import UpdateAttendanceRequest

from app.models.section import Section

def get_class_roster_attendance(db: Session, session_id: int, section_id: int = None):
    # Get session
    session = db.query(ClassSession).filter(ClassSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    # Get all students enrolled in this subject, filtered by section if provided
    query = db.query(User).join(Enrollment, User.id == Enrollment.student_id)\
        .filter(Enrollment.subject_id == session.subject_id, User.role == "student")
    
    if section_id:
        query = query.filter(User.section_id == section_id)
        
    enrolled_students = query.all()
        
    # Get attendance records for this session
    attendance_records = db.query(Attendance).filter(Attendance.session_id == session_id).all()
    
    # Map attendance by student_id
    attendance_map = {r.student_id: r.present for r in attendance_records}
    
    roster = []
    present_count = 0
    absent_count = 0
    
    for student in enrolled_students:
        is_present = attendance_map.get(student.id, False) # Default to False if no scan
        if is_present:
            present_count += 1
        else:
            absent_count += 1
            
        roster.append({
            "student_id": student.id,
            "name": student.name,
            "present": is_present,
            "section_name": student.section.name if student.section else "N/A"
        })
        
    return {
        "session_id": session_id,
        "subject_id": session.subject_id,
        "section_id": section_id,
        "present_count": present_count,
        "absent_count": absent_count,
        "roster": roster
    }

def update_class_attendance(db: Session, request: UpdateAttendanceRequest, faculty_id: int):
    # Verify faculty is class advisor
    faculty = db.query(User).filter(User.id == faculty_id).first()
    if not faculty or not faculty.is_class_advisor:
        raise HTTPException(status_code=403, detail="Only class advisors can manually edit attendance")
        
    session = db.query(ClassSession).filter(ClassSession.id == request.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    updated_records = 0
    
    for override in request.overrides:
        record = db.query(Attendance).filter(
            Attendance.session_id == request.session_id,
            Attendance.student_id == override.student_id
        ).first()
        
        if record:
            record.present = override.present
        else:
            # Create a manual record if they weren't scanned at all
            new_record = Attendance(
                session_id=request.session_id,
                student_id=override.student_id,
                present=override.present
            )
            db.add(new_record)
        
        updated_records += 1
            
    db.commit()
    return {"message": f"Successfully updated {updated_records} attendance records"}
