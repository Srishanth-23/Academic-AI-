from fastapi import APIRouter
from app.ml.predict import predict_risk
from app.ml.predict_cgpa import predict_cgpa
from app.services.weak_subject_service import detect_weak_subjects
from app.services.momentum_service import calculate_momentum
from app.services.recommendation_service import generate_recommendations

router = APIRouter()


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