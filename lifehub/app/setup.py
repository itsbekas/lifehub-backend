import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

import lifehub.models  # noqa: F401

# from lifehub.config.providers import setup_providers
from lifehub.models.base import BaseModel


def run():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url, echo=True)

    # setup_providers()
    BaseModel.metadata.create_all(engine)


if __name__ == "__main__":
    run()
