# src/dto/api_response.py

from typing import Generic, Optional, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")  # For data
M = TypeVar("M")  # For metadata

class ApiResponse(GenericModel, Generic[T, M]):
    success: bool
    message: str
    data: Optional[T] = None
    metadata: Optional[M] = None
