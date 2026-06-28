from pydantic import BaseModel


class Estudiante(BaseModel):
    codigo: str
    nombres: str
    apellidos: str
    correo: str
    carrera: str
