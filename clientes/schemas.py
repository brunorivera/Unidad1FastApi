# app/modules/clientes/schemas.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, example="Ana García")
    email: EmailStr = Field(..., example="ana@ejemplo.com")
    telefono: str = Field(..., pattern=r"^\+?\d{7,15}$", example="+5491112345678")
    activo: bool = True


class ClienteCreate(ClienteBase):
    pass  # Exige todos los campos de Base


class ClienteUpdate(BaseModel):
    # Para PATCH (actualización parcial), todos opcionales
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, pattern=r"^\+?\d{7,15}$")
    activo: Optional[bool] = None


class ClienteRead(ClienteBase):
    id: int  # El ID siempre se devuelve al leer