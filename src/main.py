from fastapi import FastAPI
from src.routers.cifrado_descifrado import router as cifrado_descifrado_router
from src.utils.http_error_handler import HTTPErrorHandler

app = FastAPI()

app.add_middleware(HTTPErrorHandler)

app.include_router(cifrado_descifrado_router)
