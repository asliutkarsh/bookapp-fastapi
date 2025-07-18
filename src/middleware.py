from src.common import log_config
import logging.config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def log_middleware(request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000  # in milliseconds
        logger.info(f"Response: {response.status_code} - Process Time: {process_time:.2f} ms")
        return response
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.add_middleware(
        log_middleware
    )
