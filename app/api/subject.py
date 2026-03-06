from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.subject import SubjectCreate
from app.services.subject_service import create_subject, get_subjects
from app.dependencies import get_db


router = APIRouter()


@router.post("/create")
def create_new_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    return create_subject(db, subject)


@router.get("/")
def list_subjects(db: Session = Depends(get_db)):
    return get_subjects(db)