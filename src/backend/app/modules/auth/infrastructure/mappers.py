from app.modules.auth.domain.entities import Personal, Rol
from app.modules.auth.domain.value_objects import Dni
from app.modules.auth.infrastructure.orm_models import PersonalModel


def personal_a_dominio(modelo: PersonalModel) -> Personal:
    return Personal(
        id=modelo.id,
        dni=Dni(modelo.dni),
        nombre=modelo.nombre,
        rol=Rol(modelo.rol),
        password_hash=modelo.password_hash,
        fecha_registro=modelo.fecha_registro,
    )


def personal_a_modelo(personal: Personal) -> PersonalModel:
    return PersonalModel(
        id=personal.id,
        dni=str(personal.dni),
        nombre=personal.nombre,
        rol=str(personal.rol),
        password_hash=personal.password_hash,
        fecha_registro=personal.fecha_registro,
    )
