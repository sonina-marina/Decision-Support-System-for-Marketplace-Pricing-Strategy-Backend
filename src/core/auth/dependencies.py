import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.auth.security import decode_access_token
from src.services.exceptions import ForbiddenError, UnauthorizedError

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    )
):

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        return payload

    except jwt.InvalidTokenError:
        raise UnauthorizedError()


def require_role(*roles):

    async def checker(
        user=Depends(get_current_user)
    ):

        if user["role"] not in roles:
            raise ForbiddenError()

        return user

    return checker
