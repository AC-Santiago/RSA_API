from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.utils.connections.Firebase_config import get_firebase_config

firebase = get_firebase_config()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def authenticate_user(request_form: Annotated[OAuth2PasswordRequestForm, Depends]):
    email = request_form.username
    contraseña = request_form.password
    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email, password=contraseña
        )
        token = user["idToken"]
        return token
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
