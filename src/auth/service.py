from typing import Optional

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.auth.schemas import UserCreateModel
from src.auth.utils import generate_password_hash


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession) -> User:
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password = generate_password_hash(user_data_dict["password"])

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


user_service = UserService()
