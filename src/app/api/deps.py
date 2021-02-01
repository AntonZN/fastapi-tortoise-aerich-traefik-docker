import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist

from app import schemas
from app.core import security
from app.core.config import get_settings
from app.models.user import UserPydantic, User

settings = get_settings()

auth_scheme = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> UserPydantic:
    try:
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    try:
        return await User.get(id=token_data.sub)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist"
        )


async def get_current_active_user(
    current_user: UserPydantic = Depends(get_current_user),
) -> UserPydantic:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return await UserPydantic.from_tortoise_orm(current_user)


async def get_current_super_user(
    current_user: UserPydantic = Depends(get_current_user),
) -> UserPydantic:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is not super user"
        )
    return current_user
