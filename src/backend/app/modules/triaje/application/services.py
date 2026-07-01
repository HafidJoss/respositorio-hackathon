import logging
from uuid import UUID

from app.modules.triaje.application.dtos import RegistrarTriajeCommand
from app.modules.triaje.domain.entities import NivelAtencion, Triaje
from app.modules.triaje.domain.exceptions import (
    NivelAtencionInvalidoError,
    PacienteNoExisteError,
    TriajeNoEncontradoError,
)
from app.modules.triaje.domain.ports import (
    CatalogoSintomasRepository,
    NotificacionPort,
    PacienteLookupPort,
    TriajeRepository,
)

logger = logging.getLogger(__name__)


def _parsear_nivel_atencion(valor: str) -> NivelAtencion:
    if not valor:
        raise NivelAtencionInvalidoError("nivel_atencion no puede quedar vacío")
    try:
        return NivelAtencion(valor)
    except ValueError as error:
        raise NivelAtencionInvalidoError(f"nivel_atencion inválido: '{valor}'") from error


def _construir_triaje(cmd: RegistrarTriajeCommand, nivel: NivelAtencion) -> Triaje:
    return Triaje.crear(
        cmd.paciente_id, cmd.nombres, cmd.apellidos, cmd.dni, cmd.edad, cmd.peso,
        cmd.talla, cmd.presion_arterial, cmd.sintomas, nivel,
    )


class RegistrarTriajeService:
    def __init__(
        self,
        triaje_repo: TriajeRepository,
        paciente_lookup: PacienteLookupPort,
        notificacion: NotificacionPort,
    ) -> None:
        self._triaje_repo = triaje_repo
        self._paciente_lookup = paciente_lookup
        self._notificacion = notificacion

    def ejecutar(self, cmd: RegistrarTriajeCommand) -> Triaje:
        if not self._paciente_lookup.existe_paciente(cmd.paciente_id):
            raise PacienteNoExisteError(
                f"Paciente {cmd.paciente_id} no existe — regístrelo en registro-pacientes"
            )
        nivel = _parsear_nivel_atencion(cmd.nivel_atencion)
        triaje = self._triaje_repo.guardar(_construir_triaje(cmd, nivel))
        self._notificar_si_corresponde(triaje)
        return triaje

    def _notificar_si_corresponde(self, triaje: Triaje) -> None:
        if not triaje.requiere_notificacion_medico():
            return
        try:
            self._notificacion.notificar_triaje_urgente(triaje)
        except Exception:
            logger.exception(
                "Fallo notificando triaje urgente %s — el triaje ya quedó guardado", triaje.id
            )


class ObtenerTriajeService:
    def __init__(self, triaje_repo: TriajeRepository) -> None:
        self._triaje_repo = triaje_repo

    def ejecutar(self, triaje_id: UUID) -> Triaje:
        triaje = self._triaje_repo.buscar_por_id(triaje_id)
        if triaje is None:
            raise TriajeNoEncontradoError(f"Triaje {triaje_id} no encontrado")
        return triaje


class ListarTriajesDePacienteService:
    def __init__(self, triaje_repo: TriajeRepository, paciente_lookup: PacienteLookupPort) -> None:
        self._triaje_repo = triaje_repo
        self._paciente_lookup = paciente_lookup

    def ejecutar(self, paciente_id: UUID) -> list[Triaje]:
        if not self._paciente_lookup.existe_paciente(paciente_id):
            raise PacienteNoExisteError(f"Paciente {paciente_id} no existe")
        return self._triaje_repo.listar_por_paciente(paciente_id)


class ListarCatalogoSintomasService:
    def __init__(self, catalogo_repo: CatalogoSintomasRepository) -> None:
        self._catalogo_repo = catalogo_repo

    def ejecutar(self) -> list[str]:
        return self._catalogo_repo.listar()
