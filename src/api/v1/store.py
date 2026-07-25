from fastapi import APIRouter, Depends
from src.schemas.store import (StoreCreate, StoreList, StoreUpdate, StoreView)
from src.services.store import StoreService
from src.api.dependencies import get_store_service


router = APIRouter(prefix='/stores')


@router.post('/', response_model=StoreView)
async def create_store(
    schema: StoreCreate,
    store_service: StoreService = Depends(get_store_service)
):

    return await store_service.create(schema)


@router.get('/', response_model=StoreView)
async def get_by_id(
    id: int,
    store_service: StoreService = Depends(get_store_service)
):

    return await store_service.get_by_id(id)


@router.get('/all', response_model=StoreList)
async def get_all(
    store_service: StoreService = Depends(get_store_service)
):

    return await store_service.get_all()


@router.delete('/')
async def delete_by_id(
    id: int,
    store_service: StoreService = Depends(get_store_service)
):

    return await store_service.delete(id)


@router.put('/', response_model=StoreView)
async def update(
    schema: StoreUpdate,
    store_service: StoreService = Depends(get_store_service),
):

    return await store_service.update(schema)
