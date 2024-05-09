from lifehub.clients.db.service import get_session
from lifehub.clients.db.util import FetchUpdateDBClient, ModuleDBClient
from lifehub.models.user_old import User
from lifehub.models.util import Module


class BaseFetcher:
    module_name: str | None = None

    def __init__(self):
        with get_session() as session:
            self.module: Module = ModuleDBClient(session=session).get_by_name(
                self.module_name, retrieve_users=True
            )

    def _get_users(self) -> list[User]:
        return self.module.users

    def fetch(self):
        for self.user in self._get_users():
            with get_session() as self.session:
                self._update_fetch_timestamp()
                self.fetch_data()
                self.session.commit()

    def fetch_data(self):
        raise NotImplementedError("fetch_data must be implemented in the subclass")

    def _update_fetch_timestamp(self):
        db_client = FetchUpdateDBClient(self.session)
        self.prev_timestamp = db_client.get(self.module).last_update
        db_client.update(self.module)
