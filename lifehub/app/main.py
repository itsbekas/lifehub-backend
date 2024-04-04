import uvicorn
from dotenv import load_dotenv

from .api import api


def run():
    load_dotenv()

    uvicorn.run(api, host="localhost", port=8000)


if __name__ == "__main__":
    run()
