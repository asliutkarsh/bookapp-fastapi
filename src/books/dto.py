from datetime import datetime
import uuid
from pydantic import BaseModel

# Pydantic models
# Input
class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str
    
    class Config:
        extra = 'forbid'


# Output extending Input + id
class BookOut(BookCreate):
    id: uuid.UUID
    created_at: datetime 
    updated_at: datetime | None = None

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    page_count: int | None = None
    language: str | None = None

    class Config:
        extra = 'forbid'
