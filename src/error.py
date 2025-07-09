from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.common import ApiResponse

class BookNotFoundException(Exception):
    """
    Exception raised when a book is not found in the database.
    """
    pass

class InvalidPaginationException(Exception):
    """
    Exception raised for invalid pagination parameters.
    """
    pass

def register_all_errors(app: FastAPI):
    @app.exception_handler(BookNotFoundException)
    async def book_not_found_exception_handler(request: Request, exc: BookNotFoundException):
        response = ApiResponse[None, dict](
            success=False,
            message="Book Not Found",
            data=None,
            metadata=None
        )
        return JSONResponse(
            status_code=404,
            content=response.dict()
        )

    @app.exception_handler(InvalidPaginationException)
    async def invalid_pagination_exception_handler(request: Request, exc: InvalidPaginationException):
        response = ApiResponse[None, dict](
            success=False,
            message="Invalid Pagination",
            data=None,
            metadata=None
        )
        return JSONResponse(
            status_code=400,
            content=response.dict()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        response = ApiResponse[None, list](
            success=False,
            message="Validation Error",
            data=None,
            metadata={"error_description": exc.errors()}
        )
        return JSONResponse(
            status_code=422,
            content=response.dict()
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        response = ApiResponse[None, dict](
            success=False,
            message="HTTP Exception",
            data=None,
            metadata={"error_description": exc.detail}
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=response.dict()
        )
