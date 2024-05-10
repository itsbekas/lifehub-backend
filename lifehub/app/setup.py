import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from lifehub.config.providers import setup_providers
from lifehub.core.common.base_model import BaseModel
from lifehub.core.module.schema import *  # noqa: F401,F403
from lifehub.core.provider.schema import *  # noqa: F401,F403
from lifehub.core.user.schema import *  # noqa: F401,F403
from lifehub.providers.qbittorrent.schema import *  # noqa: F401,F403
from lifehub.providers.ynab.schema import *  # noqa: F401,F403


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
