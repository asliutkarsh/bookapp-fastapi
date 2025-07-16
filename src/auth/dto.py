from datetime import datetime
import uuid
from pydantic import BaseModel, Field, model_validator


class LoginRequest(BaseModel):
    email: str | None = Field(default=None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    username: str | None = Field(default=None, min_length=3)  
    password: str = Field(..., min_length=8)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "johndoe@example.com",
                "username": "johndoe",
                "password": "S!ecurepassword123"
            }
        }
    }
    
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3)
    first_name: str | None = None
    last_name: str | None = None
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.com",
                "password": "S!ecurepassword123",
                "confirm_password": "S!ecurepassword123"
            }
        }
    }
    
    @model_validator(mode='after')
    def match_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
        

class UpdateUserRequest(BaseModel):
    username: str  | None = Field(..., min_length=3)
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe_updated",
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe_updated@example.com",
            }
        }
    }
    

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    first_name: str | None = None
    last_name: str | None = None
    email: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime | None = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.com",
                "is_verified": True,
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z"
            }
        }
    }

class AuthResponse(BaseModel):
    user: UserResponse
    token: str