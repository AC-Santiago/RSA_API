from pydantic import BaseModel
from typing import List


class Usuario(BaseModel):
    nombre: str
    correo: str
    contraseña: str

