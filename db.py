from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

# exportiert Base für die Modelle
Base = declarative_base()

# exportiert session für crud
Session = sessionmaker(bind=engine)
session = Session()
