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
