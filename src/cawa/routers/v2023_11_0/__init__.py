from fastapi import APIRouter

from . import auth, customers, warehouses


router = APIRouter(prefix='/v2023.11.0')

router.include_router(auth.router)
router.include_router(customers.router)
router.include_router(warehouses.router)
