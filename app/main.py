from fastapi import FastAPI
from app.database import Base, engine

from app.api import auth
from app.api import subject
from app.api import attendance
from app.api import marks
from app.api import coding
from app.api import risk
from app.api import cgpa
from app.api import weak_subject
from app.api import momentum
from app.api import recommendation
from app.api import student_insight
from app.api import progress
from app.api import device
from app.api import ble


from app.models import user
from app.models import subject as subject_model
from app.models import enrollment
from app.models import attendance as attendance_model
from app.models import session
from app.models import marks as marks_model
from app.models import coding_profile
from app.models import coding_activity
from app.models import contest_history
from app.models import coding_skills



app = FastAPI(
    title="Academic AI Backend",
    version="1.0"
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine, checkfirst=True)


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(subject.router, prefix="/subjects", tags=["Subjects"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
app.include_router(marks.router, prefix="/marks", tags=["Marks"])
app.include_router(coding.router, prefix="/coding", tags=["Coding"])

app.include_router(risk.router, prefix="/risk", tags=["Risk Prediction"])
app.include_router(cgpa.router, prefix="/cgpa", tags=["CGPA Prediction"])
app.include_router(weak_subject.router, prefix="/weak-subject", tags=["Weak Subject Detection"])

app.include_router(momentum.router, prefix="/momentum", tags=["Momentum Score"])
app.include_router(recommendation.router, prefix="/recommendation", tags=["AI Study Recommendation"])
app.include_router(student_insight.router, prefix="/student", tags=["Student Insight"])
app.include_router(progress.router, prefix="/progress", tags=["Student Progress"])
app.include_router(device.router, prefix="/device", tags=["Device"])
app.include_router(ble.router, prefix="/ble", tags=["BLE Scanner"])

@app.get("/")
def home():
    return {"message": "Academic Intelligence Platform Running"}