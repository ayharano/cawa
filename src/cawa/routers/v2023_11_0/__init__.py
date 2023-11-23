from fastapi import APIRouter

from . import auth


router = APIRouter(prefix='/v2023.11.0')

router.include_router(auth.router)
