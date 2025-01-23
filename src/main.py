from fastapi import FastAPI

from src.routers.cifrado_descifrado import router as cifrado_descifrado_router
from src.routers.keys import router as keys_router
from src.routers.users import router as users_router
from src.utils.connections.Firebase_connection import connect_firebase
from src.utils.http_error_handler import HTTPErrorHandler

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    connect_firebase()


app.add_middleware(HTTPErrorHandler)

# Coleccion de las rutas
app.include_router(cifrado_descifrado_router)
app.include_router(users_router)
app.include_router(keys_router)
