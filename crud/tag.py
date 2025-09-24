from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from models import Tag, Flashcard

# -------------------
# Basis-CRUD für Tags
# -------------------

def create_tag(db: Session, *, name: str) -> Tag:
    tag = Tag(name=name)
    try:
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag
    except SQLAlchemyError:
        db.rollback()
        raise

def get_tag(db: Session, tag_id: int) -> Optional[Tag]:
    return db.get(Tag, tag_id)

def get_tag_by_name(db: Session, name: str) -> Optional[Tag]:
    return db.execute(select(Tag).where(Tag.name == name)).scalar_one_or_none()

def list_tags(db: Session, *, q: Optional[str] = None, limit: Optional[int] = None) -> List[Tag]:
    stmt = select(Tag)
    if q:
        # einfacher "contains" Filter; für Postgres ohne ILIKE hier basic contains
        stmt = stmt.where(Tag.name.contains(q))
    if limit is not None:
        stmt = stmt.limit(limit)
    return list(db.execute(stmt).scalars().all())

def update_tag(db: Session, tag_id: int, *, name: Optional[str] = None) -> Optional[Tag]:
    tag = db.get(Tag, tag_id)
    if not tag:
        return None

    if name is not None:
        tag.name = name

    try:
        db.commit()
        db.refresh(tag)
        return tag
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_tag(db: Session, tag_id: int) -> bool:
    tag = db.get(Tag, tag_id)
    if not tag:
        return False
    try:
        db.delete(tag)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise

# --------------------------------------
# Helper für Beziehungen zu Flashcards
# --------------------------------------

def list_tags_for_flashcard(db: Session, flashcard_id: int) -> List[Tag]:
    fc = db.get(Flashcard, flashcard_id)
    if not fc:
        return []
    # Bei lazy="selectin" sind Tags effizient ladbar
    return list(fc.tags)

def add_tag_to_flashcard(db: Session, *, flashcard_id: int, tag_id: int) -> bool:
    fc = db.get(Flashcard, flashcard_id)
    tag = db.get(Tag, tag_id)
    if not fc or not tag:
        return False

    if tag not in fc.tags:
        fc.tags.append(tag)
        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise
    return True

def remove_tag_from_flashcard(db: Session, *, flashcard_id: int, tag_id: int) -> bool:
    fc = db.get(Flashcard, flashcard_id)
    tag = db.get(Tag, tag_id)
    if not fc or not tag:
        return False

    if tag in fc.tags:
        fc.tags.remove(tag)
        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise
    return True

def replace_tags_for_flashcard(db: Session, *, flashcard_id: int, tag_ids: List[int]) -> bool:
    """
    Ersetzt alle Tags der Flashcard durch die angegebenen tag_ids.
    Nicht vorhandene IDs werden ignoriert.
    """
    fc = db.get(Flashcard, flashcard_id)
    if not fc:
        return False

    new_tags = []
    for tid in tag_ids:
        t = db.get(Tag, tid)
        if t:
            new_tags.append(t)

    fc.tags = new_tags
    try:
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise

def list_flashcards_by_tag(db: Session, *, tag_id: int) -> List[Flashcard]:
    tag = db.get(Tag, tag_id)
    if not tag:
        return []
    return list(tag.flashcards)