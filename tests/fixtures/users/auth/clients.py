from dataclasses import dataclass

import httpx
import pytest
from app.settings import Settings
from app.users.auth.shema import GoogleUserData, YandexUserData

from faker import Factory as FakerFactory

faker = FakerFactory.create()


@dataclass
class FakeGoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def _get_user_access_token(self, code: str) -> str:
        return faker.sha256()

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        user_info: dict = self.google_user_info_data()
        return GoogleUserData(**user_info, access_token=access_token)

    def google_user_info_data(self) -> dict:
        return {
            "id": faker.random_int(),
            "email": faker.email(),
            "verified_email": True,
            "name": faker.name()
        }


@dataclass
class FakeYandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        access_token = await self._get_user_access_token(code=code)
        user_info: dict = self.yandex_user_info_data()
        return YandexUserData(**user_info, access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        return f"fake_access_token: {code}"

    def yandex_user_info_data(self) -> dict:
        return {
            "id": faker.random_int(),
            "login": faker.name(),
            "real_name": faker.name(),
            "default_email": faker.email(),
            "verified_email": True,
        }


@pytest.fixture
def google_client():
    return FakeGoogleClient(settings=Settings(), async_client=httpx.AsyncClient())


@pytest.fixture
def yandex_client():
    return FakeYandexClient(settings=Settings(), async_client=httpx.AsyncClient())
