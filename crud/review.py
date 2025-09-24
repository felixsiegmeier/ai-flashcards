from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, desc, TIMESTAMP
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from models import Review

def create_review(
    db: Session,
    *,
    flashcard_id: int,
    user_id: int,
    response_quality: int = 3,
    ease_factor: float = 1.0,
    reviewed_at=None  # Optional: überschreiben, sonst server_default=now()
) -> Review:
    rv = Review(
        flashcard_id=flashcard_id,
        user_id=user_id,
        response_quality=response_quality,
        ease_factor=ease_factor,
    )
    if reviewed_at is not None:
        rv.reviewed_at = reviewed_at

    try:
        db.add(rv)
        db.commit()
        db.refresh(rv)
        return rv
    except SQLAlchemyError:
        db.rollback()
        raise

def get_review(db: Session, review_id: int) -> Optional[Review]:
    return db.get(Review, review_id)

def list_reviews_by_flashcard(
    db: Session,
    flashcard_id: int,
    *,
    limit: Optional[int] = None
) -> List[Review]:
    stmt = (
        select(Review)
        .where(Review.flashcard_id == flashcard_id)
        .order_by(desc(Review.reviewed_at))
    )
    if limit is not None:
        stmt = stmt.limit(limit)
    return list(db.execute(stmt).scalars().all())

def list_reviews_by_user(
    db: Session,
    user_id: int,
    *,
    limit: Optional[int] = None
) -> List[Review]:
    stmt = (
        select(Review)
        .where(Review.user_id == user_id)
        .order_by(desc(Review.reviewed_at))
    )
    if limit is not None:
        stmt = stmt.limit(limit)
    return list(db.execute(stmt).scalars().all())

def update_review(
    db: Session,
    review_id: int,
    *,
    response_quality: Optional[int] = None,
    ease_factor: Optional[float] = None,
    reviewed_at: Optional[TIMESTAMP] = None  # None = nicht ändern; Wert = setzen
) -> Optional[Review]:
    rv = db.get(Review, review_id)
    if not rv:
        return None

    if response_quality is not None:
        rv.response_quality = response_quality
    if ease_factor is not None:
        rv.ease_factor = ease_factor
    if reviewed_at is not None:
        rv.reviewed_at = reviewed_at

    try:
        db.commit()
        db.refresh(rv)
        return rv
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_review(db: Session, review_id: int) -> bool:
    """
    Hard-Delete: Es gibt kein soft_deleted-Feld im Review-Model.
    """
    rv = db.get(Review, review_id)
    if not rv:
        return False

    try:
        db.delete(rv)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise