from fastapi.testclient import TestClient
from fastapi import status

from main import app

client = TestClient(app)


def test_registrar_alumno_exito():
    payload = {
        "codigo": "2026999",
        "nombres": "Carlos",
        "apellidos": "Mendoza",
        "correo": "carlos@correo.com",
        "carrera": "Sistemas",
    }
    respuesta = client.post("/estudiantes", json=payload)
    assert respuesta.status_code == status.HTTP_201_CREATED
    assert respuesta.json() == {
        "status": "success",
        "detail": "Estudiante registrado exitosamente",
    }


def test_consultar_estudiante_exito():
    respuesta = client.get("/estudiantes/2026999")
    assert respuesta.status_code == status.HTTP_200_OK
    assert respuesta.json()["status"] == "success"
    assert respuesta.json()["data"]["codigo"] == "2026999"


def test_consultar_estudiante_no_encontrado():
    respuesta = client.get("/estudiantes/9999999")
    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Estudiante no encontrado"
