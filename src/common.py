# src/dto/api_response.py

from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")  # For data
M = TypeVar("M")  # For metadata

class ApiResponse(BaseModel, Generic[T, M]):
    success: bool
    message: str
    data: Optional[T] = None
    metadata: Optional[M] = None

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["file", "console"],
    },
}    
