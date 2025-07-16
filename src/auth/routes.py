from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.common import ApiResponse
from src.auth.dto import RegisterRequest, LoginRequest, UserResponse, AuthResponse
from src.auth.service import UserService
from src.db.main import get_session
from src.auth.deps import get_current_user
from src.auth.model import User

auth_router = APIRouter()
service = UserService()

@auth_router.post(
    "/signup", 
    response_model=ApiResponse[AuthResponse, str],
    status_code=status.HTTP_201_CREATED
)
async def register_user(user_data: RegisterRequest, session: AsyncSession = Depends(get_session)):
    user, token, refresh_token = await service.register_user(user_data, session)
    data = AuthResponse(
        user=UserResponse.model_validate(user.model_dump()),
        token=token,
        refresh_token=refresh_token
    )
    return ApiResponse(success=True, message="User created successfully", data=data)
    
    
@auth_router.post(
    "/login", 
    response_model=ApiResponse[AuthResponse, str],
    status_code=status.HTTP_200_OK
)
async def login_user(login_data: LoginRequest, session: AsyncSession = Depends(get_session)):
    user, token, refresh_token = await service.login_user(login_data, session)
    data = AuthResponse(
        user=UserResponse.model_validate(user.model_dump()),
        token=token,
        refresh_token=refresh_token
    )
    return ApiResponse(success=True, message="User logged in successfully", data=data)

@auth_router.get(
    "/me", 
    response_model=ApiResponse[UserResponse, None],
    status_code=status.HTTP_200_OK
)
async def get_current_user(
    user: User = Depends(get_current_user),
):
    user_response = UserResponse.model_validate(user.model_dump())
    return ApiResponse(success=True, message="User retrieved successfully", data=user_response)