from sqlalchemy.orm import Session
from app.models.subject import Subject


def create_subject(db: Session, subject):

    new_subject = Subject(
        name=subject.name,
        code=subject.code,
        faculty_id=subject.faculty_id
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject


def get_subjects(db: Session):
    return db.query(Subject).all()