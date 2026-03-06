from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal
from app.services.device_service import register_device


router = APIRouter()


class DeviceRegister(BaseModel):

    student_id: int

    device_id: str

    device_model: str


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/register-device")

def register_student_device(data: DeviceRegister, db: Session = Depends(get_db)):

    device = register_device(
        db,
        data.student_id,
        data.device_id,
        data.device_model
    )

    return {
        "message": "Device registered successfully",
        "device_id": device.device_id
    }