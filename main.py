# test.py
from sqlalchemy import event
from db import Base, engine, SessionLocal
from models import User, Deck
from crud import create_user

# SQLite: Foreign Keys einschalten
@event.listens_for(engine, "connect")
def _fk_pragma(dbapi_conn, conn_record):
    cur = dbapi_conn.cursor()
    cur.execute("PRAGMA foreign_keys=ON")
    cur.close()

def main():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        user = create_user(db=db, username="Felix", email="felixMail", hashed_password="12345")
        print(user.id, user.username, user.email)

if __name__ == "__main__":
    main()