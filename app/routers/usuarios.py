from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Usuario, UsuarioCreate, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=Usuario)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_session)):
    db_usuario = Usuario.model_validate(usuario)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/", response_model=List[Usuario])
def listar_usuarios(db: Session = Depends(get_session)):
    return db.exec(select(Usuario)).all()

@router.get("/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_session)):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{usuario_id}", response_model=Usuario)
def actualizar_usuario(usuario_id: int, usuario_data: UsuarioUpdate, db: Session = Depends(get_session)):
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    data = usuario_data.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_usuario, key, value)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_session)):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"mensaje": f"Usuario {usuario_id} eliminado exitosamente"}