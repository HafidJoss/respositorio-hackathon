import re
from dataclasses import dataclass

from app.modules.auth.domain.exceptions import DniInvalidoError, PasswordInvalidaError

_DNI_PATTERN = re.compile(r"^\d{8}$")
_PASSWORD_LONGITUD_MINIMA = 6


@dataclass(frozen=True, slots=True)
class Dni:
    """DNI peruano: exactamente 8 dígitos numéricos (mismo formato que registro-pacientes)."""

    valor: str

    def __post_init__(self) -> None:
        if not _DNI_PATTERN.fullmatch(self.valor):
            raise DniInvalidoError(
                f"DNI inválido: '{self.valor}' — debe ser exactamente 8 dígitos"
            )

    def __str__(self) -> str:
        return self.valor


@dataclass(frozen=True, slots=True)
class Password:
    """Password en texto plano, validado antes de hashear. Nunca se persiste así."""

    valor: str

    def __post_init__(self) -> None:
        if len(self.valor) < _PASSWORD_LONGITUD_MINIMA:
            raise PasswordInvalidaError(
                f"La contraseña debe tener al menos {_PASSWORD_LONGITUD_MINIMA} caracteres"
            )
