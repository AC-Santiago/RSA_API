from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from firebase_admin import auth

from src.models.usuario import Usuario
from src.utils.connections.Firebase_config import get_firebase_config

router = APIRouter()
firebase = get_firebase_config()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/singup/", tags=["users"])
async def register_user(user: Usuario):
    try:
        user = auth.create_user(
            email=user.correo, password=user.contraseña, display_name=user.nombre
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user


@router.post("/login/", tags=["users"])
async def login_user(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    email = user.username
    contraseña = user.password
    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email, password=contraseña
        )
        token = user["idToken"]
        return JSONResponse(
            content={"access_token": token}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user


@router.post("/check_token/", tags=["users"])
async def check_token(token_jwt: Annotated[str, Depends(oauth2_scheme)]):
    user = auth.verify_id_token(token_jwt)
    return JSONResponse(content={"user": user}, status_code=status.HTTP_200_OK)
