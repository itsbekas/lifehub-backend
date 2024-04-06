from sqlmodel import Session, select

from lifehub.app.db import get_session
from lifehub.lib.models.utils.fetch_update import FetchUpdate
import datetime as dt

class Fetch:

    table_id: str | None = None

    def fetch(self):
        with get_session() as self.session:
            self.last_updated: dt.datetime = self._update_fetch_timestamp()
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
