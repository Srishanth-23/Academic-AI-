from fastapi import APIRouter
from app.ml.predict_cgpa import predict_cgpa

router = APIRouter()


@router.post("/predict")
def cgpa_prediction(data: dict):

    attendance = data["attendance"]
    internal_marks = data["internal_marks"]
    coding_activity = data["coding_activity"]
    previous_cgpa = data["previous_cgpa"]

    result = predict_cgpa(
        attendance,
        internal_marks,
        coding_activity,
        previous_cgpa
    )

    return result