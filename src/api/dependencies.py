from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import status

from core.config import settings


api_key_header = APIKeyHeader(name='X-API-KEY', auto_error=False)


async def verify_credentials(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )
    if api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Forbidden'
        )
    return api_key
