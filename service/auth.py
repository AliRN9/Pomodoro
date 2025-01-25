from dataclasses import dataclass
from datetime import datetime, timedelta
from exception import UserNotFoundException, UserNotCorrectPasswordException, TokenExpire, TokenNotCorrect
from models import UserProfile as DBUser
from repository import UserRepository
from settings import Settings
from shema import UserLoginSchema
from jose import jwt
from jose.exceptions import JWTError


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        user: DBUser = self.user_repository.get_user_by_username(username)
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
        expires_data_inix = (datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode(
            {'user_id': user_id, 'expire': expires_data_inix},
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
        if payload['expire'] < datetime.utcnow().timestamp():
            raise TokenExpire
        return payload['user_id']
