from typing import Any

from lifehub.core.common.api_client import APIClient
from lifehub.core.user.schema import User

from .models import Calendar


class GoogleCalendarAPIClient(APIClient):
    provider_name = "google"
    base_url = "https://www.googleapis.com/calendar/v3"

    def __init__(self, user: User) -> None:
        super().__init__(user)
        self.headers = self._token_headers

    def _get(self, endpoint: str, params: dict[str, str] = {}) -> Any:
        return self._get_with_headers(endpoint, params=params)

    def get_calendars(self) -> list[Calendar]:
        res = self._get("users/me/calendarList")
        data = res.get("items", [])
        return [Calendar.from_response(c) for c in data]

    def _error_msg(self, res: Any) -> Any:
        return res.text
