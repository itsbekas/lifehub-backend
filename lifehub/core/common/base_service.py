from sqlalchemy.orm import Session

from lifehub.core.common.database_service import get_session


class BaseService:
    def __init__(self) -> None:
        self.session: Session = get_session()
