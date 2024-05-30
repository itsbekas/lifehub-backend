import re
from typing import Any

from lifehub.providers.base.api_client import APIClient

from .models import Account, CategoryGroup


class YNABAPIClient(APIClient):
    provider_name = "ynab"
    base_url = "https://api.ynab.com/v1"

    budget = "last-used"

    def _get(self, endpoint: str) -> dict[str, Any]:
        # TODO: Maybe catch exceptions here and return None
        # TODO: Save endpoint's last knowledge of server
        return self._get_with_token_bearer(endpoint)

    def _test(self) -> None:
        self.get_user()

    def get_user(self) -> dict[str, Any]:
        return self._get("user")

    def get_budgets(self) -> dict[str, Any]:
        return self._get("budgets")

    def get_budget(self, budget: str = "last-used") -> dict[str, Any]:
        return self._get(f"budgets/{budget}")

    def get_budget_settings(self, budget: str = "last-used") -> dict[str, Any]:
        return self._get(f"budgets/{budget}/settings")

    def get_accounts(self, budget: str = "last-used") -> list[Account]:
        res = self._get(f"budgets/{budget}/accounts")
        data = res.get("data", {}).get("accounts", [])
        return [Account.from_response(a) for a in data]

    def get_account(self, account: str) -> dict[str, Any]:
        return self._get(f"budgets/{self.budget}/accounts/{account}")

    def get_categories(self) -> list[CategoryGroup]:
        res = self._get(f"budgets/{self.budget}/categories")
        data = res.get("data", {}).get("category_groups", [])
        return [CategoryGroup.from_response(c) for c in data]

    def get_category(self, category: str) -> dict[str, Any]:
        return self._get(f"budgets/{self.budget}/categories/{category}")

    def get_category_month(self, category: str, month: str) -> dict[str, Any]:
        if not re.match(r"\d{4}-\d{2}", month):
            raise Exception(
                "Can't retrieve category month. Month must be in format YYYY-MM-DD"
            )
        return self._get(f"budgets/{self.budget}/months/{month}/categories/{category}")

    def _error_msg(self, res: Any) -> Any:
        return res.json().get("error", {}).get("detail")
