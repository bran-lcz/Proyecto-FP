from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Modelos SQLAlchemy para la base de datos
class ProductoDB(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    caracteristicas = Column(String(255))
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    categoria = Column(String(50))
    imagen = Column(String(255))
    fecha_creacion = Column(DateTime, default=func.now())

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    fecha_creacion = Column(DateTime, default=func.now())

# Modelos Pydantic para la API
class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    caracteristicas: str
    precio: float
    stock: int
    categoria: str
    imagen: str

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
    fecha_creacion: str

    class Config:
        orm_mode = True

class UsuarioBase(BaseModel):
    nombre: str
    username: str
    role: str  # Roles permitidos: 'administrador', 'vendedor', 'bodeguero'

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    fecha_creacion: str

    class Config:
        orm_mode = True

class UsuarioLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    id: int
    nombre: str
    username: str
    role: str