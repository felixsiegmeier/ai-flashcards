from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from models import Flashcard

def create_flashcard(
    db: Session,
    *,
    deck_id: int,
    question: str,
    answer: str,
    hint: Optional[str] = None
) -> Flashcard:
    fc = Flashcard(
        deck_id=deck_id,
        question=question,
        answer=answer,
        hint=hint,
    )
    try:
        db.add(fc)
        db.commit()
        db.refresh(fc)
        return fc
    except SQLAlchemyError:
        db.rollback()
        raise

def get_flashcard(db: Session, flashcard_id: int) -> Optional[Flashcard]:
    return db.get(Flashcard, flashcard_id)

def list_flashcards_by_deck(
    db: Session,
    deck_id: int,
    *,
    include_soft_deleted: bool = False
) -> List[Flashcard]:
    stmt = select(Flashcard).where(Flashcard.deck_id == deck_id)
    if not include_soft_deleted:
        stmt = stmt.where(Flashcard.soft_deleted is False)
    return list(db.execute(stmt).scalars().all())

def update_flashcard(
    db: Session,
    flashcard_id: int,
    *,
    question: Optional[str] = None,
    answer: Optional[str] = None,
    hint: Optional[Optional[str]] = None,  # None = nicht ändern; "" oder Text = setzen
    soft_deleted: Optional[bool] = None
) -> Optional[Flashcard]:
    fc = db.get(Flashcard, flashcard_id)
    if not fc:
        return None

    if question is not None:
        fc.question = question
    if answer is not None:
        fc.answer = answer
    if hint is not None:
        fc.hint = hint
    if soft_deleted is not None:
        fc.soft_deleted = soft_deleted

    # updated_at aktualisieren (falls kein onupdate konfiguriert)
    fc.updated_at = func.now()

    try:
        db.commit()
        db.refresh(fc)
        return fc
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_flashcard(
    db: Session,
    flashcard_id: int,
    *,
    hard_delete: bool = False
) -> bool:
    fc = db.get(Flashcard, flashcard_id)
    if not fc:
        return False

    try:
        if hard_delete:
            db.delete(fc)
        else:
            fc.soft_deleted = True
            fc.updated_at = func.now()
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise