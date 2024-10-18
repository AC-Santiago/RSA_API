from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.models.cifrado_descifrado_request import CifrarRequest, DescifrarRequest
from src.utils.auth import get_current_user
from src.utils.RSA import RSA

router = APIRouter()


@router.post("/cifrar/", tags=["RSA"])
def cifrar(request: CifrarRequest, user: Annotated[dict, Depends(get_current_user)]):
    rsa = RSA()
    return JSONResponse(
        content={"mensaje_cifrado": rsa.cifrar(request.mensaje, request.llave_publica)},
        status_code=status.HTTP_200_OK,
    )


@router.post("/descifrar/", tags=["RSA"])
def descifrar(
    request: DescifrarRequest, user: Annotated[dict, Depends(get_current_user)]
):
    rsa = RSA()
    return JSONResponse(
        content={
            "mensaje_descifrado": rsa.descifrar(request.mensaje, request.llave_privada)
        },
        status_code=status.HTTP_200_OK,
    )


@router.post("/generar_llaves/", tags=["RSA"])
def generar_llaves(user: Annotated[dict, Depends(get_current_user)]):
    rsa = RSA()
    llaves: tuple = rsa.generar_claves()
    return JSONResponse(
        content={"llave_publica": llaves[0], "llave_privada": llaves[1]},
        status_code=status.HTTP_200_OK,
    )
