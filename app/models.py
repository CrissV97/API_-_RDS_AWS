from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class UsuarioBase(SQLModel):
    nombre: str
    email: str

class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    libros: List["Libro"] = Relationship(back_populates="usuario")

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(SQLModel):
    nombre: Optional[str] = None
    email: Optional[str] = None

class LibroBase(SQLModel):
    titulo: str
    autor: str
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

class Libro(LibroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario: Optional[Usuario] = Relationship(back_populates="libros")

class LibroCreate(LibroBase):
    pass

class LibroUpdate(SQLModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    usuario_id: Optional[int] = None