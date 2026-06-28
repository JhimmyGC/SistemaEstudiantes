from fastapi import APIRouter
from src.models.estudiante import Estudiante
from src.db.dbconect import DB
from sqlalchemy import text
from fastapi import HTTPException, status

router = APIRouter(tags=["Estudiantes"])


@router.post("/estudiantes", status_code=status.HTTP_201_CREATED)
def registrar_alumno(estudiante: Estudiante):
    db = DB.conectar()
    try:
        datos_estudiante = estudiante.dict()

        db.execute(
            text(
                """INSERT INTO estudiantes (codigo, nombres, apellidos, correo, carrera) 
                   VALUES (:codigo, :nombres, :apellidos, :correo, :carrera)"""
            ),
            datos_estudiante,
        )
        db.commit()

        return {"status": "success", "detail": "Estudiante registrado exitosamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo registrar al estudiante: {str(e)}",
        )

    finally:
        db.close()


from fastapi import HTTPException, status
from sqlalchemy import text


@router.get("/estudiantes/{id}", status_code=status.HTTP_200_OK)
def consultar_estudiante(id: int):
    db = DB.conectar()
    try:
        resultado = db.execute(
            text(
                "SELECT id, codigo, nombres, apellidos, correo, carrera FROM estudiantes WHERE id = :id"
            ),
            {"id": id},
        ).fetchone()

        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado"
            )

        datos_estudiante = dict(resultado._mapping)
        return {"status": "success", "data": datos_estudiante}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo obtener al estudiante: {str(e)}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado al obtener al estudiante",
        )
    finally:
        db.close()


@router.put("/estudiantes/{id}", status_code=status.HTTP_200_OK)
def actualizar_estudiante(id: int, estudiante: Estudiante):
    db = DB.conectar()
    try:
        datos_estudiante = estudiante.dict()

        db.execute(
            text(
                "UPDATE estudiantes SET codigo = :codigo, nombres = :nombres, apellidos = :apellidos, correo = :correo, carrera = :carrera WHERE id = :id"
            ),
            {**datos_estudiante, "id": id},
        )
        db.commit()

        return {"status": "success", "detail": "Estudiante actualizado exitosamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo actualizar al estudiante: {str(e)}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado al actualizar al estudiante",
        )
    finally:
        db.close()


@router.delete("/estudiantes/{id}", status_code=status.HTTP_200_OK)
def eliminar_estudiante(id: int):
    db = DB.conectar()
    try:
        db.execute(
            text("DELETE FROM estudiantes WHERE id = :id"),
            {"id": id},
        )
        db.commit()

        return {"status": "success", "detail": "Estudiante eliminado exitosamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo eliminar al estudiante: {str(e)}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado al eliminar al estudiante",
        )
    finally:
        db.close()


@router.get("/estudiantes", status_code=status.HTTP_200_OK)
def consultar_estudiantes():
    db = DB.conectar()
    try:
        resultado = db.execute(
            text("SELECT * FROM estudiantes"),
            {},
        ).fetchall()

        datos_estudiantes = [dict(row._mapping) for row in resultado]
        return {"status": "success", "data": datos_estudiantes}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudieron obtener los estudiantes: {str(e)}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado al obtener los estudiantes",
        )
    finally:
        db.close()
