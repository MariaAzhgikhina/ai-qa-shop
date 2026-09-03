from fastapi import APIRouter

from app.api.cart.routes import router as cart_router
from app.api.orders.routes import router as orders_router
from app.api.products.routes import router as products_router


router = APIRouter(prefix="/api")
router.include_router(products_router)
router.include_router(cart_router)
router.include_router(orders_router)
