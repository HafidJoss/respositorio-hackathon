from app.modules.auth.api.schemas import PersonalResponse
from app.modules.auth.domain.entities import Personal


def a_personal_response(personal: Personal) -> PersonalResponse:
    return PersonalResponse(
        id=personal.id,
        dni=str(personal.dni),
        nombre=personal.nombre,
        rol=str(personal.rol),
        fecha_registro=personal.fecha_registro,
    )
