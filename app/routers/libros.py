from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Libro, LibroCreate, LibroUpdate

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.post("/", response_model=Libro)
def crear_libro(libro: LibroCreate, db: Session = Depends(get_session)):
    db_libro = Libro.model_validate(libro)
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

@router.get("/", response_model=List[Libro])
def listar_libros(db: Session = Depends(get_session)):
    return db.exec(select(Libro)).all()

@router.get("/{libro_id}", response_model=Libro)
def obtener_libro(libro_id: int, db: Session = Depends(get_session)):
    libro = db.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.put("/{libro_id}", response_model=Libro)
def actualizar_libro(libro_id: int, libro_data: LibroUpdate, db: Session = Depends(get_session)):
    db_libro = db.get(Libro, libro_id)
    if not db_libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    data = libro_data.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_libro, key, value)
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

@router.delete("/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(get_session)):
    libro = db.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db.delete(libro)
    db.commit()
    return {"mensaje": f"Libro {libro_id} eliminado exitosamente"}