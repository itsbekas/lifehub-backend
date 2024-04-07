import re

from lifehub.lib.api.base import APIClient

from .models import Account, CategoryGroup


class YNABAPIClient(APIClient):
    base_url = "https://api.ynab.com/v1"

    def __init__(self, budget: str = "last-used"):
        super().__init__()
        self.token = self._load_env_token("YNAB_TOKEN")
        self.budget = budget

    def _get(self, endpoint: str):
        # TODO: Maybe catch exceptions here and return None
        # TODO: Save endpoint's last knowledge of server
        return self._get_with_token_bearer(endpoint)

    def get_user(self):
        return self._get("user")

    def get_budgets(self):
        return self._get("budgets")

    def get_budget(self, budget: str = "last-used"):
        return self._get(f"budgets/{budget}")

    def get_budget_settings(self, budget: str = "last-used"):
        return self._get(f"budgets/{budget}/settings")

    def get_accounts(self, budget: str = "last-used"):
        try:
            res = self._get(f"budgets/{budget}/accounts")
            data = res.get("data", {}).get("accounts", [])
            return [Account.from_response(a) for a in data]
        except Exception as e:
            print(e)
            return []

    def get_account(self, account: str):
        return self._get(f"budgets/{self.budget}/accounts/{account}")

    def get_categories(self):
        try:
            res = self._get(f"budgets/{self.budget}/categories")
            data = res.get("data", {}).get("category_groups", [])
            return [CategoryGroup.from_response(c) for c in data]
        except Exception as e:
            print(e)
            return []

    def get_category(self, category: str):
        return self._get(f"budgets/{self.budget}/categories/{category}")

    def get_category_month(self, category: str, month: str):
        if not re.match(r"\d{4}-\d{2}", month):
            raise Exception(
                "Can't retrieve category month. Month must be in format YYYY-MM-DD"
            )
        return self._get(f"budgets/{self.budget}/months/{month}/categories/{category}")

    def _error_msg(self, res):
        return res.json().get("error", {}).get("detail")
