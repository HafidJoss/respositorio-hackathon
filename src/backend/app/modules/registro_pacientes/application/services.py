from uuid import UUID

from app.modules.registro_pacientes.application.dtos import (
    RegistrarPacienteCommand,
    RegistrarUsuarioCommand,
    ResultadoRegistroPaciente,
    VincularUsuarioPacienteCommand,
)
from app.modules.registro_pacientes.domain.entities import (
    Paciente,
    TipoRelacion,
    Usuario,
    UsuarioPaciente,
)
from app.modules.registro_pacientes.domain.exceptions import (
    TipoRelacionInvalidaError,
    UsuarioDuplicadoError,
    UsuarioNoEncontradoError,
    VinculoDuplicadoError,
)
from app.modules.registro_pacientes.domain.ports import (
    PacienteRepository,
    UsuarioPacienteRepository,
    UsuarioRepository,
)


def _parsear_tipo_relacion(valor: str) -> TipoRelacion:
    try:
        return TipoRelacion(valor)
    except ValueError as error:
        raise TipoRelacionInvalidaError(f"tipo_relacion inválido: '{valor}'") from error


class RegistrarUsuarioService:
    def __init__(self, usuario_repo: UsuarioRepository) -> None:
        self._usuario_repo = usuario_repo

    def ejecutar(self, cmd: RegistrarUsuarioCommand) -> Usuario:
        if self._usuario_repo.buscar_por_dni(cmd.dni) is not None:
            raise UsuarioDuplicadoError(f"Ya existe un Usuario con DNI {cmd.dni}")
        if self._usuario_repo.buscar_por_telefono(cmd.telefono) is not None:
            raise UsuarioDuplicadoError(
                f"Ya existe un Usuario con teléfono {cmd.telefono}"
            )
        usuario = Usuario.crear(dni=cmd.dni, telefono=cmd.telefono)
        return self._usuario_repo.guardar(usuario)


class ObtenerUsuarioService:
    def __init__(self, usuario_repo: UsuarioRepository) -> None:
        self._usuario_repo = usuario_repo

    def ejecutar(self, usuario_id: UUID) -> Usuario:
        usuario = self._usuario_repo.buscar_por_id(usuario_id)
        if usuario is None:
            raise UsuarioNoEncontradoError(f"Usuario {usuario_id} no encontrado")
        return usuario


class BuscarPacientePorDniService:
    """Capacidad reutilizada por `triaje` y `bot-ivr-urgencias` (fase-0 §MUST)."""

    def __init__(self, paciente_repo: PacienteRepository) -> None:
        self._paciente_repo = paciente_repo

    def ejecutar(self, dni: str) -> Paciente | None:
        return self._paciente_repo.buscar_por_dni(dni)


class VincularUsuarioPacienteService:
    def __init__(
        self,
        usuario_repo: UsuarioRepository,
        paciente_repo: PacienteRepository,
        vinculo_repo: UsuarioPacienteRepository,
    ) -> None:
        self._usuario_repo = usuario_repo
        self._paciente_repo = paciente_repo
        self._vinculo_repo = vinculo_repo

    def ejecutar(self, cmd: VincularUsuarioPacienteCommand) -> UsuarioPaciente:
        if self._usuario_repo.buscar_por_id(cmd.usuario_id) is None:
            raise UsuarioNoEncontradoError(f"Usuario {cmd.usuario_id} no encontrado")
        if self._paciente_repo.buscar_por_id(cmd.paciente_id) is None:
            raise UsuarioNoEncontradoError(f"Paciente {cmd.paciente_id} no encontrado")
        tipo_relacion = _parsear_tipo_relacion(cmd.tipo_relacion)
        self._asegurar_vinculo_no_duplicado(cmd.usuario_id, cmd.paciente_id, tipo_relacion)
        vinculo = UsuarioPaciente.crear(cmd.usuario_id, cmd.paciente_id, tipo_relacion)
        return self._vinculo_repo.guardar(vinculo)

    def _asegurar_vinculo_no_duplicado(
        self, usuario_id: UUID, paciente_id: UUID, tipo_relacion: TipoRelacion
    ) -> None:
        if self._vinculo_repo.existe_vinculo_vigente(usuario_id, paciente_id, tipo_relacion):
            raise VinculoDuplicadoError(
                "Ya existe un vínculo vigente con ese tipo_relacion entre "
                f"usuario {usuario_id} y paciente {paciente_id}"
            )


class ListarPacientesDeUsuarioService:
    def __init__(self, usuario_repo: UsuarioRepository, vinculo_repo: UsuarioPacienteRepository) -> None:
        self._usuario_repo = usuario_repo
        self._vinculo_repo = vinculo_repo

    def ejecutar(self, usuario_id: UUID) -> list[UsuarioPaciente]:
        if self._usuario_repo.buscar_por_id(usuario_id) is None:
            raise UsuarioNoEncontradoError(f"Usuario {usuario_id} no encontrado")
        return self._vinculo_repo.listar_por_usuario(usuario_id)


class RegistrarPacienteService:
    """Regla de negocio central: DNI de Paciente duplicado -> ofrecer vínculo,
    nunca duplicar silenciosamente (00-arquitectura-y-calidad.md, MUST fase-0)."""

    def __init__(
        self,
        paciente_repo: PacienteRepository,
        usuario_repo: UsuarioRepository,
        vinculo_repo: UsuarioPacienteRepository,
    ) -> None:
        self._paciente_repo = paciente_repo
        self._usuario_repo = usuario_repo
        self._vinculo_repo = vinculo_repo

    def ejecutar(self, cmd: RegistrarPacienteCommand) -> ResultadoRegistroPaciente:
        if self._usuario_repo.buscar_por_id(cmd.usuario_id) is None:
            raise UsuarioNoEncontradoError(f"Usuario {cmd.usuario_id} no encontrado")
        tipo_relacion = _parsear_tipo_relacion(cmd.tipo_relacion)
        existente = self._paciente_repo.buscar_por_dni(cmd.dni)
        if existente is not None:
            return self._vincular_a_existente(existente, cmd.usuario_id, tipo_relacion)
        return self._crear_y_vincular(cmd, tipo_relacion)

    def _vincular_a_existente(
        self, paciente: Paciente, usuario_id: UUID, tipo_relacion: TipoRelacion
    ) -> ResultadoRegistroPaciente:
        if self._vinculo_repo.existe_vinculo_vigente(usuario_id, paciente.id, tipo_relacion):
            raise VinculoDuplicadoError(
                f"El paciente con DNI {paciente.dni} ya está vinculado a este usuario"
            )
        vinculo = UsuarioPaciente.crear(usuario_id, paciente.id, tipo_relacion)
        vinculo = self._vinculo_repo.guardar(vinculo)
        return ResultadoRegistroPaciente(paciente=paciente, creado=False, vinculo=vinculo)

    def _crear_y_vincular(
        self, cmd: RegistrarPacienteCommand, tipo_relacion: TipoRelacion
    ) -> ResultadoRegistroPaciente:
        paciente = Paciente.crear(
            dni=cmd.dni,
            nombres=cmd.nombres,
            apellidos=cmd.apellidos,
            edad=cmd.edad,
            jurisdiccion_sis=cmd.jurisdiccion_sis,
        )
        paciente = self._paciente_repo.guardar(paciente)
        vinculo = UsuarioPaciente.crear(cmd.usuario_id, paciente.id, tipo_relacion)
        vinculo = self._vinculo_repo.guardar(vinculo)
        return ResultadoRegistroPaciente(paciente=paciente, creado=True, vinculo=vinculo)
