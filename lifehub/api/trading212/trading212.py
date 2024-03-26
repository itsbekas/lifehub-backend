from os import getenv
from lifehub.api.base import API


class Trading212(API):
    base_url = "https://live.trading212.com/api/v0"

    def __init__(self):
        self.token = getenv("T212_TOKEN")

    def _get(self, endpoint: str):
        return self._get_with_token(endpoint)

    def get_account(self):
        return self._get("equity/account/cash")

    def _error_msg(self, res):
        return res.text
