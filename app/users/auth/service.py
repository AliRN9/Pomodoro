from dataclasses import dataclass
from datetime import datetime

from black import timezone

from app.users.auth.client import GoogleClient, YandexClient, MailClient
from app.exception import UserNotFoundException, UserNotCorrectPasswordException, TokenNotCorrect

from app.users.user_profile.models import UserProfile as DBUser
from app.users.user_profile.repository import UserRepository
from app.settings import Settings
from app.users.user_profile.shema import UserCreateSchema
from app.users.auth.shema import GoogleUserData, YandexUserData, UserLoginSchema
from jose import jwt
from jose.exceptions import JWTError


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient
    mail_client: MailClient

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user: DBUser = await self.user_repository.get_user_by_username(username)
        self.__validate_auth_user(user, password)
        access_token = self.generate_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def __validate_auth_user(user: DBUser, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_token(self, user_id: int) -> str:
        expires_data_inix = (datetime.now(timezone.utc) + self.settings.TOKEN_EXPIRE).timestamp()
        token = jwt.encode(
            {'user_id': user_id, 'exp': expires_data_inix},
            key=self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM
        )
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(token=access_token, key=self.settings.JWT_SECRET_KEY,
                                 algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrect
        # if payload['expire'] < datetime.utcnow().timestamp():
        #     raise TokenExpire
        return payload['user_id']

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    async def google_auth(self, code: str) -> UserLoginSchema:
        user_data: GoogleUserData = await self.google_client.get_user_info(code=code)
        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_token(user_id=user.id)

            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            email=user_data.email,
            name=user_data.name,
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_token(user_id=created_user.id)
        self.mail_client.send_welcome_email(to=user_data.email)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    async def yandex_auth(self, code: str) -> UserLoginSchema:
        user_data: YandexUserData = await self.yandex_client.get_user_info(code=code)
        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_token(user_id=user.id)

            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            email=user_data.email,
            name=user_data.name,
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_token(user_id=created_user.id)
        self.mail_client.send_welcome_email(to=user_data.email)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)
