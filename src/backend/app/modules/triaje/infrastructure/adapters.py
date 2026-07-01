import logging
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.registro_pacientes.infrastructure.repositories import (
    SqlAlchemyPacienteRepository,
)
from app.modules.triaje.domain.entities import Triaje
from app.modules.triaje.domain.ports import NotificacionPort, PacienteLookupPort

logger = logging.getLogger(__name__)


class PacienteLookupAdapter(PacienteLookupPort):
    """Adaptador sobre la capacidad de `registro-pacientes` — solo la
    infraestructura de triaje conoce este import, nunca su dominio."""

    def __init__(self, db: Session) -> None:
        self._paciente_repo = SqlAlchemyPacienteRepository(db)

    def existe_paciente(self, paciente_id: UUID) -> bool:
        return self._paciente_repo.buscar_por_id(paciente_id) is not None


class NotificacionAdapterPendiente(NotificacionPort):
    """Adaptador provisional: el módulo `notificaciones` aún no tiene
    fase-0 congelada (ledger-dependencias.md DEP-004). Este adaptador
    solo deja evidencia en el log — no bloquea ni revierte el triaje."""

    def notificar_triaje_urgente(self, triaje: Triaje) -> None:
        logger.info(
            "Notificación pendiente de adaptador real: triaje %s (%s) requiere atención médica",
            triaje.id,
            triaje.nivel_atencion,
        )
