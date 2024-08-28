from fastapi import FastAPI
from src.routers.cifrado_descifrado import router as cifrado_descifrado_router

app = FastAPI()

app.include_router(cifrado_descifrado_router)
