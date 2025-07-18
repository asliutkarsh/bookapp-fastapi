from fastapi.security import HTTPBearer
from fastapi import Request
from src.auth.utils import decode_jwt
from src.error import InvalidTokenError, AccountNotVerified, InsufficientPermission
from src.db.main import get_session
from src.auth.service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import List
from src.auth.model import User

user_service = UserService()

class BearerTokenDepends(HTTPBearer ):
    def __init__(self):
        super().__init__(auto_error=True)
    
    async def __call__(self, request: Request):
        """Extracts the bearer token from the request headers."""
        
        auth = await super().__call__(request)
        
        token = auth.credentials
        
        try:
            payload = decode_jwt(token)
        except Exception as e:
            raise InvalidTokenError("Invalid token")
                
        return payload
            
        
async def get_current_user(
    token_details: dict = Depends(BearerTokenDepends()),
    session: AsyncSession = Depends(get_session),
):
    user_id = token_details["user_id"]
    user = await user_service.get_user_by_id(user_id, session)
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if not current_user.is_verified:
            raise AccountNotVerified()
        if current_user.role in self.allowed_roles:
            return current_user

        raise InsufficientPermission()
    
admin_checker = RoleChecker(["admin"])
user_checker = RoleChecker(["user"])
