import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.books.service import BookService
from src.books.dto import BookCreate, BookUpdate, BookOut
from src.common import ApiResponse
from src.auth.deps import admin_checker, user_checker
from src.auth.model import User

book_router = APIRouter(prefix="/books")

service = BookService()

@book_router.post(
    "/",
    response_model=ApiResponse[BookOut, None],
    status_code=status.HTTP_201_CREATED
)
async def create_book(
        book: BookCreate, 
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(admin_checker)
    ):
    created = await service.create_book(session, book)
    return ApiResponse(success=True, message="Book created successfully", data=created)


@book_router.get(
    "/",
    response_model=ApiResponse[List[BookOut], None],
    status_code=status.HTTP_200_OK
)
async def get_books(
    skip: int = 0, 
    limit: int = 10, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(user_checker)
):
    books = await service.get_all_books(session, skip, limit)
    return ApiResponse(success=True, message="Books retrieved", data=books)


@book_router.get(
    "/{book_id}",
    response_model=ApiResponse[BookOut, None],
    status_code=status.HTTP_200_OK
)
async def get_book(
    book_id: uuid.UUID, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(user_checker)
):
    book = await service.get_book(session, book_id)
    return ApiResponse(success=True, message="Book retrieved", data=book)


@book_router.put(
    "/{book_id}",
    response_model=ApiResponse[BookOut, None],
    status_code=status.HTTP_200_OK
)
async def update_book(
    book_id: uuid.UUID, 
    book: BookUpdate, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(admin_checker)
):
    updated = await service.update_book(session, book_id, book)
    return ApiResponse(success=True, message="Book updated", data=updated)


@book_router.delete(
    "/{book_id}",
    response_model=ApiResponse[None, None],
    status_code=status.HTTP_200_OK
)
async def delete_book(
    book_id: uuid.UUID, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(admin_checker)
):
    await service.delete_book(session, book_id)
    return ApiResponse(success=True, message="Book deleted")
