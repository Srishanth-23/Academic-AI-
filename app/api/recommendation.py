from fastapi import APIRouter
from app.services.recommendation_service import generate_recommendations

router = APIRouter()


@router.post("/study-plan")
def study_recommendations(data: dict):

    weak_subjects = data["weak_subjects"]
    momentum_score = data["momentum_score"]
    coding_activity = data["coding_activity"]

    result = generate_recommendations(
        weak_subjects,
        momentum_score,
        coding_activity
    )

    return result