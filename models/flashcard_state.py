# app/models/flashcard_state.py
from sqlalchemy import (
    Column, Integer, Float, SmallInteger, ForeignKey, DateTime,
    Index, PrimaryKeyConstraint
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from db import Base  # deine declarative Base

class FlashcardState(Base):
    __tablename__ = "flashcard_states"

    # Composite Primary Key direkt an den Spalten
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    flashcard_id = Column(ForeignKey("flashcards.id", ondelete="CASCADE"), primary_key=True, nullable=False)

    last_reviewed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    repetitions = Column(Integer, nullable=False, default=0)
    last_response_quality = Column(SmallInteger, nullable=False, default=3)
    ease_factor = Column(Float, nullable=False, default=2.5)
    priority = Column(Float, nullable=False, default=0.0)

    # Beziehungen (Passe die back_populates-Namen in User/Flashcard an)
    flashcard = relationship("Flashcard", back_populates="states")
    user = relationship("User", back_populates="flashcard_states")

# Ein einzelner zusammengesetzter Index für die tägliche Auswahl:
Index("ix_fs_user_prio", FlashcardState.user_id, FlashcardState.priority)