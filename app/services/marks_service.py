from sqlalchemy.orm import Session
from app.models.marks import Marks


def add_marks(db: Session, data):

    mark = Marks(
        student_id=data.student_id,
        subject_id=data.subject_id,
        assessment_type=data.assessment_type,
        score=data.score,
        max_score=data.max_score
    )

    db.add(mark)
    db.commit()
    db.refresh(mark)

    return mark


def get_student_marks(db: Session, student_id: int):

    marks = db.query(Marks).filter(
        Marks.student_id == student_id
    ).all()

    return marks