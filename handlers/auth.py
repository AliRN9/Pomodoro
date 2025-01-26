from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from dependecy import get_auth_service
from exception import UserNotCorrectPasswordException, UserNotFoundException
from service.auth import AuthService
from shema import UserLoginSchema, UserCreateSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginSchema)
async def login_user(user: UserCreateSchema,
                     auth_service: Annotated[AuthService, Depends(get_auth_service)],
                     ) -> UserLoginSchema:
    try:
        return auth_service.login(username=user.username, password=user.password)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=404,
            detail=e.detail
        )
    except UserNotCorrectPasswordException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )


@router.get("/login/google", response_class=RedirectResponse)
async def google_login(auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(url=redirect_url)


@router.get("/google")
async def google_auth(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
):
    print(code)
    return auth_service.google_auth(code=code)
