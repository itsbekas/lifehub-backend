from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import finance, auth
from dotenv import load_dotenv

#### Setup ####
load_dotenv()

#### Config ####
app = FastAPI(
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#### Routers ####
app.include_router(auth.router)
app.include_router(finance.router)