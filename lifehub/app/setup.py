from dotenv import load_dotenv
from sqlmodel import SQLModel

import lifehub.lib.models  # noqa: F401
from lifehub.lib.db.base import DatabaseClient


def run():
    load_dotenv()

    client = DatabaseClient()

    try:
        SQLModel.metadata.create_all(client.engine)
    except Exception as e:
        print("Error creating database tables: ", e)


if __name__ == "__main__":
    run()
