import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.triaje.domain.entities import Triaje
from app.modules.triaje.domain.ports import CatalogoSintomasRepository, TriajeRepository
from app.modules.triaje.infrastructure import mappers
from app.modules.triaje.infrastructure.orm_models import CatalogoSintomaModel, TriajeModel


class SqlAlchemyTriajeRepository(TriajeRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def guardar(self, triaje: Triaje) -> Triaje:
        modelo = mappers.triaje_a_modelo(triaje)
        self._db.add(modelo)
        self._db.flush()
        return mappers.triaje_a_dominio(modelo)

    def buscar_por_id(self, triaje_id: UUID) -> Triaje | None:
        modelo = self._db.get(TriajeModel, triaje_id)
        return mappers.triaje_a_dominio(modelo) if modelo else None

    def listar_por_paciente(self, paciente_id: UUID) -> list[Triaje]:
        stmt = select(TriajeModel).where(TriajeModel.paciente_id == paciente_id)
        modelos = self._db.scalars(stmt).all()
        return [mappers.triaje_a_dominio(m) for m in modelos]


class SqlAlchemyCatalogoSintomasRepository(CatalogoSintomasRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def listar(self) -> list[str]:
        stmt = select(CatalogoSintomaModel.nombre).order_by(CatalogoSintomaModel.nombre)
        return list(self._db.scalars(stmt).all())


def sembrar_catalogo_si_vacio(db: Session, sintomas: list[str]) -> None:
    """Seed manual del catálogo — no expuesto por API (fase-0 §MUST: solo lectura)."""
    if db.scalars(select(CatalogoSintomaModel).limit(1)).first() is not None:
        return
    for nombre in sintomas:
        db.add(CatalogoSintomaModel(id=uuid.uuid4(), nombre=nombre))
    db.commit()
