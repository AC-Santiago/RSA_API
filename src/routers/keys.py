import json
import os
from typing import Annotated

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from firebase_admin import firestore_async

from src.models.usuario_key import UsuarioKey
from src.utils.auth import get_current_user
from src.utils.connections.Firebase_config import get_firebase_config

router = APIRouter()
firebase = get_firebase_config()


@router.post("/save_keys/", tags=["keys"])
async def save_keys(
    user: Annotated[dict, Depends(get_current_user)], llaves_usuario: UsuarioKey
):
    llaves_usuario = llaves_usuario.dict()
    db = firestore_async.client()
    sentencia = (
        db.collection("usuarios")
        .document(user["uid"])
        .collection("Llaves")
        .document(llaves_usuario["nombre_llaves"])
    )
    consulta = await sentencia.get()
    if consulta.exists:
        return JSONResponse(
            content={"mensaje": "Las llaves ya existen"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    load_dotenv()
    llave_encrypt = os.getenv("KEY_ENCRYPT")
    f = Fernet(llave_encrypt.encode())
    llave_privada_encrypt = f.encrypt(str(llaves_usuario["llave_privada"]).encode())
    llave_publica_encrypt = f.encrypt(str(llaves_usuario["llave_publica"]).encode())
    llave_guardar = {
        "llave_publica": llave_publica_encrypt,
        "llave_privada": llave_privada_encrypt,
    }
    await sentencia.set(llave_guardar)
    return JSONResponse(
        content={"mensaje": "Llaves almacenadas correctamente"},
        status_code=status.HTTP_200_OK,
    )


@router.get("/get_keys/", tags=["keys"])
async def get_keys(user: Annotated[dict, Depends(get_current_user)]):
    db = firestore_async.client()
    sentencia = db.collection("usuarios").document(user["uid"]).collection("Llaves")
    consulta = await sentencia.get()
    llaves = []
    for llave in consulta:
        llave = llave.to_dict()
        load_dotenv()
        llave_encrypt = os.getenv("KEY_ENCRYPT")
        f = Fernet(llave_encrypt.encode())
        llave["llave_publica"] = json.loads(f.decrypt(llave["llave_publica"]).decode())
        llave["llave_privada"] = json.loads(f.decrypt(llave["llave_privada"]).decode())
        llaves.append(llave)
    return JSONResponse(content={"llaves": llaves}, status_code=status.HTTP_200_OK)


@router.get("/get_key/{nombre_llaves}", tags=["keys"])
async def get_key(user: Annotated[dict, Depends(get_current_user)], nombre_llaves: str):
    db = firestore_async.client()
    sentencia = (
        db.collection("usuarios")
        .document(user["uid"])
        .collection("Llaves")
        .document(nombre_llaves)
    )
    consulta = await sentencia.get()
    if not consulta.exists:
        return JSONResponse(
            content={"mensaje": "Las llaves no existen"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    llave = consulta.to_dict()
    load_dotenv()
    llave_encrypt = os.getenv("KEY_ENCRYPT")
    f = Fernet(llave_encrypt.encode())
    llave["llave_publica"] = json.loads(f.decrypt(llave["llave_publica"]).decode())
    llave["llave_privada"] = json.loads(f.decrypt(llave["llave_privada"]).decode())
    return JSONResponse(content={"llave": llave}, status_code=status.HTTP_200_OK)
