import os

import firebase_admin
from firebase_admin import credentials, firestore_async
from google.cloud.firestore import AsyncClient

from src.core.config import get_settings


settings = get_settings()


def connect_firebase():
    separador = os.path.sep
    directory = os.path.dirname(os.path.abspath(__file__))
    dir_prev = f"{separador}".join(directory.split(separador)[:-2])

    path = os.path.join(dir_prev, "json", settings.FIRE_BASE_KEY)

    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred)


async def get_client() -> AsyncClient:
    if not firebase_admin._apps:
        connect_firebase()
    return firestore_async.client()
