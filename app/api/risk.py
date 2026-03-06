from fastapi import APIRouter
from app.ml.predict import predict_risk

router = APIRouter()

@router.post("/predict")
def risk_prediction(data: dict):

    attendance = data["attendance"]
    marks = data["marks"]
    coding = data["coding"]

    result = predict_risk(
        attendance,
        marks,
        coding
    )

    return result