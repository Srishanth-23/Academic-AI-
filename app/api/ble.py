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

    detected_students = []

    for d in devices:

        device_id = d["device_id"]

        student = db.query(BLEDevice).filter(
            BLEDevice.device_id == device_id
        ).first()

        if student:

            attendance = Attendance(
                student_id=student.student_id,
                status="present",
                timestamp=datetime.utcnow()
            )

            db.add(attendance)

            detected_students.append(student.student_id)

    db.commit()

    return {
        "message": "Detection processed",
        "students_detected": detected_students
    }