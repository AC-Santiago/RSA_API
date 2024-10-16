import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials

load_dotenv()


def connect_firebase():
    separador = os.path.sep
    directory = os.path.dirname(os.path.abspath(__file__))
    dir_prev = f"{separador}".join(directory.split(separador)[:-2])

    path = os.path.join(dir_prev, "json", os.getenv("FIRE_BASE_KEY"))

    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred)
