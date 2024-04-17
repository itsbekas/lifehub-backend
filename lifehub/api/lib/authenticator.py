from lifehub.api.lib.auth_config import auth_info


class Authenticator:
    def __init__(self, api_id: str, user_id: str):
        self.auth_info = auth_info[api_id]
