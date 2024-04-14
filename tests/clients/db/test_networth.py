import uuid

import pytest

from lifehub.clients.db.networth import NetworthDBClient
from lifehub.models.finance import Networth


@pytest.fixture(scope="module")
def user_id():
    return uuid.uuid4()


@pytest.fixture(scope="function")
def db_client(engine):
    Networth.metadata.create_all(bind=engine)
    yield NetworthDBClient(user_id)
    Networth.metadata.drop_all(bind=engine)


def test_creation(user_id):
    """
    Test creating a NetworthDBClient object
    Expected: Object is created
    """
    assert NetworthDBClient(user_id)
