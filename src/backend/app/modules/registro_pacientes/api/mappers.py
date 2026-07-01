from app.modules.registro_pacientes.api.schemas import (
    PacienteRegistroResponse,
    PacienteResponse,
    UsuarioResponse,
    VinculoResponse,
)
from app.modules.registro_pacientes.domain.entities import (
    Paciente,
    Usuario,
    UsuarioPaciente,
)


def a_usuario_response(usuario: Usuario) -> UsuarioResponse:
    return UsuarioResponse(
        id=usuario.id,
        dni=str(usuario.dni),
        telefono=str(usuario.telefono),
        fecha_registro=usuario.fecha_registro,
    )


def a_paciente_response(paciente: Paciente) -> PacienteResponse:
    return PacienteResponse(
        id=paciente.id,
        dni=str(paciente.dni),
        nombres=paciente.nombres,
        apellidos=paciente.apellidos,
        edad=paciente.edad,
        jurisdiccion_sis=paciente.jurisdiccion_sis,
        fecha_registro=paciente.fecha_registro,
    )


def a_paciente_registro_response(
    paciente: Paciente, creado: bool
) -> PacienteRegistroResponse:
    base = a_paciente_response(paciente)
    return PacienteRegistroResponse(**base.model_dump(), ya_existia=not creado)


def a_vinculo_response(vinculo: UsuarioPaciente) -> VinculoResponse:
    return VinculoResponse(
        id=vinculo.id,
        usuario_id=vinculo.usuario_id,
        paciente_id=vinculo.paciente_id,
        tipo_relacion=str(vinculo.tipo_relacion),
        vigente=vinculo.vigente,
        fecha_vinculacion=vinculo.fecha_vinculacion,
    )
