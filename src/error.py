from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.common import ApiResponse
from fastapi import status

class BookNotFoundException(Exception):
    """
    Exception raised when a book is not found in the database.
    """
    pass

class UserNotFoundException(Exception):
    """
    Exception raised when a user is not found in the database.
    """
    pass

class DuplicateEntityException(Exception):
    """
    Exception raised when trying to create an entity that already exists.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
    

class WrongPasswordException(Exception):
    """
    Exception raised when the provided password does not match the stored password.
    """
    pass

class InvalidPaginationException(Exception):
    """
    Exception raised for invalid pagination parameters.
    """
    pass

class ExpiredSignatureError(Exception):
    """
    Exception raised when the token has expired.
    """
    pass

class InvalidTokenError(Exception):
    """
    Exception raised when the token is invalid.
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
            status_code=status.HTTP_404_NOT_FOUND,
            content=response.model_dump()
        )

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
        response = ApiResponse[None, dict](
            success=False,
            message="User Not Found",
            data=None,
            metadata=None
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=response.model_dump()
        )
    
    @app.exception_handler(DuplicateEntityException)
    async def duplicate_entity_exception_handler(request: Request, exc: DuplicateEntityException):
        response = ApiResponse[None, dict](
            success=False,
            message=exc.message,
            data=None,
            metadata=None
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.model_dump()
        )
    
    @app.exception_handler(WrongPasswordException)
    async def wrong_password_exception_handler(request: Request, exc: WrongPasswordException):
        response = ApiResponse[None, dict](
            success=False,
            message="Wrong Password",
            data=None,
            metadata=None
        )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=response.model_dump()
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
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.model_dump()
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
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=response.model_dump()
        )

    @app.exception_handler(Exception)
    async def http_exception_handler(request: Request, exc: Exception):
        response = ApiResponse[None, dict](
            success=False,
            message="Internal Server Error",
            data=None,
            metadata={"error_description": str(exc)}
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump()
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
            content=response.model_dump()
        )
    
    @app.exception_handler(ExpiredSignatureError)
    async def expired_signature_exception_handler(request: Request, exc: ExpiredSignatureError):
        response = ApiResponse[None, dict](
            success=False,
            message="Token has expired",
            data=None,
            metadata=None
        )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=response.model_dump()
        )
    
    @app.exception_handler(InvalidTokenError)
    async def invalid_token_exception_handler(request: Request, exc: InvalidTokenError):
        response = ApiResponse[None, dict](
            success=False,
            message="Invalid token",
            data=None,
            metadata=None
        )
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=response.model_dump()
        )
    
