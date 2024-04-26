from requests import Response

from lifehub.clients.api.base import APIClient

from .models import MainData


class QBittorrentAPIClient(APIClient):
    base_url = "https://qb.b21.tech/api/v2"

    def __init__(self):
        super().__init__()

        from requests import post

        username = self._load_env_token("QBITTORRENT_USERNAME")
        password = self._load_env_token("QBITTORRENT_PASSWORD")
        headers = {"Referer": "https://qb.b21.tech/"}
        auth_data = {"username": username, "password": password}
        res = post(f"{self.base_url}/auth/login", headers=headers, data=auth_data)
        self.cookies = res.cookies.get_dict()

    def _get(self, endpoint: str):
        return self._get_with_cookies(endpoint)

    def get_main_data(self) -> MainData | None:
        res = self._get("sync/maindata")
        return MainData.from_response(res)

    def _error_msg(self, res: Response):
        return res.text
