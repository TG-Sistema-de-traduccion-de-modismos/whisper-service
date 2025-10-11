from fastapi import FastAPI
from app.infrastructure.routes import router
from app.core.logging_config import setup_logging

setup_logging()
app = FastAPI(title="Whisper Service (API)", version="1.0")
app.include_router(router)
