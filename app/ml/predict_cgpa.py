import joblib
import numpy as np

model = joblib.load("app/ml/cgpa_model.pkl")


def predict_cgpa(attendance, internal_marks, coding_activity, previous_cgpa):

    features = np.array([
        attendance,
        internal_marks,
        coding_activity,
        previous_cgpa
    ]).reshape(1, -1)

    prediction = model.predict(features)[0]

    return {
        "predicted_cgpa": round(float(prediction), 2)
    }