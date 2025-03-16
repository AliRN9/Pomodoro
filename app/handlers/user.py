from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependecy import get_users_service
from app.shema import UserLoginSchema, UserCreateSchema
from app.service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserLoginSchema)
async def create_user(user: UserCreateSchema,
                      user_service: Annotated[UserService, Depends(get_users_service)],
                      ) -> UserLoginSchema:
    return await user_service.create_user(username=user.username, password=user.password)
