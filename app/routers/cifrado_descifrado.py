import os
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse

from app.models.cifrado_descifrado_request import (
    CifrarRequest,
    DescifrarRequest,
)
from app.utils.auth import get_current_user
from app.utils.RSA import RSA

router = APIRouter()

SEPARATOR = os.path.sep


@router.post("/cifrar/", tags=["RSA"])
def cifrar(
    request: CifrarRequest, user: Annotated[dict, Depends(get_current_user)]
):
    rsa = RSA()
    return JSONResponse(
        content={
            "mensaje_cifrado": rsa.cifrar(
                request.mensaje, request.llave_publica
            )
        },
        status_code=status.HTTP_200_OK,
    )


@router.post("/descifrar/", tags=["RSA"])
def descifrar(
    request: DescifrarRequest, user: Annotated[dict, Depends(get_current_user)]
):
    rsa = RSA()
    print(f"request.mensaje: {request.mensaje}")
    return JSONResponse(
        content={
            "mensaje_descifrado": rsa.descifrar(
                request.mensaje, request.llave_privada
            )
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


def create_file_txt(content: bytes, path: str) -> None:
    with open(f"{path}.txt", "wb") as file:
        file.write(content)


@router.post("/cifrar/file/", tags=["RSA"])
async def cifrar_file(
    user: Annotated[dict, Depends(get_current_user)],
    archivo: Annotated[UploadFile, File(...)],
    llave_publica: str = Form(...),
):
    try:
        llave_publica = [int(i) for i in llave_publica.split(",")]
    except ValueError:
        return JSONResponse(
            content={
                "detail": "La llave publica debe ser una lista de enteros"
            },
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
        lista_mensajes_cifrados = list(executor.map(cifrar_chunck, chunks))
    contenido: str = ",".join(lista_mensajes_cifrados)

    file_name: str = "cifrado"
    file = create_file_txt(
        contenido.encode("utf-8"), f"files{SEPARATOR}{file_name}"
    )
    path: str = os.path.abspath(
        os.path.join(os.getcwd(), "files", f"{file_name}.txt")
    )
    print(f"Path: {path}")
    if not os.path.exists(path):
        return JSONResponse(
            content={"detail": "No se pudo crear el archivo"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return FileResponse(
        media_type="text/plain",
        status_code=status.HTTP_200_OK,
        path=path,
        filename="cifrado.txt",
    )


@router.post("/descifrar/file/", tags=["RSA"])
async def descifrar_file(
    user: Annotated[dict, Depends(get_current_user)],
    archivo: Annotated[UploadFile, File(...)],
    llave_privada=Form(...),
):
    try:
        llave_privada = [int(i) for i in llave_privada.split(",")]
    except ValueError:
        return JSONResponse(
            content={
                "detail": "La llave privada debe ser una lista de enteros"
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if archivo.content_type != "text/plain":
        return JSONResponse(
            content={"detail": "El archivo debe ser de tipo texto plano"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    contenido_byte: bytes = await archivo.read()
    contenido: str = str(contenido_byte.decode("utf-8").rstrip("\n"))
    rsa = RSA()

    def descifrar_chunck(chunk: str):
        return rsa.descifrar(chunk, llave_privada)

    chunks = contenido.split(",")
    with ThreadPoolExecutor() as executor:
        lista_mensajes_descifrados = list(
            executor.map(descifrar_chunck, chunks)
        )
    contenido = "".join(lista_mensajes_descifrados).strip("\n")

    file_name: str = "descifrado"
    file = create_file_txt(
        contenido.encode("utf-8"), f"files{SEPARATOR}{file_name}"
    )
    path: str = os.path.abspath(
        os.path.join(os.getcwd(), "files", f"{file_name}.txt")
    )
    print(f"Path: {path}")

    if not os.path.exists(path):
        return JSONResponse(
            content={"detail": "No se pudo crear el archivo"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return FileResponse(
        media_type="text/plain",
        status_code=status.HTTP_200_OK,
        path=path,
        filename="descifrado.txt",
    )
