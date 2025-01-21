from typing import Annotated

from fastapi import APIRouter, Depends

from dependecy import get_users_service
from shema import UserLoginSchema, UserCreateSchema
from service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserLoginSchema)
async def create_user(user: UserCreateSchema,
                      user_service: Annotated[UserService, Depends(get_users_service)],
                      ) -> UserLoginSchema:
    return user_service.create_user(username=user.username, password=user.password)
