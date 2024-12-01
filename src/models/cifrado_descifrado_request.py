from typing import List

from pydantic import BaseModel


class CifrarRequest(BaseModel):
    mensaje: str
    llave_publica: List[int]


class DescifrarRequest(BaseModel):
    mensaje: str
    llave_privada: List[int]
