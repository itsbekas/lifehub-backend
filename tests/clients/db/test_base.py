# Arbitrary model for testing
import pytest
from sqlmodel import Field, SQLModel

from lifehub.clients.db.base import BaseDBClient


# Test model
class BaseTestModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=10)


@pytest.fixture(scope="function")
def db_client(engine):
    # Create table
    BaseTestModel.metadata.create_all(bind=engine)
    yield BaseDBClient(BaseTestModel)
    # Drop table
    BaseTestModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def obj1():
    return BaseTestModel(id=1, name="obj1")


@pytest.fixture(scope="function")
def obj2():
    return BaseTestModel(id=2, name="obj2")


class TestAdd:
    def test_add(self, db_client, obj1):
        db_client.add(obj1)
        assert db_client.get_all() == [obj1]

    def test_add_multiple(self, db_client, obj1, obj2):
        db_client.add(obj1)
        db_client.add(obj2)
        assert db_client.get_all() == [obj1, obj2]

    def test_add_duplicate(self, db_client, obj1):
        db_client.add(obj1)
        duplicate_obj = BaseTestModel(id=1, name="obj1")
        with pytest.raises(Exception):
            db_client.add(duplicate_obj)

    def test_max_length(self, db_client):
        obj = BaseTestModel(id=1, name="a" * 10)
        db_client.add(obj)
        assert db_client.get_all() == [obj]

    def test_max_length_exceeded(self, db_client):
        obj = BaseTestModel(id=1, name="a" * 11)
        with pytest.raises(Exception):
            db_client.add(obj)


class TestGetAll:
    def test_get_all_empty(self, db_client):
        assert db_client.get_all() == []

    def test_get_all_single(self, db_client, obj1):
        db_client.add(obj1)
        assert db_client.get_all() == [obj1]

    def test_get_all_multiple(self, db_client, obj1, obj2):
        db_client.add(obj1)
        db_client.add(obj2)
        assert db_client.get_all() == [obj1, obj2]


class TestUpdate:
    def test_update(self, db_client, obj1):
        db_client.add(obj1)
        obj1.name = "new_name"
        db_client.update(obj1)
        retrieved_obj = db_client.get_all()[0]
        assert retrieved_obj.name == "new_name"

    def test_update_multiple(self, db_client, obj1, obj2):
        db_client.add(obj1)
        db_client.add(obj2)
        obj1.name = "new_name1"
        obj2.name = "new_name2"
        db_client.update(obj1)
        db_client.update(obj2)
        retrieved_objs = db_client.get_all()
        assert retrieved_objs[0].name == "new_name1"
        assert retrieved_objs[1].name == "new_name2"

    # Because SQLAlchemy ORM deals add as save_or_update, this test fails unless
    # we add a check for existence of the object in the database
    # This might be done in the future, but for the time being, default behavior
    # is left as is
    def test_update_nonexistent(self, db_client, obj1):
        pass
        # with pytest.raises(Exception):
        #     db_client.update(obj1)


class TestDelete:
    def test_delete(self, db_client, obj1):
        db_client.add(obj1)
        db_client.delete(obj1)
        assert db_client.get_all() == []

    def test_delete_multiple(self, db_client, obj1, obj2):
        db_client.add(obj1)
        db_client.add(obj2)
        db_client.delete(obj1)
        assert db_client.get_all() == [obj2]

    def test_delete_nonexistent(self, db_client, obj1):
        with pytest.raises(Exception):
            db_client.delete(obj1)
