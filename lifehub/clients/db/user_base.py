import uuid
from typing import Type

from .base import BaseDBClient, BaseModel


class UserBaseDBClient(BaseDBClient[BaseModel]):
    def __init__(self, model: Type[BaseModel], user_id: uuid.UUID):
        super().__init__(model)
        self.user_id = user_id
