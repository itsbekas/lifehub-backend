import os

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv("test.env")
    testing_flag = os.getenv("TESTING")
    if testing_flag is None or testing_flag != "True":
        raise ValueError("TESTING flag must be set to True in test.env")


@pytest.fixture(scope="session")
def db():
    from lifehub.clients.db.db_service import DatabaseClient

    return DatabaseClient.get_instance()


@pytest.fixture(scope="session")
def db_session(db):
    return db.get_session()
