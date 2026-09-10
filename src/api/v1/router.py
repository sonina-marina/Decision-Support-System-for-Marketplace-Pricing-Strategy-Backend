from fastapi import APIRouter

from src.api.v1.user import router as user_router
from src.api.v1.store import router as store_router
from src.api.v1.product import router as product_router
from src.api.v1.metrics import router as metrics_router

router = APIRouter(prefix='/v1')

router.include_router(user_router)
router.include_router(store_router)
router.include_router(product_router)
router.include_router(metrics_router)
