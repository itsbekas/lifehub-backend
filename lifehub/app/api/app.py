from fastapi import FastAPI
from .routers import finance
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LifeHub API",
    description="API for LifeHub",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(finance.router)
