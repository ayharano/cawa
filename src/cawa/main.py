from fastapi import FastAPI

from . import __version__ as VERSION
from cawa.routers import v2023_11_0


app = FastAPI(
    title='cawa',
    summary=(
        'Proof of concept API application to provide a customer and warehouse'
        ' RESTful API.'
    ),
    version=VERSION,
)

app.include_router(v2023_11_0.router)
