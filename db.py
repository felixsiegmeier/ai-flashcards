# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

# Für FastAPI (oder andere DI), liefert per yield und schließt IMMER
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()