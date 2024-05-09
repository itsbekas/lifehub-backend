import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from lifehub.config.providers import setup_providers
from lifehub.core.models.base import BaseModel
from lifehub.core.module.models import *  # noqa: F401,F403
from lifehub.core.provider.models import *  # noqa: F401,F403
from lifehub.core.user.models import *  # noqa: F401,F403
from lifehub.modules.finance.models import *  # noqa: F401,F403
from lifehub.modules.server.models import *  # noqa: F401,F403


def run():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url, echo=True)

    BaseModel.metadata.create_all(engine)

    setup_providers()


if __name__ == "__main__":
    run()
