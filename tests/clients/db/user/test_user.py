import pytest

from lifehub.clients.db.user import UserDBClient
from lifehub.models.user_old import User


@pytest.fixture(scope="function")
def db_client(engine):
    User.metadata.create_all(bind=engine)
    yield UserDBClient()
    User.metadata.drop_all(bind=engine)


def test_creation(db_client):
    """
    Test creating a UserBaseDBClient object
    Expected: Object is created
    """
    assert db_client
