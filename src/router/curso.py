from fastapi import APIRouter
from src.models.curso import Curso
from src.db.dbconect import DB
from sqlalchemy import text
from fastapi import HTTPException, status

router = APIRouter(tags=["Cursos"])


@router.post("/cursos", status_code=status.HTTP_201_CREATED)
def registrar_curso(curso: Curso):
    db = DB.conectar()
    try:
        datos_curso = curso.dict()

        db.execute(
            text("""INSERT INTO cursos (codigo, nombre, creditos, docente) 
                   VALUES (:codigo, :nombre, :creditos, :docente)"""),
            datos_curso,
        )
        db.commit()

        return {"status": "success", "detail": "Curso registrado exitosamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo registrar el curso: {str(e)}",
        )

    finally:
        db.close()


from fastapi import HTTPException, status
from sqlalchemy import text


@router.get("/cursos/{id}", status_code=status.HTTP_200_OK)
def consultar_curso(id: int):
    db = DB.conectar()
    try:
        resultado = db.execute(
            text(
                "SELECT id, codigo, nombre, creditos, docente FROM cursos WHERE id = :id"
            ),
            {"id": id},
        ).fetchone()

        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Curso no encontrado"
            )

        datos_curso = dict(resultado._mapping)
        return {"status": "success", "data": datos_curso}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo obtener el curso: {str(e)}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado al obtener el curso",
        )
    finally:
        db.close()


@router.put("/cursos/{id}", status_code=status.HTTP_200_OK)
def actualizar_curso(id: int, curso: Curso):
    db = DB.conectar()
    try:
        datos_curso = curso.dict()

        db.execute(
            text(
                "UPDATE cursos SET codigo = :codigo, nombre = :nombre, creditos = :creditos, docente = :docente WHERE id = :id"
            ),
            {**datos_curso, "id": id},
        )
        db.commit()

        return {"status": "success", "detail": "Curso actualizado exitosamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo actualizar el curso: {str(e)}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado al actualizar el curso",
        )
    finally:
        db.close()


@router.delete("/cursos/{id}", status_code=status.HTTP_200_OK)
def eliminar_curso(id: int):
    db = DB.conectar()
    try:
        db.execute(
            text("DELETE FROM cursos WHERE id = :id"),
            {"id": id},
        )
        db.commit()

        return {"status": "success", "detail": "Curso eliminado exitosamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudo eliminar el curso: {str(e)}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado al eliminar el curso",
        )
    finally:
        db.close()


@router.get("/cursos", status_code=status.HTTP_200_OK)
def consultar_cursos():
    db = DB.conectar()
    try:
        resultado = db.execute(
            text("SELECT * FROM cursos"),
            {},
        ).fetchall()

        datos_cursos = [dict(row._mapping) for row in resultado]
        return {"status": "success", "data": datos_cursos}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se pudieron obtener los cursos: {str(e)}",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocurrió un error inesperado al obtener los cursos",
        )
    finally:
        db.close()
