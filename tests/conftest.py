import os

import pytest
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, MetaData

from lifehub.models.user import User
import lifehub.models # noqa: F401


# Load the environment 
load_dotenv("test.env")
testing_flag = os.getenv("TESTING")
if testing_flag is None or testing_flag != "True":
    raise ValueError("TESTING flag must be set to True in test.env")

@pytest.fixture(scope="session", autouse=True)
def setup_session():
    # Setup the database
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url)
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print("Error creating database tables: ", e)
    
    yield

    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def db_session(db):
    return db.get_session()


@pytest.fixture(scope="session")
def user1():
    return User(username="user1", password="password1", name="User One")


@pytest.fixture(scope="session")
def user2():
    return User(username="user2", password="password2", name="User Two")
