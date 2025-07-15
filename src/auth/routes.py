from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.common import ApiResponse
from src.auth.dto import RegisterRequest, LoginRequest, UserResponse
from src.auth.service import UserService
from src.db.main import get_session

auth_router = APIRouter()
service = UserService()

@auth_router.post(
    "/signup", 
    response_model=ApiResponse[UserResponse, None],
    status_code=status.HTTP_201_CREATED
)
async def register_user(user_data: RegisterRequest, session: AsyncSession = Depends(get_session)):
    user = await service.register_user(user_data, session)
    return ApiResponse(success=True, message="User created successfully", data=UserResponse.model_validate(user))
    
    
@auth_router.post(
    "/login", 
    response_model=ApiResponse[UserResponse, None],
    status_code=status.HTTP_200_OK
)
async def login_user(login_data: LoginRequest, session: AsyncSession = Depends(get_session)):
    user = await service.login_user(login_data, session)
    return ApiResponse(success=True, message="User logged in successfully", data=UserResponse.model_validate(user))
