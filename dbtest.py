# test.py
from sqlalchemy import event
from db import Base, engine, SessionLocal
from models import User, Deck
from crud import create_user, get_user, update_user, create_user_settings

# SQLite: Foreign Keys einschalten
@event.listens_for(engine, "connect")
def _fk_pragma(dbapi_conn, conn_record):
    cur = dbapi_conn.cursor()
    cur.execute("PRAGMA foreign_keys=ON")
    cur.close()

with SessionLocal() as db:
    pass