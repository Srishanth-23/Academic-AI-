from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import hash_password, verify_password, create_access_token


def register_user(db: Session, user):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return None


    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user


def login_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None


    if not verify_password(password, user.hashed_password):
        return None


    token = create_access_token({"sub": user.email})

    return token