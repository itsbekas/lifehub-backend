import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

import lifehub.models  # noqa: F401
from lifehub.models.base import BaseModel


def run():
    """
    Warning: This function will drop all tables and recreate them
    This is only for development purposes
    """
    input(
        "This will drop all tables in the database. Press Enter to continue or Ctrl+C to exit"
    )

    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url, echo=True)

    BaseModel.metadata.drop_all(engine)


if __name__ == "__main__":
    run()
