from fastapi import APIRouter, Depends

from src.api.dependencies import get_auth_service
from src.schemas.login import LoginSchema
from src.services.auth import AuthService

router = APIRouter(prefix='/login')

@router.post('/')
async def login(
    schema: LoginSchema,
    auth_service: AuthService = Depends(get_auth_service)
):
    
    token = await auth_service.login(schema)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
