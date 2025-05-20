from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from app.dependecy import get_auth_service
from app.exception import UserNotCorrectPasswordException, UserNotFoundException
from app.users.auth.service import AuthService
from app.users.user_profile.shema import UserCreateSchema
from app.users.auth.shema import UserLoginSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginSchema)
async def login_user(
    user: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserLoginSchema:
    try:
        return await auth_service.login(username=user.username, password=user.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)


@router.get("/login/google", response_class=RedirectResponse)
async def google_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(url=redirect_url)


@router.get("/google")
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    return await auth_service.google_auth(code=code)


@router.get("/login/yandex", response_class=RedirectResponse)
async def yandex_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(url=redirect_url)


@router.get("/yandex")
async def yandex_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)], code: str
):
    return await auth_service.yandex_auth(code=code)
