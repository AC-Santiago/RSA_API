from pydantic import BaseModel
from typing import List


class CifrarRequest(BaseModel):
    mensaje: str
    llave_publica: List[int]


class DescifrarRequest(BaseModel):
    mensaje: str
    llaves: List[int]
