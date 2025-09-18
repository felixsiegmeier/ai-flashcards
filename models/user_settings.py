from sqlalchemy.orm import relationship
from ..db import Base
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    CheckConstraint,
    Text,
)

class UserSettings(Base):
    __tablename__ = 'user_settings'

    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    locale = Column(Text, default='de-DE', nullable=False)
    timezone = Column(Text, default='Europe/Berlin', nullable=False)
    daily_new_limit = Column(Integer, default=20, nullable=False)
    daily_review_limit = Column(Integer, default=200, nullable=False)
    theme = Column(
        Text,
        default='system',
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "theme IN ('light', 'dark', 'system')",
            name='check_theme_valid'
        ),
    )

    user = relationship("User", back_populates="settings")