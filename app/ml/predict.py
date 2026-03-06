import joblib
import numpy as np

model = joblib.load("app/ml/model.pkl")

def predict_risk(attendance, marks, coding):

    features = np.array([
        attendance,
        marks,
        coding
    ]).reshape(1, -1)

    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0][1]

    if prediction == 1:
        status = "HIGH RISK"
    else:
        status = "SAFE"

    return {
        "risk_status": status,
        "risk_probability": float(probability)
    }