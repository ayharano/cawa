from fastapi import FastAPI

from . import __version__ as VERSION


app = FastAPI(
    title='cawa',
    summary=(
        'Proof of concept API application to provide a customer and warehouse'
        ' RESTful API.'
    ),
    version=VERSION,
)
