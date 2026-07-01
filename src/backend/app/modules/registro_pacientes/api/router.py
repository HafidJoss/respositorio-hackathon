from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.registro_pacientes.api import mappers
from app.modules.registro_pacientes.api.schemas import (
    PacienteCreate,
    PacienteRegistroResponse,
    PacienteResponse,
    UsuarioCreate,
    UsuarioResponse,
    VinculoCreate,
    VinculoResponse,
)
from app.modules.registro_pacientes.application.dtos import (
    RegistrarPacienteCommand,
    RegistrarUsuarioCommand,
    VincularUsuarioPacienteCommand,
)
from app.modules.registro_pacientes.application.services import (
    BuscarPacientePorDniService,
    ListarPacientesDeUsuarioService,
    ObtenerUsuarioService,
    RegistrarPacienteService,
    RegistrarUsuarioService,
    VincularUsuarioPacienteService,
)
from app.modules.registro_pacientes.domain.exceptions import PacienteNoEncontradoError
from app.modules.registro_pacientes.infrastructure.repositories import (
    SqlAlchemyPacienteRepository,
    SqlAlchemyUsuarioPacienteRepository,
    SqlAlchemyUsuarioRepository,
)

router = APIRouter(tags=["registro-pacientes"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/usuarios", response_model=UsuarioResponse, status_code=201)
def crear_usuario(payload: UsuarioCreate, db: DbSession) -> UsuarioResponse:
    servicio = RegistrarUsuarioService(SqlAlchemyUsuarioRepository(db))
    cmd = RegistrarUsuarioCommand(dni=payload.dni, telefono=payload.telefono)
    usuario = servicio.ejecutar(cmd)
    db.commit()
    return mappers.a_usuario_response(usuario)


@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: UUID, db: DbSession) -> UsuarioResponse:
    servicio = ObtenerUsuarioService(SqlAlchemyUsuarioRepository(db))
    usuario = servicio.ejecutar(usuario_id)
    return mappers.a_usuario_response(usuario)


@router.post("/pacientes", response_model=PacienteRegistroResponse, status_code=201)
def registrar_paciente(payload: PacienteCreate, db: DbSession) -> PacienteRegistroResponse:
    servicio = RegistrarPacienteService(
        SqlAlchemyPacienteRepository(db),
        SqlAlchemyUsuarioRepository(db),
        SqlAlchemyUsuarioPacienteRepository(db),
    )
    cmd = RegistrarPacienteCommand(
        dni=payload.dni,
        nombres=payload.nombres,
        apellidos=payload.apellidos,
        edad=payload.edad,
        jurisdiccion_sis=payload.jurisdiccion_sis,
        usuario_id=payload.usuario_id,
        tipo_relacion=payload.tipo_relacion,
    )
    resultado = servicio.ejecutar(cmd)
    db.commit()
    return mappers.a_paciente_registro_response(resultado.paciente, resultado.creado)


@router.get("/pacientes", response_model=PacienteResponse)
def buscar_paciente_por_dni(
    db: DbSession, dni: Annotated[str, Query(min_length=8, max_length=8)]
) -> PacienteResponse:
    servicio = BuscarPacientePorDniService(SqlAlchemyPacienteRepository(db))
    paciente = servicio.ejecutar(dni)
    if paciente is None:
        raise PacienteNoEncontradoError(f"No existe Paciente con DNI {dni}")
    return mappers.a_paciente_response(paciente)


@router.post(
    "/usuarios/{usuario_id}/pacientes", response_model=VinculoResponse, status_code=201
)
def vincular_paciente_a_usuario(
    usuario_id: UUID, payload: VinculoCreate, db: DbSession
) -> VinculoResponse:
    servicio = VincularUsuarioPacienteService(
        SqlAlchemyUsuarioRepository(db),
        SqlAlchemyPacienteRepository(db),
        SqlAlchemyUsuarioPacienteRepository(db),
    )
    cmd = VincularUsuarioPacienteCommand(
        usuario_id=usuario_id,
        paciente_id=payload.paciente_id,
        tipo_relacion=payload.tipo_relacion,
    )
    vinculo = servicio.ejecutar(cmd)
    db.commit()
    return mappers.a_vinculo_response(vinculo)


@router.get("/usuarios/{usuario_id}/pacientes", response_model=list[VinculoResponse])
def listar_pacientes_de_usuario(usuario_id: UUID, db: DbSession) -> list[VinculoResponse]:
    servicio = ListarPacientesDeUsuarioService(
        SqlAlchemyUsuarioRepository(db), SqlAlchemyUsuarioPacienteRepository(db)
    )
    vinculos = servicio.ejecutar(usuario_id)
    return [mappers.a_vinculo_response(v) for v in vinculos]
