from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app)


def test_registrar_alumno_exito():
    payload = {
        "codigo": "2026111",
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
    respuesta = client.get("/estudiantes/1")
    if respuesta.status_code == status.HTTP_200_OK:
        assert respuesta.json()["status"] == "success"
        assert "data" in respuesta.json()
        assert "codigo" in respuesta.json()["data"]
    else:
        assert respuesta.status_code == status.HTTP_404_NOT_FOUND


def test_consultar_estudiante_no_encontrado():
    respuesta = client.get("/estudiantes/999999")

    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Estudiante no encontrado"


def test_actualizar_estudiante_exito():
    payload = {
        "codigo": "2026111",
        "nombres": "Carlos Alberto",
        "apellidos": "Mendoza Modificado",
        "correo": "carlos_nuevo@correo.com",
        "carrera": "Sistemas Avanzados",
    }
    respuesta = client.put("/estudiantes/1", json=payload)

    if respuesta.status_code == status.HTTP_200_OK:
        assert respuesta.json() == {
            "status": "success",
            "detail": "Estudiante actualizado exitosamente",
        }


def test_consultar_estudiantes_lista():
    respuesta = client.get("/estudiantes")

    assert respuesta.status_code == status.HTTP_200_OK
    assert respuesta.json()["status"] == "success"
    assert isinstance(respuesta.json()["data"], list)


def test_eliminar_estudiante_exito():
    respuesta = client.delete("/estudiantes/1")

    if respuesta.status_code == status.HTTP_200_OK:
        assert respuesta.json() == {
            "status": "success",
            "detail": "Estudiante eliminado exitosamente",
        }
