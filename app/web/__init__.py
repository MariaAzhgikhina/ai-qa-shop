from fastapi import APIRouter

from app.web.cart.routes import router as cart_router
from app.web.orders.routes import router as orders_router
from app.web.products.routes import router as products_router


router = APIRouter()
router.include_router(products_router)
router.include_router(cart_router)
router.include_router(orders_router)
