from lifehub.lib.api.base import API

from .models import AccountCash, AccountMetadata


class Trading212(API):
    base_url = "https://live.trading212.com/api/v0"

    def __init__(self):
        self.token = self._load_env_token("T212_TOKEN")

    def _get(self, endpoint: str, params: dict = {}):
        return self._get_with_token(endpoint, params=params)

    def get_account_cash(self) -> AccountCash | None:
        try:
            res = self._get("equity/account/cash")
            return AccountCash.from_response(res)
        except Exception as e:
            print(e)
            return None

    def get_account_metadata(self) -> AccountMetadata | None:
        try:
            res = self._get("equity/account/info")
            return AccountMetadata.from_response(res)
        except Exception as e:
            print(e)
            return None

    def _error_msg(self, res):
        return res.text
