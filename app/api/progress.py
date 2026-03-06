from fastapi import APIRouter
from app.services.progress_service import generate_progress

router = APIRouter()


@router.post("/trend")
def student_progress(data: dict):

    attendance_history = data["attendance_history"]
    marks_history = data["marks_history"]
    coding_history = data["coding_history"]

    result = generate_progress(
        attendance_history,
        marks_history,
        coding_history
    )

    return result