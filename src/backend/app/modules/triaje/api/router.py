from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.triaje.api import mappers
from app.modules.triaje.api.schemas import TriajeCreate, TriajeResponse
from app.modules.triaje.application.dtos import RegistrarTriajeCommand
from app.modules.triaje.application.services import (
    ListarCatalogoSintomasService,
    ListarTriajesDePacienteService,
    ObtenerTriajeService,
    RegistrarTriajeService,
)
from app.modules.triaje.infrastructure.adapters import (
    NotificacionAdapterPendiente,
    PacienteLookupAdapter,
)
from app.modules.triaje.infrastructure.repositories import (
    SqlAlchemyCatalogoSintomasRepository,
    SqlAlchemyTriajeRepository,
)

router = APIRouter(tags=["triaje"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/triajes", response_model=TriajeResponse, status_code=201)
def registrar_triaje(payload: TriajeCreate, db: DbSession) -> TriajeResponse:
    servicio = RegistrarTriajeService(
        SqlAlchemyTriajeRepository(db),
        PacienteLookupAdapter(db),
        NotificacionAdapterPendiente(),
    )
    cmd = RegistrarTriajeCommand(**payload.model_dump())
    triaje = servicio.ejecutar(cmd)
    db.commit()
    return mappers.a_triaje_response(triaje)


@router.get("/triajes/{triaje_id}", response_model=TriajeResponse)
def obtener_triaje(triaje_id: UUID, db: DbSession) -> TriajeResponse:
    servicio = ObtenerTriajeService(SqlAlchemyTriajeRepository(db))
    triaje = servicio.ejecutar(triaje_id)
    return mappers.a_triaje_response(triaje)


@router.get("/pacientes/{paciente_id}/triajes", response_model=list[TriajeResponse])
def listar_triajes_de_paciente(paciente_id: UUID, db: DbSession) -> list[TriajeResponse]:
    servicio = ListarTriajesDePacienteService(
        SqlAlchemyTriajeRepository(db), PacienteLookupAdapter(db)
    )
    triajes = servicio.ejecutar(paciente_id)
    return [mappers.a_triaje_response(t) for t in triajes]


@router.get("/sintomas-comunes", response_model=list[str])
def listar_sintomas_comunes(db: DbSession) -> list[str]:
    servicio = ListarCatalogoSintomasService(SqlAlchemyCatalogoSintomasRepository(db))
    return servicio.ejecutar()
