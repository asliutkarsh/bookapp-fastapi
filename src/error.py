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

class AccountNotVerified(Exception):
    """
    Exception raised when the user's account is not verified.
    """
    pass

class InsufficientPermission(Exception):
    """
    Exception raised when the user does not have the required permissions.
    """
    pass

def register_exception_handlers(app: FastAPI):
    """Registers all custom exception handlers for the app."""
    
    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(request: Request, exc: UserNotFoundException):
        response = ApiResponse[None, None](success=False, message="User not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response.model_dump())

    @app.exception_handler(DuplicateEntityException)
    async def duplicate_entity_handler(request: Request, exc: DuplicateEntityException):
        response = ApiResponse[None, None](success=False, message=exc.message)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.model_dump())

    @app.exception_handler(WrongPasswordException)
    async def wrong_password_handler(request: Request, exc: WrongPasswordException):
        response = ApiResponse[None, None](success=False, message="Incorrect email or password")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.model_dump())

    @app.exception_handler(ExpiredSignatureError)
    async def expired_token_handler(request: Request, exc: ExpiredSignatureError):
        response = ApiResponse[None, None](success=False, message="Token has expired")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.model_dump())

    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(request: Request, exc: InvalidTokenError):
        response = ApiResponse[None, None](success=False, message="Could not validate credentials")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.model_dump())
    
    @app.exception_handler(AccountNotVerified)
    async def account_not_verified_handler(request: Request, exc: AccountNotVerified):
        response = ApiResponse[None, None](success=False, message="Account not verified")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response.model_dump())
    
    @app.exception_handler(InsufficientPermission)
    async def insufficient_permission_handler(request: Request, exc: InsufficientPermission):
        response = ApiResponse[None, None](success=False, message="Insufficient permissions")
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=response.model_dump())
            
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        response = ApiResponse[None, None](
            success=False, 
            message=exc.detail
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump()
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        response = ApiResponse[None, dict](
            success=False,
            message="An unexpected internal server error occurred.",
            metadata={"error_type": type(exc).__name__}
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump()
        )

