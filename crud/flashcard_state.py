from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from sqlalchemy.exc import SQLAlchemyError
from models import FlashcardState

FlashcardKey = Tuple[int, int]  # (user_id, flashcard_id)

def create_flashcard_state(
    db: Session,
    *,
    user_id: int,
    flashcard_id: int,
    last_reviewed_at=None,
    repetitions: int = 0,
    last_response_quality: int = 3,
    ease_factor: float = 2.5,
    priority: float = 0.0,
) -> FlashcardState:
    state = FlashcardState(
        user_id=user_id,
        flashcard_id=flashcard_id,
        last_reviewed_at=last_reviewed_at,
        repetitions=repetitions,
        last_response_quality=last_response_quality,
        ease_factor=ease_factor,
        priority=priority,
    )
    try:
        db.add(state)
        db.commit()
        db.refresh(state)
        return state
    except SQLAlchemyError:
        db.rollback()
        raise

def get_flashcard_state(
    db: Session, *, user_id: int, flashcard_id: int
) -> Optional[FlashcardState]:
    return db.get(FlashcardState, {"user_id": user_id, "flashcard_id": flashcard_id})

def upsert_flashcard_state(
    db: Session,
    *,
    user_id: int,
    flashcard_id: int,
    last_reviewed_at=None,
    repetitions: Optional[int] = None,
    last_response_quality: Optional[int] = None,
    ease_factor: Optional[float] = None,
    priority: Optional[float] = None,
) -> FlashcardState:
    """
    Legt an, falls nicht vorhanden, sonst aktualisiert es selektiv die Felder.
    """
    state = get_flashcard_state(db, user_id=user_id, flashcard_id=flashcard_id)
    if state is None:
        # Defaults aus dem Model werden via create respektiert
        return create_flashcard_state(
            db,
            user_id=user_id,
            flashcard_id=flashcard_id,
            last_reviewed_at=last_reviewed_at,
            repetitions=repetitions or 0,
            last_response_quality=last_response_quality or 3,
            ease_factor=ease_factor if ease_factor is not None else 2.5,
            priority=priority if priority is not None else 0.0,
        )

    # Update-Zweig
    if last_reviewed_at is not None:
        state.last_reviewed_at = last_reviewed_at
    if repetitions is not None:
        state.repetitions = repetitions
    if last_response_quality is not None:
        state.last_response_quality = last_response_quality
    if ease_factor is not None:
        state.ease_factor = ease_factor
    if priority is not None:
        state.priority = priority

    try:
        db.commit()
        db.refresh(state)
        return state
    except SQLAlchemyError:
        db.rollback()
        raise

def update_flashcard_state(
    db: Session,
    *,
    user_id: int,
    flashcard_id: int,
    last_reviewed_at=None,
    repetitions: Optional[int] = None,
    last_response_quality: Optional[int] = None,
    ease_factor: Optional[float] = None,
    priority: Optional[float] = None,
) -> Optional[FlashcardState]:
    """
    Selektives Update eines vorhandenen Zustands.
    Gibt None zurück, wenn der Datensatz nicht existiert.
    """
    state = get_flashcard_state(db, user_id=user_id, flashcard_id=flashcard_id)
    if state is None:
        return None

    if last_reviewed_at is not None:
        state.last_reviewed_at = last_reviewed_at
    if repetitions is not None:
        state.repetitions = repetitions
    if last_response_quality is not None:
        state.last_response_quality = last_response_quality
    if ease_factor is not None:
        state.ease_factor = ease_factor
    if priority is not None:
        state.priority = priority

    try:
        db.commit()
        db.refresh(state)
        return state
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_flashcard_state(
    db: Session, *, user_id: int, flashcard_id: int
) -> bool:
    state = get_flashcard_state(db, user_id=user_id, flashcard_id=flashcard_id)
    if state is None:
        return False
    try:
        db.delete(state)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise

def list_states_for_user_by_priority(
    db: Session,
    *,
    user_id: int,
    limit: Optional[int] = None,
    descending: bool = True,
) -> List[FlashcardState]:
    """
    Liefert Zustände eines Users sortiert nach Priority.
    Standard: höchste Priorität zuerst.
    """
    stmt = select(FlashcardState).where(FlashcardState.user_id == user_id)
    stmt = stmt.order_by(
        desc(FlashcardState.priority) if descending else FlashcardState.priority
    )
    if limit is not None:
        stmt = stmt.limit(limit)
    return list(db.execute(stmt).scalars().all())