from concurrent.futures import ThreadPoolExecutor
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import JSONResponse

from src.models.cifrado_descifrado_request import (
    CifrarRequest,
    DescifrarRequest,
)
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


@router.post("/cifrar/file/", tags=["RSA"])
async def cifrar_file(
    user: Annotated[dict, Depends(get_current_user)],
    archivo: Annotated[UploadFile, File(...)],
    llave_publica: str = Form(...),
):
    try:
        llave_publica = [int(i) for i in llave_publica.split(",")]
    except ValueError:
        return JSONResponse(  # noqa
            content={"detail": "La llave publica debe ser una lista de enteros"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if archivo.content_type != "text/plain":
        return JSONResponse(
            content={"detail": "El archivo debe ser de tipo texto plano"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    contenido_byte: bytes = await archivo.read()
    size_chunk = 1024
    chunks = [
        contenido_byte[i : i + size_chunk]
        for i in range(0, len(contenido_byte), size_chunk)
    ]

    rsa = RSA()

    def cifrar_chunck(chunk: bytes):
        return rsa.cifrar(chunk.decode("utf-8"), llave_publica)

    with ThreadPoolExecutor() as executor:
        contenido_byte = "".join(executor.map(cifrar_chunck, chunks))

    return JSONResponse(
        content={"mensaje_cifrado": f"{contenido_byte}"},
        status_code=status.HTTP_200_OK,
    )
