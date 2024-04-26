from lifehub.clients.api.base import APIClient

from .models import AccountCash, AccountMetadata, Order, Transaction


class Trading212APIClient(APIClient):
    provider_name = "trading212"
    base_url = "https://live.trading212.com/api/v0"

    def _get(self, endpoint: str, params: dict = {}):
        return self._get_with_token(endpoint, params=params)

    def _test(self):
        self.get_account_metadata()

    def get_account_cash(self) -> AccountCash | None:
        res = self._get("equity/account/cash")
        return AccountCash.from_response(res)

    def get_account_metadata(self) -> AccountMetadata | None:
        res = self._get("equity/account/info")
        return AccountMetadata.from_response(res)

    def get_order_history(self):
        res = self._get("equity/history/orders")
        data = res.get("items", [])
        return [Order.from_response(o) for o in data]

    def get_paid_out_dividends(self):
        raise NotImplementedError

    def get_transactions(self):
        res = self._get("history/transactions")
        data = res.get("items", [])
        return [Transaction.from_response(t) for t in data]

    def _error_msg(self, res):
        return res.text
