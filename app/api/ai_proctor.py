from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class MCQRequest(BaseModel):
    studentId: str
    subject: str
    unit: int
    type: str

class VerificationSubmit(BaseModel):
    studentId: str
    subject: str
    unit: int
    score: int

@router.post("/generate-mcq")
def generate_mcq(request: MCQRequest):
    """
    Mock endpoint to generate MCQs for the syllabus tracker verification.
    """
    return [
        {
            "question": f"What is the primary concept of Unit {request.unit} in {request.subject}?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correctAnswerIndex": 0
        },
        {
            "question": f"Which of the following is true regarding {request.subject}?",
            "options": ["False statement 1", "True statement", "False statement 2", "None of the above"],
            "correctAnswerIndex": 1
        }
    ]

@router.post("/submit-verification")
def submit_verification(request: VerificationSubmit):
    """
    Mock endpoint to handle the verification score submission.
    """
    return {
        "message": f"Verification successful! Scored {request.score} on {request.subject} Unit {request.unit}."
    }
