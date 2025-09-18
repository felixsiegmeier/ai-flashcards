from ..db import Base
from sqlalchemy import Integer, Column, TIMESTAMP, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    reviewed_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    response_quality = Column(Integer, nullable=False, default=3)
    ease_factor = Column(Float, nullable=False, default=1)

    flashcard = relationship("Flashcard", back_populates="review")
    user = relationship("User", back_populates="reviews")

    # Anmerkung: ist das nicht doppelt mit flashcard-state?
    # Anmerkung: siehe auch Überlegung in flashcard-state zu review-System