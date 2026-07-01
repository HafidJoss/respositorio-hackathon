from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UsuarioCreate(BaseModel):
    dni: str
    telefono: str


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    dni: str
    telefono: str
    fecha_registro: datetime


class PacienteCreate(BaseModel):
    dni: str
    nombres: str
    apellidos: str
    edad: int
    jurisdiccion_sis: str
    usuario_id: UUID
    tipo_relacion: str


class PacienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    dni: str
    nombres: str
    apellidos: str
    edad: int
    jurisdiccion_sis: str
    fecha_registro: datetime


class PacienteRegistroResponse(PacienteResponse):
    ya_existia: bool


class VinculoCreate(BaseModel):
    paciente_id: UUID
    tipo_relacion: str


class VinculoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    usuario_id: UUID
    paciente_id: UUID
    tipo_relacion: str
    vigente: bool
    fecha_vinculacion: datetime
