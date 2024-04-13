import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

import lifehub.models  # noqa: F401


def run():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)

    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print("Error creating database tables: ", e)


if __name__ == "__main__":
    run()
