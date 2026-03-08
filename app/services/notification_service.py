from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.models.user import User, ParentStudent

def create_notification(db: Session, user_id: int, title: str, message: str, type: str):
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=type
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def check_and_trigger_momentum_alert(db: Session, student_id: int, score: float):
    if score < 60:
        student = db.query(User).filter(User.id == student_id).first()
        if not student: return
        
        # Notify student
        create_notification(
            db, student_id, 
            "Academic Momentum Alert", 
            f"Your academic momentum score has dropped to {score}. Let's work on a recovery plan with your AI coach!",
            "MOMENTUM_ALERT"
        )
        
        # Notify Class Advisor
        if student.section and student.section.advisors:
            for advisor in student.section.advisors:
                create_notification(
                    db, advisor.id,
                    f"Low Momentum Alert: {student.name}",
                    f"Student {student.name} ({student.unique_id}) in {student.section.name} has a low momentum score of {score}.",
                    "MOMENTUM_ALERT"
                )
        
        # Notify Parents
        parents = db.query(User).join(ParentStudent, User.id == ParentStudent.parent_id)\
            .filter(ParentStudent.student_id == student_id).all()
        for parent in parents:
            create_notification(
                db, parent.id,
                f"Academic Alert: {student.name}",
                f"Your ward {student.name}'s academic momentum score is currently {score}. We recommend discussing this with their mentor.",
                "MOMENTUM_ALERT"
            )
