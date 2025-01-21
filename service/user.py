import string
from dataclasses import dataclass
from random import random, choice

from repository import UserRepository
from shema import UserLoginSchema


@dataclass
class UserService:
    user_repository: UserRepository

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        access_token = self._generate_token()
        user = self.user_repository.create_user(username=username, password=password, access_token=access_token)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _generate_token() -> str:
        return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(32))
