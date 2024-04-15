import uuid

from lifehub.clients.db.user_base import UserBaseDBClient
from lifehub.models.user import UserToken


class UserTokenDBClient(UserBaseDBClient[UserToken]):
    def __init__(self, user_id: uuid.UUID):
        super().__init__(UserToken, user_id)
