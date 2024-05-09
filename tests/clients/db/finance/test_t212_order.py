import uuid

import pytest

from lifehub.clients.db.finance import T212OrderDBClient
from lifehub.modules.finance.models import T212Order


@pytest.fixture(scope="module")
def user_id():
    return uuid.uuid4()


@pytest.fixture(scope="function")
def db_client(engine, user_id):
    T212Order.metadata.create_all(bind=engine)
    yield T212OrderDBClient(user_id)
    T212Order.metadata.drop_all(bind=engine)


def test_creation(db_client):
    """
    Test creating a T212OrderDBClient object
    Expected: Object is created
    """
    assert db_client
