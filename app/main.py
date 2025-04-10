from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.cifrado_descifrado import router as cifrado_descifrado_router
from app.routers.keys import router as keys_router
from app.routers.users import router as users_router
from app.utils.connections.Firebase_connection import connect_firebase
from app.utils.http_error_handler import HTTPErrorHandler


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_firebase()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(HTTPErrorHandler)

# Coleccion de las rutas
app.include_router(cifrado_descifrado_router)
app.include_router(users_router)
app.include_router(keys_router)
