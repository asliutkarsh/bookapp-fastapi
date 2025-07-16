from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.dto import RegisterRequest, LoginRequest, UserResponse
from src.auth.model import User
from src.auth.utils import generate_passwd_hash, verify_passwd_hash, create_jwt
from src.error import UserNotFoundException, WrongPasswordException, DuplicateEntityException 
from src.config import Config
class UserService:
    
    async def register_user(self, user_data: RegisterRequest, session: AsyncSession):
        user_exists = await self.user_exists(user_data.email, user_data.username, session)
        
        if user_exists:
            raise DuplicateEntityException("User already exists")
        
        user = await self.create_user(user_data, session)
        user_data = {
            "user_id": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role
        }
        token = create_jwt(user_data)
        refresh_token = create_jwt(user_data, Config.REFRESH_TOKEN_EXPIRY_MINUTES)
        return user, token, refresh_token
    
    async def login_user(self, login_data: LoginRequest, session: AsyncSession):
        if login_data.email:
            user = await self.get_user_by_email(login_data.email, session)
        else:
            user = await self.get_user_by_username(login_data.username, session)
        if user is None:
            raise UserNotFoundException("User not found")
        if not verify_passwd_hash(login_data.password, user.password_hash):
            raise WrongPasswordException("Wrong password")
        user_data = {
            "user_id": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role
        }
        token = create_jwt(user_data)
        refresh_token = create_jwt(user_data, Config.REFRESH_TOKEN_EXPIRY_MINUTES)
        return user, token, refresh_token

    async def get_user_by_id(self, user_id: int, session: AsyncSession):
        statement = select(User).where(User.id == user_id)
        result = await session.exec(statement)
        user = result.first()
        return user
    
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def get_user_by_username(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def user_exists(self, email, username, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        if user is None:
            user = await self.get_user_by_username(username, session)
        return True if user is not None else False

    async def create_user(self, user_data: RegisterRequest, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password_hash = generate_passwd_hash(user_data_dict["password"])
        new_user.role = "user"
        
        session.add(new_user)
        
        await session.commit()
        return new_user
