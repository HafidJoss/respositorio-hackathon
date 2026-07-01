from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

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
from app.modules.registro_pacientes.infrastructure import mappers
from app.modules.registro_pacientes.infrastructure.orm_models import (
    PacienteModel,
    UsuarioModel,
    UsuarioPacienteModel,
)


class SqlAlchemyUsuarioRepository(UsuarioRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def guardar(self, usuario: Usuario) -> Usuario:
        modelo = mappers.usuario_a_modelo(usuario)
        self._db.add(modelo)
        self._db.flush()
        return mappers.usuario_a_dominio(modelo)

    def buscar_por_id(self, usuario_id: UUID) -> Usuario | None:
        modelo = self._db.get(UsuarioModel, usuario_id)
        return mappers.usuario_a_dominio(modelo) if modelo else None

    def buscar_por_dni(self, dni: str) -> Usuario | None:
        stmt = select(UsuarioModel).where(UsuarioModel.dni == dni)
        modelo = self._db.scalars(stmt).first()
        return mappers.usuario_a_dominio(modelo) if modelo else None

    def buscar_por_telefono(self, telefono: str) -> Usuario | None:
        stmt = select(UsuarioModel).where(UsuarioModel.telefono == telefono)
        modelo = self._db.scalars(stmt).first()
        return mappers.usuario_a_dominio(modelo) if modelo else None


class SqlAlchemyPacienteRepository(PacienteRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def guardar(self, paciente: Paciente) -> Paciente:
        modelo = mappers.paciente_a_modelo(paciente)
        self._db.add(modelo)
        self._db.flush()
        return mappers.paciente_a_dominio(modelo)

    def buscar_por_id(self, paciente_id: UUID) -> Paciente | None:
        modelo = self._db.get(PacienteModel, paciente_id)
        return mappers.paciente_a_dominio(modelo) if modelo else None

    def buscar_por_dni(self, dni: str) -> Paciente | None:
        stmt = select(PacienteModel).where(PacienteModel.dni == dni)
        modelo = self._db.scalars(stmt).first()
        return mappers.paciente_a_dominio(modelo) if modelo else None


class SqlAlchemyUsuarioPacienteRepository(UsuarioPacienteRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def guardar(self, vinculo: UsuarioPaciente) -> UsuarioPaciente:
        modelo = mappers.vinculo_a_modelo(vinculo)
        self._db.add(modelo)
        self._db.flush()
        return mappers.vinculo_a_dominio(modelo)

    def listar_por_usuario(self, usuario_id: UUID) -> list[UsuarioPaciente]:
        stmt = select(UsuarioPacienteModel).where(
            UsuarioPacienteModel.usuario_id == usuario_id
        )
        modelos = self._db.scalars(stmt).all()
        return [mappers.vinculo_a_dominio(m) for m in modelos]

    def existe_vinculo_vigente(
        self, usuario_id: UUID, paciente_id: UUID, tipo_relacion: TipoRelacion
    ) -> bool:
        stmt = select(UsuarioPacienteModel).where(
            UsuarioPacienteModel.usuario_id == usuario_id,
            UsuarioPacienteModel.paciente_id == paciente_id,
            UsuarioPacienteModel.tipo_relacion == str(tipo_relacion),
            UsuarioPacienteModel.vigente.is_(True),
        )
        return self._db.scalars(stmt).first() is not None
