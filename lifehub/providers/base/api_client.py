from os import getenv
from typing import Optional

import requests

from lifehub.clients.db.provider import ProviderDBClient, ProviderTokenDBClient
from lifehub.core.database_service import get_session
from lifehub.core.provider.schema import Provider, ProviderToken
from lifehub.core.user.schema import User


class APIException(Exception):
    def __init__(self, api: str, url: str, status_code: int, msg: str):
        self.api = api
        self.url = url
        self.status_code = status_code
        self.msg = msg

    def __str__(self):
        return f"{self.api} API: Error accessing {self.url} - HTTP {self.status_code}: {self.msg}"


class APIClient:
    provider_name: str
    base_url: str
    headers: Optional[dict]
    cookies: Optional[dict[str, str]]

    def __init__(self, user: User):
        with get_session() as session:
            self.provider: Provider | None = ProviderDBClient(session).get_by_name(
                self.provider_name
            )

            if self.provider is None:
                raise Exception(
                    f"Provider {self.provider_name} not found in the database"
                )

            api_token: ProviderToken | None = ProviderTokenDBClient(session).get(
                user, self.provider
            )

            if api_token is None:
                raise Exception(f"Token not found for {self.provider_name} provider")

            self.token = api_token.token

    def _get(self, endpoint: str):
        """
        GET request to the API
        """
        raise NotImplementedError

    def _get_basic(self, endpoint: str, params: dict = {}):
        """
        Basic GET request to the API
        """
        url = f"{self.base_url}/{endpoint}"
        res = requests.get(url, params=params)
        if res.status_code != 200:
            raise APIException(
                type(self).__name__, url, res.status_code, self._error_msg(res)
            )
        return res.json()

    def _get_with_token(self, endpoint: str, params: dict = {}):
        """
        GET request to the API with token in the header
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": self.token}
        res = requests.get(url, headers=headers, params=params)
        if res.status_code != 200:
            raise APIException(
                type(self).__name__, url, res.status_code, self._error_msg(res)
            )
        return res.json()

    def _get_with_token_bearer(self, endpoint: str, params: dict = {}):
        """
        GET request to the API with token bearer in the header
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}"}
        res = requests.get(url, headers=headers, params=params)
        if res.status_code != 200:
            raise APIException(
                type(self).__name__, url, res.status_code, self._error_msg(res)
            )
        return res.json()

    def _get_with_headers(self, endpoint: str, params: dict = {}):
        """
        GET request to the API with custom headers
        """
        url = f"{self.base_url}/{endpoint}"
        res = requests.get(url, headers=self.headers, params=params)
        if res.status_code != 200:
            raise APIException(
                type(self).__name__, url, res.status_code, self._error_msg(res)
            )
        return res.json()

    def _get_with_cookies(self, endpoint: str, params: dict = {}):
        """
        GET request to the API with cookies
        """
        url = f"{self.base_url}/{endpoint}"
        res = requests.get(url, cookies=self.cookies, params=params)
        if res.status_code != 200:
            raise APIException(
                type(self).__name__, url, res.status_code, self._error_msg(res)
            )
        return res.json()

    def _error_msg(self, res: requests.Response):
        """
        Get the error message from the response
        """
        raise NotImplementedError

    def _load_env_token(self, env_var: str):
        """
        Load token from environment variable
        """

        return getenv(env_var)

    def _test(self):
        """
        Test connection to the API
        """
        raise NotImplementedError

    def test_connection(self):
        """
        Test connection to the API
        """
        try:
            self._test()
            return True
        except APIException:
            return False
