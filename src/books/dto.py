from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict

# Pydantic models
# Input
class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str
    
    model_config = ConfigDict(extra='forbid')
    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'Example Book Title',
                'author': 'John Doe',
                'publisher': 'Example Publisher',
                'publish_date': '2023-01-01',
                'page_count': 300,
                'language': 'English'
            }
        }
    }
    
        


# Output extending Input + id
class BookOut(BookCreate):
    id: uuid.UUID
    created_at: datetime 
    updated_at: datetime | None = None
    
    model_config = {
        'json_schema_extra': {
            'example': {
                'id': '123e4567-e89a-12d3-a456-426614174000',
                'title': 'Example Book Title',  
                'author': 'John Doe',
                'publisher': 'Example Publisher',
                'publish_date': '2023-01-01',
                'page_count': 300,
                'language': 'English',
                'created_at': '2023-01-01T12:00:00Z',
                'updated_at': '2023-01-02T12:00:00Z'
            }
        }
    }

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    page_count: int | None = None
    language: str | None = None

    model_config = ConfigDict(extra='forbid')
    
    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'Updated Book Title',
                'author': 'Jane Doe',
                'publisher': 'Updated Publisher',
                'page_count': 350,
                'language': 'Spanish'
            }
        }
    }