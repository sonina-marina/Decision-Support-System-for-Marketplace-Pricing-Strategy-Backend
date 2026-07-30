from fastapi import APIRouter, Depends
from src.core.auth.dependencies import get_current_user, require_role
from src.enums import UserRole
from src.schemas.product import (ProductCreate, ProductDetailedView, ProductList, ProductUpdate, ProductView)
from src.services.product import ProductService
from src.api.dependencies import get_product_service


router = APIRouter(prefix='/products')


@router.post('/', response_model=ProductView)
async def create_product(
    schema: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
    user=Depends(
        get_current_user
    )
):

    return await product_service.create(schema)


@router.get('/', response_model=ProductView)
async def get_by_id(
    id: int,
    product_service: ProductService = Depends(get_product_service),
    user=Depends(
        get_current_user
    )
):

    return await product_service.get_by_id(id)


@router.get('/all', response_model=ProductList)
async def get_all(
    product_service: ProductService = Depends(get_product_service),
    user=Depends(
        require_role(UserRole.ADMIN)
    )
):

    return await product_service.get_all()


@router.get('/by_user', response_model=ProductList)
async def get_product_by_store_id(
    id: int,
    product_service: ProductService = Depends(get_product_service),
    user=Depends(
        get_current_user
    )
):

    return await product_service.get_product_by_store_id(id)


@router.delete('/')
async def delete_by_id(
    id: int,
    product_service: ProductService = Depends(get_product_service),
    user=Depends(
        get_current_user
    )
):

    return await product_service.delete(id)


@router.put('/', response_model=ProductView)
async def update(
    schema: ProductUpdate,
    product_service: ProductService = Depends(get_product_service),
    user=Depends(
        get_current_user
    )
):

    return await product_service.update(schema)

@router.get('/metrics/', response_model=ProductDetailedView)
async def get_product_with_metrics(
    id: int,
    product_service: ProductService = Depends(get_product_service),
    user=Depends(
        get_current_user
    )
):

    return await product_service.get_product_with_metric_by_id(id)
