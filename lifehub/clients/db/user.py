from lifehub.models.user import User
from lifehub.clients.db.base import BaseDBClient

class UserDBClient(BaseDBClient[User]):
    def __init__(self):
        super().__init__(User)
