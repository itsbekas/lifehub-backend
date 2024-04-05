import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

import lifehub.models  # noqa: F401

load_dotenv()

# Database Connection String
DATABASE_URL = os.getenv("DATABASE_URL")  # Get from environment or hardcode below

# Create the SQLModel engine
engine = create_engine(DATABASE_URL)  # echo=True for debugging SQL statements

try:
    # Function to initialize database tables
    SQLModel.metadata.create_all(engine)
except Exception as e:
    print("Error creating database tables: ", e)


# Function to get a database session
def get_session():
    return Session(engine)
