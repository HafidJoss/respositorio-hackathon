from dataclasses import dataclass
from uuid import UUID

from app.modules.registro_pacientes.domain.entities import Paciente, UsuarioPaciente


@dataclass(slots=True)
class RegistrarUsuarioCommand:
    dni: str
    telefono: str


@dataclass(slots=True)
class RegistrarPacienteCommand:
    dni: str
    nombres: str
    apellidos: str
    edad: int
    jurisdiccion_sis: str
    usuario_id: UUID
    tipo_relacion: str


@dataclass(slots=True)
class VincularUsuarioPacienteCommand:
    usuario_id: UUID
    paciente_id: UUID
    tipo_relacion: str


@dataclass(slots=True)
class ResultadoRegistroPaciente:
    paciente: Paciente
    creado: bool
    vinculo: UsuarioPaciente
