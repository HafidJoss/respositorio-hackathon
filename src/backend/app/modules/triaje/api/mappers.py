from app.modules.triaje.api.schemas import TriajeResponse
from app.modules.triaje.domain.entities import Triaje


def a_triaje_response(triaje: Triaje) -> TriajeResponse:
    return TriajeResponse(
        id=triaje.id,
        paciente_id=triaje.paciente_id,
        nombres=triaje.nombres,
        apellidos=triaje.apellidos,
        dni=triaje.dni,
        edad=triaje.edad,
        peso=triaje.peso,
        talla=triaje.talla,
        presion_arterial=str(triaje.presion_arterial),
        sintomas=triaje.sintomas,
        nivel_atencion=str(triaje.nivel_atencion),
        fecha_registro=triaje.fecha_registro,
    )
