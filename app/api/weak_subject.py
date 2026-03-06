from fastapi import APIRouter
from app.services.weak_subject_service import detect_weak_subjects

router = APIRouter()


@router.post("/detect")
def weak_subject_detection(data: dict):

    subjects = data["subjects"]

    result = detect_weak_subjects(subjects)

    return result