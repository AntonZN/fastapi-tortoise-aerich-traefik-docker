from datetime import timedelta
from typing import Any

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_versioning import version

from app import schemas
from app.api import deps
from app.core import security
from app.core.config import get_settings
from app.models.user import User, UserPydantic

settings = get_settings()
router = APIRouter()


@router.post(
    "/login/",
    response_model=schemas.Token,
    responses={status.HTTP_400_BAD_REQUEST: {"model": schemas.HTTPBadRequest}},
)
@version(1)
async def login(form_data: schemas.UserLogin) -> Any:
    user = await User.get_or_none(email=form_data.email)
    if not user or security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token)


@router.get(
    "/profile",
    response_model=UserPydantic,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": schemas.HTTPBadRequest},
        status.HTTP_401_UNAUTHORIZED: {"model": schemas.HTTPUnauthorized},
        status.HTTP_403_FORBIDDEN: {"model": schemas.HTTPForbidden},
        status.HTTP_404_NOT_FOUND: {"model": schemas.HTTPNotFound},
    },
)
@version(1)
async def read_user(
    current_user: UserPydantic = Depends(deps.get_current_active_user),
) -> Any:
    return current_user
