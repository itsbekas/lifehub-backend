from lifehub.lib.api.base import API

from .models import DailyTask, HabitTask, TodoTask


class Habitica(API):
    base_url = "https://habitica.com/api/v3"

    def __init__(self):
        self.token = self._load_env_token("HABITICA_TOKEN")
        self.x_user = self._load_env_token("HABITICA_USER")
        self.x_client = self._load_env_token("HABITICA_CLIENT")

    def _get(self, endpoint: str, params: dict = {}):
        headers = {
            "x-client": self.x_client,
            "x-api-user": self.x_user,
            "x-api-key": self.token,
        }
        return self._get_with_headers(endpoint, headers=headers, params=params)

    def _get_user_tasks(self, task_type: str):
        try:
            params = {"type": task_type}
            res = self._get("tasks/user", params=params)
            return res.get("data", [])
        except Exception as e:
            print(e)
            return []

    def get_user_habits(self):
        data = self._get_user_tasks("habits")
        return [HabitTask.from_response(t) for t in data]

    def get_user_dailies(self):
        data = self._get_user_tasks("dailys")
        return [DailyTask.from_response(t) for t in data]

    def get_user_todos(self):
        data = self._get_user_tasks("todos")
        return [TodoTask.from_response(t) for t in data]

    def _error_msg(self, res):
        return res.json()["errors"][0]["message"]
