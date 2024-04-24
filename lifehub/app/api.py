from os import getenv

import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from lifehub.api.routers import (  # noqa: E402
    auth_router,
    finance_router,
    provider_router,
    server_router,
)

#### Config ####
app = FastAPI(
    title="LifeHub API",
    description="API for LifeHub",
    version="0.1.0",
    openapi_url="/api/v0/openapi.json",
    docs_url="/api/v0/docs",
    redoc_url="/api/v0/redoc",
)

#### CORS ####
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#### Routers ####
api = APIRouter()
api.include_router(auth_router)
api.include_router(finance_router)
api.include_router(server_router)
api.include_router(provider_router)

# TODO: Eventually replace this with a reverse proxy
app.include_router(api, prefix="/api/v0")


def run():
    host = getenv("UVICORN_HOST", "localhost")
    uvicorn.run("lifehub.app.api:app", host=host, port=8000, reload=True)


if __name__ == "__main__":
    run()
