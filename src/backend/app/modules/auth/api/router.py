from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.api import mappers
from app.modules.auth.api.schemas import PersonalCreate, PersonalLogin, PersonalResponse
from app.modules.auth.application.dtos import (
    AutenticarPersonalCommand,
    RegistrarPersonalCommand,
)
from app.modules.auth.application.services import (
    AutenticarPersonalService,
    RegistrarPersonalService,
)
from app.modules.auth.infrastructure.repositories import SqlAlchemyPersonalRepository
from app.modules.auth.infrastructure.security import Pbkdf2PasswordHasher

router = APIRouter(prefix="/auth", tags=["auth"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/registro", response_model=PersonalResponse, status_code=201)
def registrar_personal(payload: PersonalCreate, db: DbSession) -> PersonalResponse:
    servicio = RegistrarPersonalService(
        SqlAlchemyPersonalRepository(db), Pbkdf2PasswordHasher()
    )
    cmd = RegistrarPersonalCommand(
        dni=payload.dni, nombre=payload.nombre, password=payload.password, rol=payload.rol
    )
    personal = servicio.ejecutar(cmd)
    db.commit()
    return mappers.a_personal_response(personal)


@router.post("/login", response_model=PersonalResponse)
def login(payload: PersonalLogin, db: DbSession) -> PersonalResponse:
    servicio = AutenticarPersonalService(
        SqlAlchemyPersonalRepository(db), Pbkdf2PasswordHasher()
    )
    cmd = AutenticarPersonalCommand(dni=payload.dni, password=payload.password)
    personal = servicio.ejecutar(cmd)
    return mappers.a_personal_response(personal)
