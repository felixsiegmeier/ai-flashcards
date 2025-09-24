from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from models import FlashcardMedia

def create_flashcard_media(
    db: Session,
    *,
    flashcard_id: int,
    type: str,
    url: str,
    caption: Optional[str] = None
) -> FlashcardMedia:
    media = FlashcardMedia(
        flashcard_id=flashcard_id,
        type=type,
        url=url,
        caption=caption,
    )
    try:
        db.add(media)
        db.commit()
        db.refresh(media)
        return media
    except SQLAlchemyError:
        db.rollback()
        raise

def get_flashcard_media(db: Session, media_id: int) -> Optional[FlashcardMedia]:
    return db.get(FlashcardMedia, media_id)

def list_flashcard_media_by_flashcard(
    db: Session,
    flashcard_id: int,
    *,
    media_type: Optional[str] = None
) -> List[FlashcardMedia]:
    stmt = select(FlashcardMedia).where(FlashcardMedia.flashcard_id == flashcard_id)
    if media_type is not None:
        stmt = stmt.where(FlashcardMedia.type == media_type)
    return list(db.execute(stmt).scalars().all())

def update_flashcard_media(
    db: Session,
    media_id: int,
    *,
    type: Optional[str] = None,
    url: Optional[str] = None,
    caption: Optional[Optional[str]] = None  # None = nicht ändern; ""/Text = setzen
) -> Optional[FlashcardMedia]:
    media = db.get(FlashcardMedia, media_id)
    if not media:
        return None

    if type is not None:
        media.type = type
    if url is not None:
        media.url = url
    if caption is not None:
        media.caption = caption

    try:
        db.commit()
        db.refresh(media)
        return media
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_flashcard_media(db: Session, media_id: int) -> bool:
    media = db.get(FlashcardMedia, media_id)
    if not media:
        return False
    try:
        db.delete(media)
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise