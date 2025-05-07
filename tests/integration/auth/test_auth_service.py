from httpx import AsyncClient

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.users.user_profile.models import UserProfile
from fastapi import status


async def test_google_auth__login_not_exist_user__success(auth_service, db_session: AsyncSession):
    code = "fake_code"

    async with db_session as session:
        users = (await session.execute(select(UserProfile))).scalars().all()

    user = await auth_service.google_auth(code)

    assert len(users) == 0
    assert user is not None

    async with db_session as session:
        users = (await session.execute(select(UserProfile))).scalars().all()
        login_user = (
            await session.execute(select(UserProfile).where(UserProfile.id == user.user_id))).scalars().first()

    assert len(users) != 0
    assert login_user is not None


async def test_login_user__success(auth_service, db_session: AsyncSession):
    username = 'test_user'
    password = 'test_password'

    query = insert(UserProfile).values(username=username, password=password)
    async with db_session as session:
        await session.execute(query)
        await session.commit()

    user = await auth_service.login(username, password)

    async with session as session:
        login_user = (
            await session.execute(select(UserProfile).where(UserProfile.username == username))).scalar_one_or_none()


    assert login_user is not None
    assert user.user_id == login_user.id


#

async def test_get_tasks_path__fail(anonymous_client: AsyncClient):
    response = await anonymous_client.get("/task/all")

    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_google_auth___create_tasks(auth_service, db_session: AsyncSession, anonymous_client: AsyncClient):
    pass

    # тут надо лучше продумать

    # code = "fake_code"
    # session: AsyncSession = db_session
    #
    # user = await auth_service.google_auth(code)
    # anonymous_client.headers = {"Authorization": f"Bearer {user.access_token}"}
    #
    # data = {
    #     "name": "test_task",
    #     "pomodoro_count": 1,
    #     "category_id": 2
    # }
    # response = await anonymous_client.post("/task/", json=data)
    #
    # async with session as session:
    #     users = (await session.execute(select(UserProfile))).scalars().all()
    # print(f"{users=}")
    #
    # async with session as session:
    #     tasks = (await session.execute(select(Tasks))).scalars().all()
    #
    #
    # assert response.status_code == status.HTTP_200_OK
    # assert len(tasks) == 1
