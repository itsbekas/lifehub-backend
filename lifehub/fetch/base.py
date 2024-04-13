import datetime as dt
import uuid

from sqlalchemy import func
from sqlmodel import select

from lifehub.clients.db import DatabaseClient
from lifehub.models.user import APIToken
from lifehub.models.utils.fetch_update import FetchUpdate


class BaseFetcher:
    table_id: str | None = None
    tokens: list[str] | None = None

    def __init__(self):
        # Setup the database engine
        self.db = DatabaseClient.get_instance()

    def _get_users(self) -> list[uuid.UUID]:
        # Get all the users that have the required tokens
        query = (
            select(APIToken.user_id)
            .where(APIToken.token.in_(self.tokens))
            .group_by(APIToken.user_id)
            .having(func.count(APIToken.token) == len(self.tokens))
        )
        return self.session.exec(query).all()

    def fetch(self):
        with self.db.get_session() as self.session:
            self.last_update: dt.datetime = self._update_fetch_timestamp()
            self.fetch_data()
            self.session.commit()

    def fetch_data(self):
        raise NotImplementedError("fetch_data must be implemented in the subclass")

    def _update_fetch_timestamp(self) -> dt.datetime:
        """
        Get the last time the fetch was updated and update it to the current time
        """
        # Get the last time the fetch was updated
        query = select(FetchUpdate).where(FetchUpdate.id == self.table_id)
        res = self.session.exec(query).first()
        # TODO: Setup a default value on table creation to avoid this check
        if res is None:
            last_update = dt.datetime.min
            res = FetchUpdate(id=self.table_id, last_update=last_update)
        else:
            last_update = res.last_update

        # Update last_update to the current time
        # This won't be saved to the database until the session is committed
        res.last_update = dt.datetime.now()
        self.session.add(res)

        # Returns the last time the fetch was updated
        return last_update
