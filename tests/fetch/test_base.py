import uuid

from lifehub.models.user import APIToken


class TestBaseFetcher:
    one_token: list[str] = ["token1"]
    two_tokens: list[str] = ["token1", "token2"]

    user1_id: uuid.UUID = uuid.uuid4()
    user2_id: uuid.UUID = uuid.uuid4()

    user1_token1: APIToken = APIToken(api_id="api1", token="token1", user_id=user1_id)
    user1_token2: APIToken = APIToken(api_id="api2", token="token2", user_id=user1_id)
    user2_token1: APIToken = APIToken(api_id="api1", token="token1", user_id=user2_id)
    user2_token2: APIToken = APIToken(api_id="api2", token="token2", user_id=user2_id)

    def test_get_users_one_token_no_users(self, db_session):
        """
        Tests that _get_users returns an empty list when there are no users
        """
        from lifehub.fetch.base import BaseFetcher

        fetcher = BaseFetcher()
        fetcher.tokens = self.one_token
        users = fetcher._get_users()
        assert users == []

    def test_get_users_one_token_one_of_two_users(self, db_session):
        """
        Tests that _get_users returns the correct user when there are two users
        but only one has the required token
        """
        from lifehub.fetch.base import BaseFetcher

        fetcher = BaseFetcher()
        fetcher.tokens = self.one_token
        db_session.add_user(self.user1)
        users = fetcher._get_users()
        assert users == [self.user1["id"]]
