import os
from typing import Annotated

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from firebase_admin import auth, firestore_async

from src.models.usuario import Usuario
from src.models.usuario_key import UsuarioKey
from src.utils.auth import get_current_user
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
    return JSONResponse(content={"message": "Usuario creado exitosamente"})


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


@router.post("/save_keys/", tags=["users"])
async def save_keys(
    user: Annotated[dict, Depends(get_current_user)], llaves_usuario: UsuarioKey
):
    llaves_usuario = llaves_usuario.dict()

    load_dotenv()
    llave_encrypt = os.getenv("KEY_ENCRYPT")
    f = Fernet(llave_encrypt.encode())
    print(llaves_usuario)
    llave_privada_encrypt = f.encrypt(str(llaves_usuario["llave_privada"]).encode())
    llave_publica_encrypt = f.encrypt(str(llaves_usuario["llave_publica"]).encode())
    db = firestore_async.client()
    llave_guardar = {
        "llave_publica": llave_publica_encrypt,
        "llave_privada": llave_privada_encrypt,
    }
    await (
        db.collection("usuarios")
        .document(user["uid"])
        .collection(llaves_usuario["nombre_llaves"])
        .set(llave_guardar)
    )
    return JSONResponse(
        content={"User id": user["uid"]}, status_code=status.HTTP_200_OK
    )
