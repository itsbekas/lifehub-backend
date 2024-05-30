from os import getenv
from typing import Any, Optional

import requests

from lifehub.core.common.database_service import get_session
from lifehub.core.common.repository.base import BaseRepository
from lifehub.core.provider.repository.provider import ProviderRepository
from lifehub.core.provider.repository.provider_token import ProviderTokenRepository
from lifehub.core.provider.schema import Provider, ProviderToken
from lifehub.core.user.schema import User


class APIException(Exception):
    def __init__(self, api: str, url: str, status_code: int, msg: str) -> None:
        self.api = api
        self.url = url
        self.status_code = status_code
        self.msg = msg

    def __str__(self) -> str:
        return f"{self.api} API: Error accessing {self.url} - HTTP {self.status_code}: {self.msg}"


class APIClient:
    provider_name: str
    base_url: str
    headers: Optional[dict]
    cookies: Optional[dict[str, str]]

    def __init__(self, user: User, repository: BaseRepository) -> None:
        with get_session() as session:
            self.provider: Provider | None = ProviderRepository(session).get_by_name(
                self.provider_name
            )

            if self.provider is None:
                raise Exception(
                    f"Provider {self.provider_name} not found in the database"
                )

            api_token: ProviderToken | None = ProviderTokenRepository(session).get(
                user, self.provider
            )

            if api_token is None:
                raise Exception(f"Token not found for {self.provider_name} provider")

            self.token = api_token.token

    def _get(self, endpoint: str) -> dict[str, Any]:
        """
        GET request to the API
        """
        raise NotImplementedError

    def _get_basic(self, endpoint: str, params: dict[str, Any] = {}) -> dict[str, Any]:
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

    def _get_with_token(
        self, endpoint: str, params: dict[str, Any] = {}
    ) -> dict[str, Any]:
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

    def _get_with_token_bearer(
        self, endpoint: str, params: dict[str, Any] = {}
    ) -> dict[str, Any]:
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

    def _get_with_headers(
        self, endpoint: str, params: dict[str, Any] = {}
    ) -> dict[str, Any]:
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

    def _get_with_cookies(
        self, endpoint: str, params: dict[str, Any] = {}
    ) -> dict[str, Any]:
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

    def _error_msg(self, res: requests.Response) -> str:
        """
        Get the error message from the response
        """
        raise NotImplementedError

    def _load_env_token(self, env_var: str) -> str | None:
        """
        Load token from environment variable
        """

        return getenv(env_var)

    def _test(self) -> None:
        """
        Test connection to the API
        """
        raise NotImplementedError

    def test_connection(self) -> bool:
        """
        Test connection to the API
        """
        try:
            self._test()
            return True
        except APIException:
            return False
