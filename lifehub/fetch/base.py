import datetime as dt
import uuid

from sqlmodel import select

from lifehub.clients.db.api_token import APITokenDBClient
from lifehub.clients.db.db_service import DatabaseService
from lifehub.models.utils.fetch_update import FetchUpdate


class BaseFetcher:
    table_id: str | None = None
    tokens: list[str] | None = None

    def __init__(self):
        # Setup the database engine
        self.db = DatabaseService()

    def _get_users(self) -> list[uuid.UUID]:
        api_token_db = APITokenDBClient()
        if self.tokens is None:
            raise ValueError("Tokens must be set in the subclass")
        user_ids = api_token_db.get_user_ids_with_tokens(self.tokens)
        return user_ids

    def fetch(self):
        for self.user_id in self._get_users():
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
