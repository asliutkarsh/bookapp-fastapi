from datetime import datetime
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.dto import BookCreate, BookUpdate
import uuid
from src.books.model import Book
from src.error import BookNotFoundException, InvalidPaginationException

class BookService:

    async def create_book(self, session: AsyncSession, book: BookCreate) -> Book:
        new_book = Book(**book.model_dump())
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def get_all_books(self, session: AsyncSession, skip: int = 0, limit: int = 10) -> list[Book]:
        if skip < 0 or limit <= 0:
            raise InvalidPaginationException(skip, limit)
        statement = select(Book).offset(skip).limit(limit).order_by(Book.created_at.desc())
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_book(self, session: AsyncSession, book_id: uuid.UUID) -> Book:
        statement = select(Book).where(Book.id == book_id)
        result = await session.execute(statement)
        book = result.scalar_one_or_none()
        if not book:
            raise BookNotFoundException(book_id)
        return book

    async def update_book(self, session: AsyncSession, book_id: uuid.UUID, book: BookUpdate) -> Book:
        existing_book = await self.get_book(session, book_id)
        for key, value in book.model_dump(exclude_unset=True).items():
            setattr(existing_book, key, value)
        existing_book.updated_at = datetime.now()
        session.add(existing_book)
        await session.commit()
        await session.refresh(existing_book)
        return existing_book

    async def delete_book(self, session: AsyncSession, book_id: uuid.UUID) -> None:
        existing_book = await self.get_book(session, book_id)
        await session.delete(existing_book)
        await session.commit()
