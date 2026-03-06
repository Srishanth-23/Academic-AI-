from sqlalchemy.orm import Session
from app.models.student_device import StudentDevice


def register_device(db: Session, student_id: int, device_id: str, device_model: str):

    device = StudentDevice(
        student_id=student_id,
        device_id=device_id,
        device_model=device_model
    )

    db.add(device)

    db.commit()

    db.refresh(device)

    return device