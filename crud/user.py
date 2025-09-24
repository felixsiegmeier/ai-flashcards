# app/crud/user.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from models import User

def create_user(db: Session, *, username: str, email: str, hashed_password: str) -> User:
    user = User(username=username, email=email, hashed_password=hashed_password)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError:
        db.rollback()
        raise

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

def update_user(db: Session, user_id: int, *, username: Optional[str] = None, email: Optional[str] = None) -> Optional[User]:
    user = db.get(User, user_id)
    if not user:
        return None
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    try:
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(User, user_id)
    if not user:
        return False
    try:
        db.delete(user)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise