from datetime import timedelta

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = ''
    DB_PASSWORD: str = ''
    DB_NAME: str = ''
    # DB_DRIVER: str = 'postgresql+psycopg2' синхронный драйвер
    DB_DRIVER: str = 'postgresql+asyncpg' #aсинхронный драйвер

    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

    JWT_SECRET_KEY: str = ''
    JWT_ENCODE_ALGORITHM: str = ''
    TOKEN_EXPIRE: timedelta = timedelta(days=7)


    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_REDIRECT_URI: str = ''
    GOOGLE_CLIENT_SECRET: str = ''
    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'

    YANDEX_CLIENT_ID: str = ''
    YANDEX_CLIENT_SECRET: str = ''
    YANDEX_REDIRECT_URI: str = ''

    YANDEX_TOKEN_URL: str = 'https://oauth.yandex.ru/token'

    @property
    def db_url(self) -> str:
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def google_redirect_url(self) -> str:
        return f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"


    @property
    def yandex_redirect_url(self) -> str:
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&force_confirm=yes"