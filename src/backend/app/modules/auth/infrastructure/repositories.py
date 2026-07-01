from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.auth.domain.entities import Personal
from app.modules.auth.domain.ports import PersonalRepository
from app.modules.auth.infrastructure import mappers
from app.modules.auth.infrastructure.orm_models import PersonalModel


class SqlAlchemyPersonalRepository(PersonalRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def guardar(self, personal: Personal) -> Personal:
        modelo = mappers.personal_a_modelo(personal)
        self._db.add(modelo)
        self._db.flush()
        return mappers.personal_a_dominio(modelo)

    def buscar_por_id(self, personal_id: UUID) -> Personal | None:
        modelo = self._db.get(PersonalModel, personal_id)
        return mappers.personal_a_dominio(modelo) if modelo else None

    def buscar_por_dni(self, dni: str) -> Personal | None:
        stmt = select(PersonalModel).where(PersonalModel.dni == dni)
        modelo = self._db.scalars(stmt).first()
        return mappers.personal_a_dominio(modelo) if modelo else None
