import requests


class APIException(Exception):
    def __init__(self, api: str, url: str, status_code: int, msg: str):
        self.api = api
        self.url = url
        self.status_code = status_code
        self.msg = msg

    def __str__(self):
        return f"{self.api} API: Error accessing {self.url} - HTTP {self.status_code}: {self.msg}"


class API:
    def _get_basic(self, endpoint: str, params: dict = {}):
        url = f"{self.base_url}/{endpoint}"
        res = requests.get(url, params=params)
        if res.status_code != 200:
            print(type(self).__name__)
            raise APIException(
                type(self).__name__, url, res.status_code, self._error_msg(res.json())
            )
        return res.json()

    def _get_with_token(self, endpoint: str, params: dict = {}):
        url = f"{self.base_url}/{endpoint}"
        res = requests.get(
            url, headers={"Authorization": f"Bearer {self.token}"}, params=params
        )
        if res.status_code != 200:
            raise APIException(
                type(self).__name__, url, res.status_code, self._error_msg(res.json())
            )
        return res.json()

    def _get_with_header(self, endpoint: str, headers: dict = {}, params: dict = {}):
        url = f"{self.base_url}/{endpoint}"
        res = requests.get(url, headers=headers, params=params)
        if res.status_code != 200:
            print(res.json())
            raise APIException(
                type(self).__name__, url, res.status_code, self._error_msg(res.json())
            )
        return res.json()

    def _error_msg(self, res: dict):
        raise NotImplementedError
