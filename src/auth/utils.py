import bcrypt
import jwt
from datetime import datetime, timedelta,timezone
from src.error import ExpiredSignatureError, InvalidTokenError
import logging
from src.config import Config

def generate_passwd_hash(password: str) -> str:
    hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hash.decode("utf-8")

def verify_passwd_hash(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))

def create_jwt(payload: dict, expiry_minutes: int = 60) -> str:
    payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    payload['iat'] = datetime.now(timezone.utc)
    return jwt.encode(payload, Config.JWT_SECRET, algorithm='HS256')

def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid token")
    except jwt.PyJWTError as e:
        logging.exception(e)
        raise InvalidTokenError("Invalid token")