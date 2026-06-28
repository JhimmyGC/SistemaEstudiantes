from fastapi import FastAPI
from src.router.estudiante import router as alumnos_router
from src.router.curso import router as cursos_router

app = FastAPI()
app.include_router(alumnos_router)
app.include_router(cursos_router)


@app.get("/")
def main():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
