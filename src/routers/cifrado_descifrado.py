from fastapi import APIRouter
from src.utils.RSA import RSA

from src.models.cifrado_descifrado_request import CifrarRequest, DescifrarRequest

router = APIRouter()
rsa = RSA()


@router.post("/cifrar/", tags=["RSA"])
async def cifrar(request: CifrarRequest):
    return {"mensaje_cifrado": rsa.cifrar(request.mensaje, request.llave_publica)}


@router.post("/descifrar/", tags=["RSA"])
async def descifrar(request: DescifrarRequest):
    print(request.mensaje)
    return {"mensaje_descifrado": rsa.descifrar(request.mensaje, request.llaves)}


@router.post("/generar_llaves/", tags=["RSA"])
async def generar_llaves():
    llaves: tuple = rsa.generar_claves()
    return {"Llave publica": llaves[0], "Llave privada": llaves[1]}
