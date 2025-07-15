from datetime import datetime
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4
        )
    )
    username: str = Field(nullable=False, unique=True)
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    email: str = Field(nullable=False, unique=True)
    password_hash: str = Field(
        exclude=True,
        sa_column=Column(pg.VARCHAR, nullable=False)
    )
    is_verified: bool = Field(default=False, nullable=False)
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False),
        default_factory=datetime.now,
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True),
        default=None
    )
