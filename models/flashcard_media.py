from db import Base
from sqlalchemy import Integer, String, Column, ForeignKey, Text
from sqlalchemy.orm import relationship

class FlashcardMedia(Base):
    __tablename__ = "flashcard_medias"
    id = Column(Integer, primary_key=True, nullable=False)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id", ondelete='CASCADE'), nullable=False)
    type = Column(String, nullable=False)
    url = Column(Text, nullable=False)
    caption = Column(Text)

    flashcard = relationship("Flashcard", back_populates="medias")