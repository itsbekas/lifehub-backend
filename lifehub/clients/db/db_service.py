import os

from sqlmodel import Session, create_engine


class DatabaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            db_url = os.getenv("DATABASE_URL")
            cls._instance.engine = create_engine(db_url)
        return cls._instance

    def get_session(self):
        return Session(self.engine)
