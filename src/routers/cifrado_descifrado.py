from fastapi import APIRouter, status
from src.utils.RSA import RSA
from fastapi.responses import JSONResponse

from src.models.cifrado_descifrado_request import CifrarRequest, DescifrarRequest

router = APIRouter()
rsa = RSA()


@router.post("/cifrar/", tags=["RSA"])
async def cifrar(request: CifrarRequest):
    return JSONResponse(content={"mensaje_cifrado": rsa.cifrar(request.mensaje, request.llave_publica)},
                        status_code=status.HTTP_200_OK)


@router.post("/descifrar/", tags=["RSA"])
async def descifrar(request: DescifrarRequest):
    return JSONResponse(content={"mensaje_descifrado": rsa.descifrar(request.mensaje, request.llave_privada)},
                        status_code=status.HTTP_200_OK)


@router.post("/generar_llaves/", tags=["RSA"])
async def generar_llaves():
    llaves: tuple = rsa.generar_claves()
    return JSONResponse(content={"llave_publica": llaves[0], "llave_privada": llaves[1]},
                        status_code=status.HTTP_200_OK)
