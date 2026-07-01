from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.triaje.domain.entities import Triaje


class TriajeRepository(ABC):
    @abstractmethod
    def guardar(self, triaje: Triaje) -> Triaje: ...

    @abstractmethod
    def buscar_por_id(self, triaje_id: UUID) -> Triaje | None: ...

    @abstractmethod
    def listar_por_paciente(self, paciente_id: UUID) -> list[Triaje]: ...


class CatalogoSintomasRepository(ABC):
    @abstractmethod
    def listar(self) -> list[str]: ...


class PacienteLookupPort(ABC):
    """Puerto hacia la capacidad de `registro-pacientes` — el dominio de
    triaje nunca importa infraestructura de otro módulo (00-arquitectura-y-calidad.md §1)."""

    @abstractmethod
    def existe_paciente(self, paciente_id: UUID) -> bool: ...


class NotificacionPort(ABC):
    """Puerto de notificación referenciado por el MUST de triaje.
    Adaptador real pendiente del módulo `notificaciones` (ver ledger DEP-004)."""

    @abstractmethod
    def notificar_triaje_urgente(self, triaje: Triaje) -> None: ...
