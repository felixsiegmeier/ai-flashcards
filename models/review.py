from ..db import Base
from sqlalchemy import Integer, Column, TIMESTAMP, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)

    flashcard_id = Column(Integer, ForeignKey("flashcards.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    reviewed_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    response_quality = Column(Integer, nullable=False, default=3)
    ease_factor = Column(Float, nullable=False, default=1.0)

    flashcard = relationship("Flashcard", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

# Nützliche Indizes für Verlauf/Analytics (neueste zuerst)
Index("ix_reviews_card_reviewed_at", Review.flashcard_id, Review.reviewed_at.desc())
Index("ix_reviews_user_reviewed_at", Review.user_id, Review.reviewed_at.desc())