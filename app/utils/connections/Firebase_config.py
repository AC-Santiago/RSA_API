import pyrebase
from src.core.config import get_settings


settings = get_settings()

config = {
    "apiKey": settings.APY_KEY,
    "authDomain": settings.AUTH_DOMAIN,
    "projectId": settings.PROJECT_ID,
    "storageBucket": settings.STORAGE_BUCKET,
    "messagingSenderId": settings.MESSAGING_SENDER_ID,
    "appId": settings.APP_ID,
    "measurementId": settings.MEASUREMENT_ID,
    "databaseURL": settings.DATABASE_URL,
}


def get_firebase_config():
    firebase = pyrebase.initialize_app(config)
    return firebase
