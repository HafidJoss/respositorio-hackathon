from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PersonalCreate(BaseModel):
    dni: str
    nombre: str
    password: str
    rol: str


class PersonalLogin(BaseModel):
    dni: str
    password: str


class PersonalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    dni: str
    nombre: str
    rol: str
    fecha_registro: datetime
