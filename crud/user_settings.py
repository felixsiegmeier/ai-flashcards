from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import UserSettings

def create_user_settings(
        db: Session,
        *,
        user_id: int,
        locale: Optional[str] = "de-DE",
        timezone: Optional[str] = "Europe/Berlin",
        daily_new_limit: Optional[int] = 20,
        daily_review_limit: Optional[int] = 200,
        theme: Optional[str] = "system",
    ) -> UserSettings:
    existing = db.get(UserSettings, user_id)
    if existing:
        return existing
    obj = UserSettings(
        user_id=user_id,
        locale=locale,
        timezone=timezone,
        daily_new_limit=daily_new_limit,
        daily_review_limit=daily_review_limit,
        theme=theme,
    )
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except SQLAlchemyError:
        db.rollback()
        raise

def get_user_settings(db: Session, *, user_id: int) -> Optional[UserSettings]:
    return db.get(UserSettings, user_id)

def update_user_settings(
        db: Session,
        *,
        user_id: int,
        locale: Optional[str] = None,
        timezone: Optional[str] = None,
        daily_new_limit: Optional[int] = None,
        daily_review_limit: Optional[int] = None,
        theme: Optional[str] = None,
    ) -> Optional[UserSettings]:
    obj = db.get(UserSettings, user_id)
    if not obj:
        return None
    if locale is not None:
        obj.locale = locale
    if timezone is not None:
        obj.timezone = timezone
    if daily_new_limit is not None:
        obj.daily_new_limit = daily_new_limit
    if daily_review_limit is not None:
        obj.daily_review_limit = daily_review_limit
    if theme is not None:
        obj.theme = theme
    try:
        db.commit()
        db.refresh(obj)
        return obj
    except SQLAlchemyError:
        db.rollback()
        raise