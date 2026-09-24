from fastapi import FastAPI
from app.database import init_db
from app.routers import usuarios, libros

init_db()

app = FastAPI(
    title="API de Gestión de Libros y Usuarios",
    description="API RESTful desplegada en EC2 con persistencia en Amazon RDS",
    version="1.0.0"
)

app.include_router(usuarios.router)
app.include_router(libros.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API ejecutándose correctamente"}