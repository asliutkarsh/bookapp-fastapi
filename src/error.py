from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

class BookNotFoundException(Exception):
    def __init__(self, book_id):
        super().__init__(f"Book with id {book_id} not found.")
        self.book_id = book_id

class InvalidPaginationException(Exception):
    def __init__(self, skip, limit):
        super().__init__(f"Invalid pagination: skip={skip}, limit={limit}. Skip must be non-negative and limit must be positive.")


def register_all_errors(app: FastAPI):
    @app.exception_handler(BookNotFoundException)
    async def book_not_found_exception_handler(request: Request, exc: BookNotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "error": "Book Not Found",
                "error_description": str(exc),
            },
        )

    @app.exception_handler(InvalidPaginationException)
    async def invalid_pagination_exception_handler(request: Request, exc: InvalidPaginationException):
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid Pagination",
                "error_description": str(exc),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation Error",
                "error_description": exc.errors(),
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code,
            },
        )
