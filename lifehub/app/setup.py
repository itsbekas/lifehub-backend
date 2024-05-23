from sqlalchemy import create_engine

from lifehub.app.util.schemas import *  # noqa: F401,F403
from lifehub.config.constants import DATABASE_URL
from lifehub.config.providers import setup_providers
from lifehub.core.common.base_model import BaseModel


def setup():
    engine = create_engine(DATABASE_URL, echo=True)

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

    engine = create_engine(DATABASE_URL, echo=True)

    BaseModel.metadata.drop_all(engine)
