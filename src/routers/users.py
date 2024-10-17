from fastapi import APIRouter, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from firebase_admin import auth

from src.models.usuario import Usuario
from src.utils.connections.Firebase_config import get_firebase_config

router = APIRouter()
firebase = get_firebase_config()


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
async def login_user(user: Usuario):
    email = user.correo
    contraseña = user.contraseña
    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email, password=contraseña
        )
        token = user["idToken"]
        return JSONResponse(content={"token": token}, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user


@router.post("/check_token/", tags=["users"])
async def check_token(request: Request):
    headers = request.headers
    token = headers["Authorization"]
    user = auth.verify_id_token(token)
    return JSONResponse(content={"user": user}, status_code=status.HTTP_200_OK)
