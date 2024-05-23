from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from lifehub.config.constants import DATABASE_URL


class DatabaseService:
    _instance: DatabaseService | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_engine(DATABASE_URL)
        return cls._instance

    def get_session(self):
        return Session(self.engine)


def get_session():
    return DatabaseService().get_session()
