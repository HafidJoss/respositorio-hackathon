import re
from dataclasses import dataclass

from app.modules.triaje.domain.exceptions import SignosVitalesInvalidosError

_PRESION_PATTERN = re.compile(r"^\d{2,3}/\d{2,3}$")


@dataclass(frozen=True, slots=True)
class PresionArterial:
    """Presión arterial en formato sistólica/diastólica, ej. '120/80'."""

    valor: str

    def __post_init__(self) -> None:
        if not _PRESION_PATTERN.fullmatch(self.valor):
            raise SignosVitalesInvalidosError(
                f"Presión arterial inválida: '{self.valor}' — formato esperado NNN/NNN"
            )

    def __str__(self) -> str:
        return self.valor
