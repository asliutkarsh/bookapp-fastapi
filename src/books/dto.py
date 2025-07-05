from pydantic import BaseModel


# Pydantic models
# Input
class Book(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str

# Output extending Input + id
class BookOut(Book):
    id: int

class BookUpdate(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
    
    class Config:
        extra = 'forbid'
