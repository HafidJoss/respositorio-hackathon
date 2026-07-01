from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TriajeCreate(BaseModel):
    paciente_id: UUID
    nombres: str
    apellidos: str
    dni: str
    edad: int
    peso: float
    talla: float
    presion_arterial: str
    sintomas: list[str]
    nivel_atencion: str


class TriajeResponse(BaseModel):
    id: UUID
    paciente_id: UUID
    nombres: str
    apellidos: str
    dni: str
    edad: int
    peso: float
    talla: float
    presion_arterial: str
    sintomas: list[str]
    nivel_atencion: str
    fecha_registro: datetime
