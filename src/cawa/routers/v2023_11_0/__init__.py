from fastapi import APIRouter

from . import auth, customers


router = APIRouter(prefix='/v2023.11.0')

router.include_router(auth.router)
router.include_router(customers.router)
