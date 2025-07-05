from fastapi import HTTPException
from typing import List
from books.book_data import books, book_id_counter
from books.dto import Book, BookOut, BookUpdate
from fastapi import APIRouter

book_router = APIRouter(prefix="/books")


# Create a Book
@book_router.post('/', status_code=201)
async def create_book(book: Book):
    global book_id_counter
    new_book = book.model_dump()
    new_book['id'] = book_id_counter
    books.append(new_book)
    book_id_counter = book_id_counter + 1
    return new_book

# Get all Books with Pagination


@book_router.get('/', response_model=List[BookOut])
async def get_books(skip: int = 0, limit: int = 10):
    return books[skip: skip + limit]

# Get a single Book by ID


@book_router.get('/{book_id}', response_model=BookOut)
async def get_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Update a Book by ID


@book_router.put('/{book_id}', response_model=BookOut)
async def update_book(book_id: int, book: BookUpdate):
    for index, existing_book in enumerate(books):
        if existing_book['id'] == book_id:
            updated_book = book.model_dump()
            updated_book['id'] = book_id
            existing_publish_date = existing_book['publish_date']
            updated_book['publish_date'] = existing_publish_date
            books[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# Delete a Book by ID


@book_router.delete('/{book_id}', status_code=204)
async def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(index)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
