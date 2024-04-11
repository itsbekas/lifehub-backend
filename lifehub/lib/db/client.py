import os

from sqlmodel import Session, create_engine


class DatabaseClient:
    __instance = None

    def __init__(self):
        if type(self).__instance is not None:
            raise Exception(
                f"{type(self).__name__} Database is a singleton. Use get_instance() method."
            )
        type(self).__instance = self
        db_url = os.getenv("DATABASE_URL")
        self.engine = create_engine(db_url)

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls()
        return cls.__instance

    def get_session(self):
        return Session(self.engine)
