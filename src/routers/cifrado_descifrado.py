from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.models.cifrado_descifrado_request import CifrarRequest, DescifrarRequest
from src.utils.RSA import RSA

router = APIRouter()


@router.post("/cifrar/", tags=["RSA"])
def cifrar(request: CifrarRequest):
    rsa = RSA()
    print(f"Mensaje de rsa {request.mensaje}")
    print(f"Mensaje guardado en laclase RSA {rsa.mensaje_cifrado}")
    return JSONResponse(
        content={"mensaje_cifrado": rsa.cifrar(request.mensaje, request.llave_publica)},
        status_code=status.HTTP_200_OK,
    )


@router.post("/descifrar/", tags=["RSA"])
def descifrar(request: DescifrarRequest):
    rsa = RSA()
    return JSONResponse(
        content={
            "mensaje_descifrado": rsa.descifrar(request.mensaje, request.llave_privada)
        },
        status_code=status.HTTP_200_OK,
    )


@router.post("/generar_llaves/", tags=["RSA"])
def generar_llaves():
    rsa = RSA()
    llaves: tuple = rsa.generar_claves()
    return JSONResponse(
        content={"llave_publica": llaves[0], "llave_privada": llaves[1]},
        status_code=status.HTTP_200_OK,
    )
