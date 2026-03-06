from fastapi import APIRouter
from app.services.momentum_service import calculate_momentum

router = APIRouter()


@router.post("/score")
def momentum_score(data: dict):

    attendance = data["attendance"]
    marks = data["marks"]
    coding_activity = data["coding_activity"]

    result = calculate_momentum(
        attendance,
        marks,
        coding_activity
    )

    return result