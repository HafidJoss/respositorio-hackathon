from uuid import uuid4

import pytest

from app.modules.registro_pacientes.domain.entities import Paciente, TipoRelacion, Usuario, UsuarioPaciente
from app.modules.registro_pacientes.domain.exceptions import EdadInvalidaError


def test_usuario_crear_genera_id_y_fecha():
    usuario = Usuario.crear(dni="12345678", telefono="+51 987654321")
    assert usuario.id is not None
    assert usuario.fecha_registro is not None


def test_paciente_crear_valido():
    paciente = Paciente.crear(
        dni="87654321", nombres="Ana", apellidos="Quispe", edad=34, jurisdiccion_sis="Ayacucho"
    )
    assert paciente.edad == 34


@pytest.mark.parametrize("edad", [-1, 131])
def test_paciente_edad_invalida_rechazada(edad):
    with pytest.raises(EdadInvalidaError):
        Paciente.crear(
            dni="87654321", nombres="Ana", apellidos="Quispe", edad=edad, jurisdiccion_sis="Ayacucho"
        )


def test_usuario_paciente_crear_vigente_por_defecto():
    vinculo = UsuarioPaciente.crear(
        usuario_id=uuid4(),
        paciente_id=uuid4(),
        tipo_relacion=TipoRelacion.TITULAR,
    )
    assert vinculo.vigente is True
