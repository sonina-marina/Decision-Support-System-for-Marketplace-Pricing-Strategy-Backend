from fastapi import APIRouter, Depends
from src.core.auth.dependencies import get_current_user, require_role
from src.enums import UserRole
from src.schemas.user import (UserCreate, UserUpdateFullname, UserUpdatePassword, UserView, UserList)
from src.services.user import UserService
from src.api.dependencies import get_user_service


router = APIRouter(prefix='/users')


@router.post('/', response_model=UserView)
async def create_user(
    schema: UserCreate,
    user_service: UserService = Depends(get_user_service),
    user=Depends(
        get_current_user
    )
):

    return await user_service.create(schema)


@router.get('/', response_model=UserView)
async def get_by_id(
    id: int,
    user_service: UserService = Depends(get_user_service),
    user=Depends(
        get_current_user
    )
):

    return await user_service.get_by_id(id)


@router.get('/all', response_model=UserList)
async def get_all(
    user_service: UserService = Depends(get_user_service),
    user=Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await user_service.get_all()


@router.delete('/')
async def delete_by_id(
    id: int,
    user_service: UserService = Depends(get_user_service),
    user=Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await user_service.delete(id)


@router.put('/update_password', response_model=UserView)
async def update_password(
    schema: UserUpdatePassword,
    user_service: UserService = Depends(get_user_service),
    user=Depends(
        get_current_user
    )
):

    return await user_service.change_password(schema)


@router.put('/update_fullname', response_model=UserView)
async def update_fullname(
    schema: UserUpdateFullname,
    user_service: UserService = Depends(get_user_service),
    user=Depends(
        get_current_user
    )

):

    return await user_service.change_fullname(schema)
