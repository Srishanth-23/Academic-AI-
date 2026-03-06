from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.marks import MarksCreate
from app.services.marks_service import add_marks, get_student_marks
from app.dependencies import get_db


router = APIRouter()


@router.post("/add")
def add_student_marks(data: MarksCreate, db: Session = Depends(get_db)):
    return add_marks(db, data)


@router.get("/student/{student_id}")
def get_marks(student_id: int, db: Session = Depends(get_db)):
    return get_student_marks(db, student_id)