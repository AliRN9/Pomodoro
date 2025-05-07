from datetime import datetime, timezone, timedelta

from app.settings import Settings
from app.users.auth.service import AuthService
from jose import jwt

from app.users.auth.shema import UserLoginSchema



async def test_get_google_redirect_url__success(mock_auth_service: AuthService, settings: Settings):
    google_redirect_url = mock_auth_service.get_google_redirect_url()

    assert google_redirect_url == settings.google_redirect_url


def test_get_yandex_redirect_url__success(mock_auth_service: AuthService, settings: Settings):
    yandex_redirect_url = mock_auth_service.get_yandex_redirect_url()
    assert yandex_redirect_url == settings.yandex_redirect_url



async def test_regenerate_access_token__success(mock_auth_service: AuthService, settings: Settings):
    user_id = 1

    access_token = mock_auth_service.generate_token(user_id)

    decode_access_token = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ENCODE_ALGORITHM])
    decoded_user_id = decode_access_token['user_id']

    decoded_access_expire = datetime.fromtimestamp(decode_access_token['exp'], timezone.utc)

    assert decoded_user_id == user_id
    assert timedelta(days=7) > decoded_access_expire - datetime.now(timezone.utc) > timedelta(days=6)


async def test_user_id_from_access_token__success(mock_auth_service: AuthService):
    user_id = 1

    access_token = mock_auth_service.generate_token(user_id)
    decode_user_id = mock_auth_service.get_user_id_from_access_token(access_token)
    assert decode_user_id == user_id


async def test_google_auth__success(mock_auth_service: AuthService):
    code = "fake code"

    user = await mock_auth_service.google_auth(code)
    decode_user_id = mock_auth_service.get_user_id_from_access_token(user.access_token)

    assert user.user_id == decode_user_id
    assert isinstance(user, UserLoginSchema)


async def test_yandex_auth__success(mock_auth_service: AuthService):
    code = "fake code"

    user = await mock_auth_service.yandex_auth(code)
    decode_user_id = mock_auth_service.get_user_id_from_access_token(user.access_token)

    assert user.user_id == decode_user_id
    assert isinstance(user, UserLoginSchema)