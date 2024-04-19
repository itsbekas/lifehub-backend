import uuid

from sqlalchemy import func, select

from lifehub.clients.db.base import BaseDBClient
from lifehub.models.provider import APIToken


class APITokenDBClient(BaseDBClient[APIToken]):
    def __init__(self):
        super().__init__(APIToken)

    def get_user_ids_with_tokens(self, tokens: list[str]) -> list[uuid.UUID]:
        """
        Gets the user IDs that have all the tokens required
        """
        with self.session as session:
            query = (
                select(APIToken.user_id)
                .filter(APIToken.api_id.in_(tokens))
                .group_by(APIToken.user_id)
                .having(func.count(APIToken.api_id) == len(tokens))
            )
            result: list[APIToken] = session.exec(query).all()
            return [r[0] for r in result]
