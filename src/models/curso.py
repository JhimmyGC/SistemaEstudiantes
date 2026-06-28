from pydantic import BaseModel


class Curso(BaseModel):
    codigo: str
    nombre: str
    creditos: int
    docente: str
