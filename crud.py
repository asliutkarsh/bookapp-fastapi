from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

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


# Sample data
books = [
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell",
        "publisher": "Secker & Warburg",
        "publish_date": "1949-06-08",
        "page_count": 328,
        "language": "English"
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publisher": "J.B. Lippincott & Co.",
        "publish_date": "1960-07-11",
        "page_count": 281,
        "language": "English"
    },
    {
        "id": 3,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publisher": "Charles Scribner's Sons",
        "publish_date": "1925-04-10",
        "page_count": 218,
        "language": "English"
    }
]

book_id_counter = len(books) + 1

# Create a Book
@app.post('/books',status_code=201)
async def create_book(book:Book):
    global book_id_counter
    new_book = book.model_dump()
    new_book['id'] = book_id_counter
    books.append(new_book)
    book_id_counter = book_id_counter + 1
    return new_book

# Get all Books with Pagination
@app.get('/books', response_model=List[BookOut])
async def get_books(skip: int = 0, limit: int = 10):
    return books[skip: skip + limit]

# Get a single Book by ID
@app.get('/books/{book_id}', response_model=BookOut)
async def get_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Update a Book by ID
@app.put('/books/{book_id}', response_model=BookOut)
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
@app.delete('/books/{book_id}', status_code=204)
async def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(index)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation failed",
            "errors": exc.errors(),
        },
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail
                 },
    )








def main():
    print("Hello from bookapp-fastapi!")
    uvicorn.run(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
