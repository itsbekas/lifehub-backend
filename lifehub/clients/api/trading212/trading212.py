from lifehub.clients.api.base import APIClient, APIException

from .models import AccountCash, AccountMetadata, Order, Transaction


class Trading212APIClient(APIClient):
    base_url = "https://live.trading212.com/api/v0"

    def __init__(self):
        super().__init__()
        self.token = self._load_env_token("T212_TOKEN")

    def _get(self, endpoint: str, params: dict = {}):
        return self._get_with_token(endpoint, params=params)

    def get_account_cash(self) -> AccountCash | None:
        try:
            res = self._get("equity/account/cash")
            return AccountCash.from_response(res)
        except APIException as e:
            print(e)
            return None

    def get_account_metadata(self) -> AccountMetadata | None:
        try:
            res = self._get("equity/account/info")
            return AccountMetadata.from_response(res)
        except APIException as e:
            print(e)
            return None

    def get_order_history(self):
        try:
            res = self._get("equity/history/orders")
            data = res.get("items", [])
            return [Order.from_response(o) for o in data]
        except APIException as e:
            print(e)
            return None

    def get_paid_out_dividends(self):
        raise NotImplementedError

    def get_transactions(self):
        try:
            res = self._get("history/transactions")
            data = res.get("items", [])
            return [Transaction.from_response(t) for t in data]
        except APIException as e:
            print(e)
            return None

    def _error_msg(self, res):
        return res.text