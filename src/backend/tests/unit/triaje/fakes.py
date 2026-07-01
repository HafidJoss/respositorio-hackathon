from uuid import UUID

from app.modules.triaje.domain.entities import Triaje
from app.modules.triaje.domain.ports import (
    CatalogoSintomasRepository,
    NotificacionPort,
    PacienteLookupPort,
    TriajeRepository,
)


class FakeTriajeRepository(TriajeRepository):
    def __init__(self) -> None:
        self._triajes: dict[UUID, Triaje] = {}

    def guardar(self, triaje: Triaje) -> Triaje:
        self._triajes[triaje.id] = triaje
        return triaje

    def buscar_por_id(self, triaje_id: UUID) -> Triaje | None:
        return self._triajes.get(triaje_id)

    def listar_por_paciente(self, paciente_id: UUID) -> list[Triaje]:
        return [t for t in self._triajes.values() if t.paciente_id == paciente_id]


class FakePacienteLookupPort(PacienteLookupPort):
    def __init__(self, pacientes_existentes: set[UUID] | None = None) -> None:
        self._pacientes_existentes = pacientes_existentes or set()

    def existe_paciente(self, paciente_id: UUID) -> bool:
        return paciente_id in self._pacientes_existentes


class FakeNotificacionPort(NotificacionPort):
    def __init__(self, falla: bool = False) -> None:
        self.falla = falla
        self.notificaciones_enviadas: list[Triaje] = []

    def notificar_triaje_urgente(self, triaje: Triaje) -> None:
        if self.falla:
            raise RuntimeError("fallo simulado de canal de notificación")
        self.notificaciones_enviadas.append(triaje)


class FakeCatalogoSintomasRepository(CatalogoSintomasRepository):
    def __init__(self, sintomas: list[str] | None = None) -> None:
        self._sintomas = sintomas or []

    def listar(self) -> list[str]:
        return self._sintomas
