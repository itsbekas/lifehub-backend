from lifehub.core.common.database_service import get_session


class BaseService:
    def __init__(self):
        self.session = get_session()
