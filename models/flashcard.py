from ..db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, TIMESTAMP, Boolean, Column, ForeignKey, Text
from sqlalchemy.sql import func

class Flashcard():
    __tablename__ = "flashcards"
    id = Column(Integer, nullable=False, primary_key=True)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    hint = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    soft_deleted = Column(Boolean, nullable=False, default=False)

    deck = relationship("Deck", back_populates="flashcards")
    medias = relationship("FlashcardMedia", back_populates="flashcard")
    review = relationship("Review", back_populates="flashcard")
    state = relationship("FlashcardState", back_populates="flashcard")
