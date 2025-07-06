import uuid
from fastapi import HTTPException
from typing import List
# from src.books.book_data import books, book_id_counter
from src.books.dto import BookCreate, BookOut, BookUpdate
from fastapi import APIRouter
from src.books.service import BookService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session

book_router = APIRouter(prefix="/books")
book_service = BookService()


# Create a Book
@book_router.post('/', status_code=201)
async def create_book(
    book: BookCreate,
    session: AsyncSession = Depends(get_session)
):
    return await book_service.create_book(book=book, session=session)

# Get all Books with Pagination
@book_router.get('/', response_model=List[BookOut])
async def get_books(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session)
):
    return await book_service.get_all_books(skip=skip, limit=limit, session=session)

# Get a single Book by ID
@book_router.get('/{book_id}', response_model=BookOut)
async def get_book(
    book_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await book_service.get_book(book_id=book_id, session=session)

# Update a Book by ID
@book_router.put('/{book_id}', response_model=BookOut)
async def update_book(
    book_id: uuid.UUID,
    book: BookUpdate,
    session: AsyncSession = Depends(get_session)
):
    return await book_service.update_book(book_id=book_id, book=book, session=session)

# Delete a Book by ID
@book_router.delete('/{book_id}', status_code=204)
async def delete_book(
    book_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await book_service.delete_book(book_id=book_id, session=session)
