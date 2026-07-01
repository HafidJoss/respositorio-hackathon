from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from app.modules.triaje.domain.exceptions import SignosVitalesInvalidosError
from app.modules.triaje.domain.value_objects import PresionArterial


class NivelAtencion(StrEnum):
    CRITICO = "critico"
    MODERADO = "moderado"
    LEVE = "leve"


@dataclass(slots=True)
class Triaje:
    id: UUID
    paciente_id: UUID
    nombres: str
    apellidos: str
    dni: str
    edad: int
    peso: float
    talla: float
    presion_arterial: PresionArterial
    sintomas: list[str]
    nivel_atencion: NivelAtencion
    fecha_registro: datetime

    def __post_init__(self) -> None:
        if self.peso <= 0 or self.talla <= 0:
            raise SignosVitalesInvalidosError("Peso y talla deben ser mayores a 0")

    def requiere_notificacion_medico(self) -> bool:
        return self.nivel_atencion in (NivelAtencion.CRITICO, NivelAtencion.MODERADO)

    @classmethod
    def crear(
        cls, paciente_id: UUID, nombres: str, apellidos: str, dni: str, edad: int,
        peso: float, talla: float, presion_arterial: str, sintomas: list[str],
        nivel_atencion: NivelAtencion,
    ) -> "Triaje":
        return cls(
            uuid4(), paciente_id, nombres, apellidos, dni, edad, peso, talla,
            PresionArterial(presion_arterial), sintomas, nivel_atencion, datetime.now(UTC),
        )
