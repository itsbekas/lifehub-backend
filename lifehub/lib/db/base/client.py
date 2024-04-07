import os

from sqlmodel import Session, create_engine


class DatabaseClient:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL")
        self.engine = create_engine(db_url)

    def get_session(self):
        return Session(self.engine)
