from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from app.modules.registro_pacientes.domain.exceptions import EdadInvalidaError
from app.modules.registro_pacientes.domain.value_objects import Dni, Telefono


class TipoRelacion(StrEnum):
    TITULAR = "titular"
    MADRE = "madre"
    PADRE = "padre"
    TUTOR_LEGAL = "tutor_legal"
    OTRO = "otro"


@dataclass(slots=True)
class Usuario:
    id: UUID
    dni: Dni
    telefono: Telefono
    fecha_registro: datetime

    @classmethod
    def crear(cls, dni: str, telefono: str) -> "Usuario":
        return cls(
            id=uuid4(),
            dni=Dni(dni),
            telefono=Telefono(telefono),
            fecha_registro=datetime.now(UTC),
        )


@dataclass(slots=True)
class Paciente:
    id: UUID
    dni: Dni
    nombres: str
    apellidos: str
    edad: int
    jurisdiccion_sis: str
    fecha_registro: datetime

    def __post_init__(self) -> None:
        if self.edad < 0 or self.edad > 130:
            raise EdadInvalidaError(f"Edad inválida: {self.edad}")

    @classmethod
    def crear(
        cls, dni: str, nombres: str, apellidos: str, edad: int, jurisdiccion_sis: str
    ) -> "Paciente":
        return cls(
            id=uuid4(),
            dni=Dni(dni),
            nombres=nombres,
            apellidos=apellidos,
            edad=edad,
            jurisdiccion_sis=jurisdiccion_sis,
            fecha_registro=datetime.now(UTC),
        )


@dataclass(slots=True)
class UsuarioPaciente:
    id: UUID
    usuario_id: UUID
    paciente_id: UUID
    tipo_relacion: TipoRelacion
    fecha_vinculacion: datetime
    vigente: bool = field(default=True)

    @classmethod
    def crear(
        cls, usuario_id: UUID, paciente_id: UUID, tipo_relacion: TipoRelacion
    ) -> "UsuarioPaciente":
        return cls(
            id=uuid4(),
            usuario_id=usuario_id,
            paciente_id=paciente_id,
            tipo_relacion=tipo_relacion,
            fecha_vinculacion=datetime.now(UTC),
            vigente=True,
        )
