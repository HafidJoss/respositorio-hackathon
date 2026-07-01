import re
from dataclasses import dataclass

from app.modules.registro_pacientes.domain.exceptions import (
    DniInvalidoError,
    TelefonoInvalidoError,
)

_DNI_PATTERN = re.compile(r"^\d{8}$")
_TELEFONO_PATTERN = re.compile(r"^\+51 9\d{8}$")


@dataclass(frozen=True, slots=True)
class Dni:
    """DNI peruano: exactamente 8 dígitos numéricos (§4.1)."""

    valor: str

    def __post_init__(self) -> None:
        if not _DNI_PATTERN.fullmatch(self.valor):
            raise DniInvalidoError(
                f"DNI inválido: '{self.valor}' — debe ser exactamente 8 dígitos"
            )

    def __str__(self) -> str:
        return self.valor


@dataclass(frozen=True, slots=True)
class Telefono:
    """Teléfono oficial: formato +51 9XXXXXXXX (§4.1)."""

    valor: str

    def __post_init__(self) -> None:
        if not _TELEFONO_PATTERN.fullmatch(self.valor):
            raise TelefonoInvalidoError(
                f"Teléfono inválido: '{self.valor}' — formato esperado +51 9XXXXXXXX"
            )

    def __str__(self) -> str:
        return self.valor
