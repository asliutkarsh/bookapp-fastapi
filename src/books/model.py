from datetime import datetime
import uuid
from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg



class Book(SQLModel, table=True):
    __tablename__ = 'books'
    id: uuid.UUID = Field(
                sa_column=Column(
                    pg.UUID(as_uuid=True), 
                    nullable=False, 
                    primary_key=True, 
                    default=uuid.uuid4
                ))
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str
    created_at: datetime  = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False),
        default_factory=datetime.now,
    )
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=True),
        default=None)
    
    def __repr__(self):
        return f"Book(id={self.id}, title={self.title}, author={self.author}, publisher={self.publisher}, publish_date={self.publish_date}, page_count={self.page_count}, language={self.language})"
