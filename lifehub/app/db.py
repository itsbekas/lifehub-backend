import os

from sqlmodel import Session, SQLModel, create_engine

# Database Connection String
DATABASE_URL = os.getenv("DATABASE_URL")  # Get from environment or hardcode below

# Create the SQLModel engine
engine = create_engine(DATABASE_URL)  # echo=True for debugging SQL statements

try:
    # Function to initialize database tables
    SQLModel.metadata.create_all(engine)
except:
    print("FAILED")


# Function to get a database session
def get_session():
    return Session(engine)
