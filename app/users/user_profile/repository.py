from dataclasses import dataclass
from typing import Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.user_profile.models import UserProfile as DBUser

from app.users.user_profile.shema import UserCreateSchema


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def create_user(self, user: UserCreateSchema) -> DBUser:
        query = (
            insert(DBUser)
            .values(
                **user.model_dump(),
            )
            .returning(DBUser.id)
        )

        async with self.db_session as session:
            user_id: DBUser.id = (await session.execute(query)).scalar()
            await session.commit()
            await session.flush()
            return await self.get_user(user_id)

    async def get_user(self, user_id: int) -> DBUser:
        query = select(DBUser).where(DBUser.id == user_id)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[DBUser]:
        user = select(DBUser).where(DBUser.username == username)
        async with self.db_session as session:
            return (await session.execute(user)).scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> DBUser:  # Optional[DBUser]:
        query = select(DBUser).where(DBUser.email == email)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()
