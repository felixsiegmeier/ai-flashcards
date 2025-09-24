from db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, TIMESTAMP, Boolean, Column, ForeignKey, Text
from sqlalchemy.sql import func

class Deck(Base):
    __tablename__ = "decks"
    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    descripton = Column(String, nullable=False)
    user_intention_prompt = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    soft_deleted = Column(Boolean, nullable=False, default=False)

    flashcards = relationship("Flashcard", back_populates="deck")
    user = relationship("User", back_populates="decks")



