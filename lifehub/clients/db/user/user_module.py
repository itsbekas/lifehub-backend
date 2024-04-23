import uuid

from lifehub.clients.db.base import UserBaseDBClient
from lifehub.models.user import UserModule


class UserModuleDBClient(UserBaseDBClient[UserModule]):
    def __init__(self, user_id: uuid.UUID):
        super().__init__(UserModule, user_id)
