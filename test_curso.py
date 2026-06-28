from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app)


def test_registrar_curso_exito():
    payload = {
        "codigo": "INF-101",
        "nombre": "Introducción a la Informática",
        "creditos": 4,
        "docente": "Ing. Jhimmy G.",
    }
    respuesta = client.post("/cursos", json=payload)

    assert respuesta.status_code == status.HTTP_201_CREATED
    assert respuesta.json() == {
        "status": "success",
        "detail": "Curso registrado exitosamente",
    }


def test_consultar_curso_exito():
    respuesta = client.get("/cursos/1")

    if respuesta.status_code == status.HTTP_200_OK:
        assert respuesta.json()["status"] == "success"
        assert "data" in respuesta.json()
        assert respuesta.json()["data"]["codigo"] == "INF-101"
    else:
        assert respuesta.status_code == status.HTTP_404_NOT_FOUND


def test_consultar_curso_no_encontrado():
    respuesta = client.get("/cursos/9999")

    assert respuesta.status_code == status.HTTP_404_NOT_FOUND
    assert respuesta.json()["detail"] == "Curso no encontrado"


def test_actualizar_curso_exito():
    payload = {
        "codigo": "INF-101",
        "nombre": "Programación Avanzada",
        "creditos": 5,
        "docente": "Ing. Jhimmy G. Modificado",
    }
    respuesta = client.put("/cursos/1", json=payload)
    if respuesta.status_code == status.HTTP_200_OK:
        assert respuesta.json() == {
            "status": "success",
            "detail": "Curso actualizado exitosamente",
        }


def test_consultar_cursos_lista():
    respuesta = client.get("/cursos")

    assert respuesta.status_code == status.HTTP_200_OK
    assert respuesta.json()["status"] == "success"
    assert isinstance(respuesta.json()["data"], list)


def test_eliminar_curso_exito():
    respuesta = client.delete("/cursos/1")

    if respuesta.status_code == status.HTTP_200_OK:
        assert respuesta.json() == {
            "status": "success",
            "detail": "Curso eliminado exitosamente",
        }
