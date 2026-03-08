from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.ble_device import BLEDevice
from app.models.attendance import Attendance
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/detect")
def detect_devices(payload: dict, db: Session = Depends(get_db)):

    scanner_id = payload.get("scanner_id")
    devices = payload.get("devices")
    session_id = payload.get("session_id") # Must be provided by the scanner app

    if not session_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="session_id is required")

    detected_students = []

    for d in devices:
        device_id = d["device_id"]
        student_device = db.query(BLEDevice).filter(BLEDevice.device_id == device_id).first()

        if student_device:
            # Check if student is already marked present for this session
            existing_attendance = db.query(Attendance).filter(
                Attendance.session_id == session_id,
                Attendance.student_id == student_device.student_id
            ).first()

            if existing_attendance:
                # Already present, just update present flag to True if it was False
                if not existing_attendance.present:
                    existing_attendance.present = True
            else:
                # Create new attendance record
                attendance = Attendance(
                    session_id=session_id,
                    student_id=student_device.student_id,
                    present=True
                )
                db.add(attendance)

            detected_students.append(student_device.student_id)

    db.commit()

    return {
        "message": "Detection processed",
        "students_detected": detected_students
    }