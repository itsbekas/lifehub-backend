from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..api.routers import auth_router, finance_router, server_router, tasks_router

#### Config ####
api = FastAPI(
    title="LifeHub API",
    description="API for LifeHub",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

#### CORS ####
origins = [
    "http://localhost:5173",
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#### Routers ####
api.include_router(auth_router)
api.include_router(finance_router)
api.include_router(tasks_router)
api.include_router(server_router)
