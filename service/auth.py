from dataclasses import dataclass

from exception import UserNotFoundException, UserNotCorrectPasswordException
from models import UserProfile as DBUser
from repository import UserRepository
from shema import UserLoginSchema


@dataclass
class AuthService:
    user_repository: UserRepository

    def login(self, username: str, password: str) -> UserLoginSchema:
        user: DBUser = self.user_repository.get_user_by_username(username)
        self.__validate_auth_user(user, password)

        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def __validate_auth_user(user: DBUser, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
