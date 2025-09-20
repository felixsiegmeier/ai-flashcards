from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

flashcard_tags = Table(
    "flashcard_tags",
    Base.metadata,
    Column("flashcard_id", Integer, ForeignKey("flashcards.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    flashcards = relationship(
        "Flashcard",
        secondary=flashcard_tags,
        back_populates="tags",
        lazy="selectin",
    )
