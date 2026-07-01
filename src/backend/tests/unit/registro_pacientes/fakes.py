from uuid import UUID

from app.modules.registro_pacientes.domain.entities import (
    Paciente,
    TipoRelacion,
    Usuario,
    UsuarioPaciente,
)
from app.modules.registro_pacientes.domain.ports import (
    PacienteRepository,
    UsuarioPacienteRepository,
    UsuarioRepository,
)


class FakeUsuarioRepository(UsuarioRepository):
    def __init__(self) -> None:
        self._usuarios: dict[UUID, Usuario] = {}

    def guardar(self, usuario: Usuario) -> Usuario:
        self._usuarios[usuario.id] = usuario
        return usuario

    def buscar_por_id(self, usuario_id: UUID) -> Usuario | None:
        return self._usuarios.get(usuario_id)

    def buscar_por_dni(self, dni: str) -> Usuario | None:
        return next((u for u in self._usuarios.values() if str(u.dni) == dni), None)

    def buscar_por_telefono(self, telefono: str) -> Usuario | None:
        return next((u for u in self._usuarios.values() if str(u.telefono) == telefono), None)


class FakePacienteRepository(PacienteRepository):
    def __init__(self) -> None:
        self._pacientes: dict[UUID, Paciente] = {}

    def guardar(self, paciente: Paciente) -> Paciente:
        self._pacientes[paciente.id] = paciente
        return paciente

    def buscar_por_id(self, paciente_id: UUID) -> Paciente | None:
        return self._pacientes.get(paciente_id)

    def buscar_por_dni(self, dni: str) -> Paciente | None:
        return next((p for p in self._pacientes.values() if str(p.dni) == dni), None)


class FakeUsuarioPacienteRepository(UsuarioPacienteRepository):
    def __init__(self) -> None:
        self._vinculos: list[UsuarioPaciente] = []

    def guardar(self, vinculo: UsuarioPaciente) -> UsuarioPaciente:
        self._vinculos.append(vinculo)
        return vinculo

    def listar_por_usuario(self, usuario_id: UUID) -> list[UsuarioPaciente]:
        return [v for v in self._vinculos if v.usuario_id == usuario_id]

    def existe_vinculo_vigente(
        self, usuario_id: UUID, paciente_id: UUID, tipo_relacion: TipoRelacion
    ) -> bool:
        return any(
            v.usuario_id == usuario_id
            and v.paciente_id == paciente_id
            and v.tipo_relacion == tipo_relacion
            and v.vigente
            for v in self._vinculos
        )
