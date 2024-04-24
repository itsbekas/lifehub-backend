from os import getenv

import requests

from lifehub.clients.db.provider import ProviderDBClient
from lifehub.models.provider import Provider


class APIException(Exception):
    def __init__(self, api: str, url: str, status_code: int, msg: str):
        self.api = api
        self.url = url
        self.status_code = status_code
        self.msg = msg

    def __str__(self):
        return f"{self.api} API: Error accessing {self.url} - HTTP {self.status_code}: {self.msg}"


class APIClient:
    def __init__(self):
        self.provider: Provider = ProviderDBClient().get_by_name(self.provider_name)

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
