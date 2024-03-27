from lifehub.api.base import API


class Trading212(API):
    base_url = "https://live.trading212.com/api/v0"

    def __init__(self):
        self.token = self._load_env_token("T212_TOKEN")

    def _get(self, endpoint: str):
        return self._get_with_token(endpoint)

    def get_account_cash(self):
        return self._get("equity/account/cash")

    def get_account_metadata(self):
        return self._get("equity/account/info")

    def _error_msg(self, res):
        return res.text
