import os

import firebase_admin
from firebase_admin import credentials, firestore_async
from google.cloud.firestore import AsyncClient

from app.core.config import get_settings


settings = get_settings()


def connect_firebase():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    firebase_key = settings.FIRE_BASE_KEY.strip('"').strip("'")
    path = os.path.join(base_dir, "app", "json", firebase_key)

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"El archivo de credenciales no existe en: {path}"
        )

    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred)


async def get_client() -> AsyncClient:
    if not firebase_admin._apps:
        connect_firebase()
    return firestore_async.client()
