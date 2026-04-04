from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import UserCreateModel, UserLoginModel, UserOut
from src.auth.service import user_service
from src.auth.utils import create_access_token, verify_password, REFRESH_TOKEN_EXPIRY
from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user
from src.db.session import get_session
from src.db.redis import add_jti_to_blocklist
from src.errors import UserAlreadyExists, InvalidCredentials
from src.rate_limiter import limiter, DEFAULT_RATE_LIMIT, HOURLY_RATE_LIMIT, WRITE_RATE_LIMIT

auth_router = APIRouter()


@auth_router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@limiter.limit(WRITE_RATE_LIMIT)
async def create_user_account(
    request: Request,
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post("/login")
@limiter.limit(WRITE_RATE_LIMIT)
async def login_users(
    request: Request,
    login_data: UserLoginModel,
    session: AsyncSession = Depends(get_session),
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user and verify_password(password, user.password):
        access_token = create_access_token(
            user_data={"email": user.email, "user_uid": str(user.uid), "role": user.role}
        )

        refresh_token = create_access_token(
            user_data={"email": user.email, "user_uid": str(user.uid), "role": user.role},
            refresh=True,
            expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
        )

        return JSONResponse(
            content={
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {"email": user.email, "uid": str(user.uid)},
            }
        )

    raise InvalidCredentials()


@auth_router.get("/refresh")
@limiter.limit(DEFAULT_RATE_LIMIT)
async def get_new_access_token(
    request: Request,
    token_details: dict = Depends(RefreshTokenBearer()),
):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidCredentials()


@auth_router.get("/logout")
@limiter.limit(DEFAULT_RATE_LIMIT)
async def revoke_token(
    request: Request,
    token_details: dict = Depends(AccessTokenBearer()),
):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged out successfully"},
        status_code=status.HTTP_200_OK,
    )


@auth_router.get("/me", response_model=UserOut)
@limiter.limit(DEFAULT_RATE_LIMIT)
async def get_current_user_profile(
    request: Request,
    user=Depends(get_current_user),
):
    return user
