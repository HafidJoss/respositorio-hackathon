from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.registro_pacientes.domain.entities import (
    Paciente,
    TipoRelacion,
    Usuario,
    UsuarioPaciente,
)


class UsuarioRepository(ABC):
    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario: ...

    @abstractmethod
    def buscar_por_id(self, usuario_id: UUID) -> Usuario | None: ...

    @abstractmethod
    def buscar_por_dni(self, dni: str) -> Usuario | None: ...

    @abstractmethod
    def buscar_por_telefono(self, telefono: str) -> Usuario | None: ...


class PacienteRepository(ABC):
    @abstractmethod
    def guardar(self, paciente: Paciente) -> Paciente: ...

    @abstractmethod
    def buscar_por_id(self, paciente_id: UUID) -> Paciente | None: ...

    @abstractmethod
    def buscar_por_dni(self, dni: str) -> Paciente | None: ...


class UsuarioPacienteRepository(ABC):
    @abstractmethod
    def guardar(self, vinculo: UsuarioPaciente) -> UsuarioPaciente: ...

    @abstractmethod
    def listar_por_usuario(self, usuario_id: UUID) -> list[UsuarioPaciente]: ...

    @abstractmethod
    def existe_vinculo_vigente(
        self, usuario_id: UUID, paciente_id: UUID, tipo_relacion: TipoRelacion
    ) -> bool: ...
