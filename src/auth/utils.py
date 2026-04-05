import uuid
import logging
from datetime import datetime, timedelta

import jwt
import bcrypt
from itsdangerous import URLSafeTimedSerializer

from src.config import settings

serializer = URLSafeTimedSerializer(secret_key=settings.jwt_secret, salt="email-verification")

ACCESS_TOKEN_EXPIRY = 60  # minutes
REFRESH_TOKEN_EXPIRY = 7  # days


def generate_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(
    user_data: dict,
    expiry: timedelta = None,
    refresh: bool = False,
) -> str:
    payload = {
        "user": user_data,
        "exp": datetime.utcnow()
        + (expiry if expiry else timedelta(minutes=ACCESS_TOKEN_EXPIRY)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }

    token = jwt.encode(
        payload=payload,
        key=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


def create_url_safe_token(data: dict) -> str:
    return serializer.dumps(data)


def decode_url_safe_token(token: str) -> dict:
    try:
        return serializer.loads(token, max_age=3600)  # 1 hour expiry
    except Exception:
        return None
