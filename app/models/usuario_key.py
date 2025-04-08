from typing import List

from pydantic import BaseModel


class UsuarioKey(BaseModel):
    nombre_llaves: str
    llave_publica: List[int]
    llave_privada: List[int]
