from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from lifehub.config.constants import DATABASE_URL

engine = create_engine(DATABASE_URL)


def get_session() -> Session:
    return Session(engine)
