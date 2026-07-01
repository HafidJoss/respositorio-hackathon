from app.modules.triaje.domain.entities import NivelAtencion, Triaje
from app.modules.triaje.domain.value_objects import PresionArterial
from app.modules.triaje.infrastructure.orm_models import TriajeModel


def triaje_a_dominio(modelo: TriajeModel) -> Triaje:
    return Triaje(
        id=modelo.id,
        paciente_id=modelo.paciente_id,
        nombres=modelo.nombres,
        apellidos=modelo.apellidos,
        dni=modelo.dni,
        edad=modelo.edad,
        peso=modelo.peso,
        talla=modelo.talla,
        presion_arterial=PresionArterial(modelo.presion_arterial),
        sintomas=list(modelo.sintomas),
        nivel_atencion=NivelAtencion(modelo.nivel_atencion),
        fecha_registro=modelo.fecha_registro,
    )


def triaje_a_modelo(triaje: Triaje) -> TriajeModel:
    return TriajeModel(
        id=triaje.id,
        paciente_id=triaje.paciente_id,
        nombres=triaje.nombres,
        apellidos=triaje.apellidos,
        dni=triaje.dni,
        edad=triaje.edad,
        peso=triaje.peso,
        talla=triaje.talla,
        presion_arterial=str(triaje.presion_arterial),
        sintomas=list(triaje.sintomas),
        nivel_atencion=str(triaje.nivel_atencion),
        fecha_registro=triaje.fecha_registro,
    )
