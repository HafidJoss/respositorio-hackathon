from app.modules.registro_pacientes.domain.entities import (
    Paciente,
    TipoRelacion,
    Usuario,
    UsuarioPaciente,
)
from app.modules.registro_pacientes.domain.value_objects import Dni, Telefono
from app.modules.registro_pacientes.infrastructure.orm_models import (
    PacienteModel,
    UsuarioModel,
    UsuarioPacienteModel,
)


def usuario_a_dominio(modelo: UsuarioModel) -> Usuario:
    return Usuario(
        id=modelo.id,
        dni=Dni(modelo.dni),
        telefono=Telefono(modelo.telefono),
        fecha_registro=modelo.fecha_registro,
    )


def usuario_a_modelo(usuario: Usuario) -> UsuarioModel:
    return UsuarioModel(
        id=usuario.id,
        dni=str(usuario.dni),
        telefono=str(usuario.telefono),
        fecha_registro=usuario.fecha_registro,
    )


def paciente_a_dominio(modelo: PacienteModel) -> Paciente:
    return Paciente(
        id=modelo.id,
        dni=Dni(modelo.dni),
        nombres=modelo.nombres,
        apellidos=modelo.apellidos,
        edad=modelo.edad,
        jurisdiccion_sis=modelo.jurisdiccion_sis,
        fecha_registro=modelo.fecha_registro,
    )


def paciente_a_modelo(paciente: Paciente) -> PacienteModel:
    return PacienteModel(
        id=paciente.id,
        dni=str(paciente.dni),
        nombres=paciente.nombres,
        apellidos=paciente.apellidos,
        edad=paciente.edad,
        jurisdiccion_sis=paciente.jurisdiccion_sis,
        fecha_registro=paciente.fecha_registro,
    )


def vinculo_a_dominio(modelo: UsuarioPacienteModel) -> UsuarioPaciente:
    return UsuarioPaciente(
        id=modelo.id,
        usuario_id=modelo.usuario_id,
        paciente_id=modelo.paciente_id,
        tipo_relacion=TipoRelacion(modelo.tipo_relacion),
        vigente=modelo.vigente,
        fecha_vinculacion=modelo.fecha_vinculacion,
    )


def vinculo_a_modelo(vinculo: UsuarioPaciente) -> UsuarioPacienteModel:
    return UsuarioPacienteModel(
        id=vinculo.id,
        usuario_id=vinculo.usuario_id,
        paciente_id=vinculo.paciente_id,
        tipo_relacion=str(vinculo.tipo_relacion),
        vigente=vinculo.vigente,
        fecha_vinculacion=vinculo.fecha_vinculacion,
    )
