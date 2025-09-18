from ..db import Base
from sqlalchemy import Integer, Column, TIMESTAMP, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class FlashcardState(Base):
    __tablename__ = "flashcard_states"
    id = Column(Integer, primary_key=True)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    last_reviewed_at = Column(TIMESTAMP)
    due_at = Column(TIMESTAMP, nullable=False)
    repetitions = Column(Integer, nullable=False, default=0)
    intervall_days = Column(Integer, nullable=False, default=0)
    last_response_quality = Column(Integer, nullable=False, default=3)
    ease_factor = Column(Float, nullable=False, default=2.5)

    flashcard = relationship("Flashcard", back_populates="state")
    user = relationship("User", back_populates="states")


# Anmerkung: das zielt hier auf ein klassisches System ab.
# Es wäre mir aber lieber, wenn ich jeden Tag x Karten reviewen kann
# Dafür ist eine Priorität eigtl. wichtiger als ein due_date
# ich könnte ein prio-Ranking einbauen; bei gleicher Prio dann random
# dann müsste die prio einzelner Karten aber täglich neu berechnet werden 
#   (weil Zeit vergangen)

# Anmerkung: ist das nicht doppelt mit review?