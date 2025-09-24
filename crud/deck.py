from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from models import Deck

def create_deck(
    db: Session,
    *,
    user_id: int,
    title: str,
    descripton: str,
    user_intention_prompt: Optional[str] = None
) -> Deck:
    deck = Deck(
        user_id=user_id,
        title=title,
        descripton=descripton,
        user_intention_prompt=user_intention_prompt
    )
    try:
        db.add(deck)
        db.commit()
        db.refresh(deck)
        return deck
    except SQLAlchemyError:
        db.rollback()
        raise

def get_deck(db: Session, deck_id: int) -> Optional[Deck]:
    return db.get(Deck, deck_id)

def update_deck(
    db: Session,
    deck_id: int,
    *,
    title: Optional[str] = None,
    descripton: Optional[str] = None,
    user_intention_prompt: Optional[Optional[str]] = None,
    soft_deleted: Optional[bool] = None
) -> Optional[Deck]:
    """
    user_intention_prompt: Optional[Optional[str]]
    - None  -> Feld nicht ändern
    - ""    -> auf leeren String setzen
    - "..." -> auf diesen String setzen
    """
    deck = db.get(Deck, deck_id)
    if not deck:
        return None

    if title is not None:
        deck.title = title
    if descripton is not None:
        deck.descripton = descripton
    if user_intention_prompt is not None:
        deck.user_intention_prompt = user_intention_prompt
    if soft_deleted is not None:
        deck.soft_deleted = soft_deleted

    # updated_at aktualisieren (falls nicht via onupdate im Model konfiguriert)
    deck.updated_at = func.now()

    try:
        db.commit()
        db.refresh(deck)
        return deck
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_deck(db: Session, deck_id: int, *, hard_delete: bool = False) -> bool:
    """
    hard_delete=False -> Soft-Delete (soft_deleted=True)
    hard_delete=True  -> Physisch löschen
    """
    deck = db.get(Deck, deck_id)
    if not deck:
        return False

    try:
        if hard_delete:
            db.delete(deck)
        else:
            deck.soft_deleted = True
            deck.updated_at = func.now()
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise