from lifehub.lib.api.base import API, APIException

from .models import DailyTask, HabitTask, TodoTask


class Habitica(API):
    base_url = "https://habitica.com/api/v3"

    def __init__(self):
        token = self._load_env_token("HABITICA_TOKEN")
        x_user = self._load_env_token("HABITICA_USER")
        x_client = self._load_env_token("HABITICA_CLIENT")
        self.headers = {
            "x-client": x_client,
            "x-api-user": x_user,
            "x-api-key": token,
        }

    def _get(self, endpoint: str, params: dict = {}):
        return self._get_with_headers(endpoint, params=params)

    def _get_user_tasks(self, task_type: str):
        try:
            params = {"type": task_type}
            res = self._get("tasks/user", params=params)
            return res.get("data", [])
        except APIException as e:
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
        msg = res.json()
        return f"{msg.get('error', '')}: {msg.get('message', '')}"
