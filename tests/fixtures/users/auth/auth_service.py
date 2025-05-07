from app.settings import Settings
from app.users.auth.service import AuthService
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.user_profile.repository import UserRepository
import pytest_asyncio


@pytest.fixture
def mock_auth_service(yandex_client, google_client, fake_user_repository) -> AuthService:
    return AuthService(
        user_repository=fake_user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client
    )


@pytest_asyncio.fixture
async def auth_service(yandex_client, google_client, settings: Settings, db_session: AsyncSession) -> AuthService:
    return AuthService(
        user_repository=UserRepository(db_session=db_session),
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client
    )
