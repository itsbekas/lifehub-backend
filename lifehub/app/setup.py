import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from lifehub.config.providers import setup_providers
from lifehub.core.base_model import BaseModel
from lifehub.core.module.models import *  # noqa: F401,F403
from lifehub.core.provider.models import *  # noqa: F401,F403
from lifehub.core.user.models import *  # noqa: F401,F403
from lifehub.modules.finance.models import *  # noqa: F401,F403
from lifehub.modules.server.models import *  # noqa: F401,F403


def setup():
    load_dotenv()

    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url, echo=True)

    BaseModel.metadata.create_all(engine)

    setup_providers()


def clean():
    """
    Warning: This function will drop all tables and recreate them
    This is only for development purposes
    """
    input(
        "This will drop all tables in the database. Press Enter to continue or Ctrl+C to exit"
    )

    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    engine = create_engine(db_url, echo=True)

    BaseModel.metadata.drop_all(engine)
