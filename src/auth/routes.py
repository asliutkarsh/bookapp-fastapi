from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.common import ApiResponse
from src.auth.dto import RegisterRequest, LoginRequest, UserResponse, AuthResponse
from src.auth.service import UserService
from src.db.main import get_session

auth_router = APIRouter()
service = UserService()

@auth_router.post(
    "/signup", 
    response_model=ApiResponse[AuthResponse, str],
    status_code=status.HTTP_201_CREATED
)
async def register_user(user_data: RegisterRequest, session: AsyncSession = Depends(get_session)):
    user, token = await service.register_user(user_data, session)
    data = AuthResponse(
        user=UserResponse.model_validate(user.model_dump()),
        token=token
    )
    return ApiResponse(success=True, message="User created successfully", data=data)
    
    
@auth_router.post(
    "/login", 
    response_model=ApiResponse[AuthResponse, str],
    status_code=status.HTTP_200_OK
)
async def login_user(login_data: LoginRequest, session: AsyncSession = Depends(get_session)):
    user, token = await service.login_user(login_data, session)
    data = AuthResponse(
        user=UserResponse.model_validate(user.model_dump()),
        token=token
    )
    return ApiResponse(success=True, message="User logged in successfully", data=data)

@auth_router.get(
    "/me", 
    response_model=ApiResponse[UserResponse, None],
    status_code=status.HTTP_200_OK
)
async def get_current_user(session: AsyncSession = Depends(get_session)):
    return ApiResponse(success=True, message="User retrieved successfully", data=session.user)