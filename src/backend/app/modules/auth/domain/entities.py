from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from app.modules.auth.domain.value_objects import Dni


class Rol(StrEnum):
    MEDICO = "medico"
    ENFERMERO = "enfermero"


@dataclass(slots=True)
class Personal:
    id: UUID
    dni: Dni
    nombre: str
    rol: Rol
    password_hash: str
    fecha_registro: datetime

    @classmethod
    def crear(cls, dni: str, nombre: str, rol: Rol, password_hash: str) -> "Personal":
        return cls(
            id=uuid4(),
            dni=Dni(dni),
            nombre=nombre,
            rol=rol,
            password_hash=password_hash,
            fecha_registro=datetime.now(UTC),
        )
