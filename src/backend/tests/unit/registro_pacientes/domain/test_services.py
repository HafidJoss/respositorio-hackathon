from uuid import uuid4

import pytest

from app.modules.registro_pacientes.application.dtos import (
    RegistrarPacienteCommand,
    RegistrarUsuarioCommand,
    VincularUsuarioPacienteCommand,
)
from app.modules.registro_pacientes.application.services import (
    BuscarPacientePorDniService,
    ListarPacientesDeUsuarioService,
    ObtenerUsuarioService,
    RegistrarPacienteService,
    RegistrarUsuarioService,
    VincularUsuarioPacienteService,
)
from app.modules.registro_pacientes.domain.exceptions import (
    TipoRelacionInvalidaError,
    UsuarioDuplicadoError,
    UsuarioNoEncontradoError,
    VinculoDuplicadoError,
)
from tests.unit.registro_pacientes.fakes import (
    FakePacienteRepository,
    FakeUsuarioPacienteRepository,
    FakeUsuarioRepository,
)


def test_registrar_usuario_rechaza_dni_duplicado():
    usuario_repo = FakeUsuarioRepository()
    servicio = RegistrarUsuarioService(usuario_repo)
    servicio.ejecutar(RegistrarUsuarioCommand(dni="12345678", telefono="+51 987654321"))
    with pytest.raises(UsuarioDuplicadoError):
        servicio.ejecutar(RegistrarUsuarioCommand(dni="12345678", telefono="+51 911111111"))


def test_registrar_usuario_rechaza_telefono_duplicado():
    usuario_repo = FakeUsuarioRepository()
    servicio = RegistrarUsuarioService(usuario_repo)
    servicio.ejecutar(RegistrarUsuarioCommand(dni="12345678", telefono="+51 987654321"))
    with pytest.raises(UsuarioDuplicadoError):
        servicio.ejecutar(RegistrarUsuarioCommand(dni="87654321", telefono="+51 987654321"))


def test_obtener_usuario_inexistente_lanza_error():
    with pytest.raises(UsuarioNoEncontradoError):
        ObtenerUsuarioService(FakeUsuarioRepository()).ejecutar(uuid4())


def test_obtener_usuario_existente():
    usuario_repo = FakeUsuarioRepository()
    usuario = RegistrarUsuarioService(usuario_repo).ejecutar(
        RegistrarUsuarioCommand(dni="12345678", telefono="+51 987654321")
    )
    encontrado = ObtenerUsuarioService(usuario_repo).ejecutar(usuario.id)
    assert encontrado.id == usuario.id


def test_buscar_paciente_por_dni_inexistente_retorna_none():
    assert BuscarPacientePorDniService(FakePacienteRepository()).ejecutar("00000000") is None


def test_vincular_usuario_paciente_rechaza_usuario_inexistente():
    servicio = VincularUsuarioPacienteService(
        FakeUsuarioRepository(), FakePacienteRepository(), FakeUsuarioPacienteRepository()
    )
    with pytest.raises(UsuarioNoEncontradoError):
        servicio.ejecutar(
            VincularUsuarioPacienteCommand(
                usuario_id=uuid4(), paciente_id=uuid4(), tipo_relacion="titular"
            )
        )


def test_vincular_usuario_paciente_rechaza_paciente_inexistente():
    usuario_repo = FakeUsuarioRepository()
    usuario = RegistrarUsuarioService(usuario_repo).ejecutar(
        RegistrarUsuarioCommand(dni="12345678", telefono="+51 987654321")
    )
    servicio = VincularUsuarioPacienteService(
        usuario_repo, FakePacienteRepository(), FakeUsuarioPacienteRepository()
    )
    with pytest.raises(UsuarioNoEncontradoError):
        servicio.ejecutar(
            VincularUsuarioPacienteCommand(
                usuario_id=usuario.id, paciente_id=uuid4(), tipo_relacion="titular"
            )
        )


def test_vincular_usuario_paciente_exitoso():
    usuario_repo = FakeUsuarioRepository()
    paciente_repo = FakePacienteRepository()
    vinculo_repo = FakeUsuarioPacienteRepository()
    usuario = RegistrarUsuarioService(usuario_repo).ejecutar(
        RegistrarUsuarioCommand(dni="11111111", telefono="+51 911111111")
    )
    otro_usuario = RegistrarUsuarioService(usuario_repo).ejecutar(
        RegistrarUsuarioCommand(dni="22222222", telefono="+51 922222222")
    )
    resultado = RegistrarPacienteService(paciente_repo, usuario_repo, vinculo_repo).ejecutar(
        RegistrarPacienteCommand(
            dni="87654321",
            nombres="Ana",
            apellidos="Quispe",
            edad=34,
            jurisdiccion_sis="Ayacucho",
            usuario_id=usuario.id,
            tipo_relacion="titular",
        )
    )
    servicio = VincularUsuarioPacienteService(usuario_repo, paciente_repo, vinculo_repo)
    vinculo = servicio.ejecutar(
        VincularUsuarioPacienteCommand(
            usuario_id=otro_usuario.id,
            paciente_id=resultado.paciente.id,
            tipo_relacion="tutor_legal",
        )
    )
    assert vinculo.usuario_id == otro_usuario.id


def test_registrar_paciente_rechaza_tipo_relacion_invalido():
    usuario_repo = FakeUsuarioRepository()
    usuario = RegistrarUsuarioService(usuario_repo).ejecutar(
        RegistrarUsuarioCommand(dni="12345678", telefono="+51 987654321")
    )
    servicio = RegistrarPacienteService(
        FakePacienteRepository(), usuario_repo, FakeUsuarioPacienteRepository()
    )
    with pytest.raises(TipoRelacionInvalidaError):
        servicio.ejecutar(
            RegistrarPacienteCommand(
                dni="87654321",
                nombres="Ana",
                apellidos="Quispe",
                edad=34,
                jurisdiccion_sis="Ayacucho",
                usuario_id=usuario.id,
                tipo_relacion="hermano",
            )
        )


def test_registrar_paciente_rechaza_usuario_inexistente():
    servicio = RegistrarPacienteService(
        FakePacienteRepository(), FakeUsuarioRepository(), FakeUsuarioPacienteRepository()
    )
    with pytest.raises(UsuarioNoEncontradoError):
        servicio.ejecutar(
            RegistrarPacienteCommand(
                dni="87654321",
                nombres="Ana",
                apellidos="Quispe",
                edad=34,
                jurisdiccion_sis="Ayacucho",
                usuario_id=uuid4(),
                tipo_relacion="titular",
            )
        )


def test_registrar_paciente_dni_existente_ya_vinculado_rechaza():
    usuario_repo = FakeUsuarioRepository()
    paciente_repo = FakePacienteRepository()
    vinculo_repo = FakeUsuarioPacienteRepository()
    usuario = RegistrarUsuarioService(usuario_repo).ejecutar(
        RegistrarUsuarioCommand(dni="12345678", telefono="+51 987654321")
    )
    servicio = RegistrarPacienteService(paciente_repo, usuario_repo, vinculo_repo)
    cmd = RegistrarPacienteCommand(
        dni="87654321",
        nombres="Ana",
        apellidos="Quispe",
        edad=34,
        jurisdiccion_sis="Ayacucho",
        usuario_id=usuario.id,
        tipo_relacion="titular",
    )
    servicio.ejecutar(cmd)
    with pytest.raises(VinculoDuplicadoError):
        servicio.ejecutar(cmd)


def test_listar_pacientes_de_usuario_inexistente_lanza_error():
    with pytest.raises(UsuarioNoEncontradoError):
        ListarPacientesDeUsuarioService(
            FakeUsuarioRepository(), FakeUsuarioPacienteRepository()
        ).ejecutar(uuid4())


def test_listar_pacientes_de_usuario_devuelve_vinculos():
    usuario_repo = FakeUsuarioRepository()
    paciente_repo = FakePacienteRepository()
    vinculo_repo = FakeUsuarioPacienteRepository()
    usuario = RegistrarUsuarioService(usuario_repo).ejecutar(
        RegistrarUsuarioCommand(dni="12345678", telefono="+51 987654321")
    )
    RegistrarPacienteService(paciente_repo, usuario_repo, vinculo_repo).ejecutar(
        RegistrarPacienteCommand(
            dni="87654321",
            nombres="Ana",
            apellidos="Quispe",
            edad=34,
            jurisdiccion_sis="Ayacucho",
            usuario_id=usuario.id,
            tipo_relacion="titular",
        )
    )
    vinculos = ListarPacientesDeUsuarioService(usuario_repo, vinculo_repo).ejecutar(usuario.id)
    assert len(vinculos) == 1


def test_registrar_paciente_dni_duplicado_ofrece_vinculo_no_duplica():
    usuario_repo = FakeUsuarioRepository()
    paciente_repo = FakePacienteRepository()
    vinculo_repo = FakeUsuarioPacienteRepository()
    usuario1 = RegistrarUsuarioService(usuario_repo).ejecutar(
        RegistrarUsuarioCommand(dni="11111111", telefono="+51 911111111")
    )
    usuario2 = RegistrarUsuarioService(usuario_repo).ejecutar(
        RegistrarUsuarioCommand(dni="22222222", telefono="+51 922222222")
    )
    servicio = RegistrarPacienteService(paciente_repo, usuario_repo, vinculo_repo)
    cmd_base = dict(
        dni="87654321", nombres="Ana", apellidos="Quispe", edad=34, jurisdiccion_sis="Ayacucho"
    )
    primero = servicio.ejecutar(
        RegistrarPacienteCommand(**cmd_base, usuario_id=usuario1.id, tipo_relacion="titular")
    )
    segundo = servicio.ejecutar(
        RegistrarPacienteCommand(**cmd_base, usuario_id=usuario2.id, tipo_relacion="tutor_legal")
    )

    assert primero.creado is True
    assert segundo.creado is False
    assert segundo.paciente.id == primero.paciente.id
    assert len(paciente_repo._pacientes) == 1


def test_vincular_usuario_paciente_rechaza_vinculo_duplicado():
    usuario_repo = FakeUsuarioRepository()
    paciente_repo = FakePacienteRepository()
    vinculo_repo = FakeUsuarioPacienteRepository()
    usuario = RegistrarUsuarioService(usuario_repo).ejecutar(
        RegistrarUsuarioCommand(dni="11111111", telefono="+51 911111111")
    )
    resultado = RegistrarPacienteService(paciente_repo, usuario_repo, vinculo_repo).ejecutar(
        RegistrarPacienteCommand(
            dni="87654321",
            nombres="Ana",
            apellidos="Quispe",
            edad=34,
            jurisdiccion_sis="Ayacucho",
            usuario_id=usuario.id,
            tipo_relacion="titular",
        )
    )
    servicio = VincularUsuarioPacienteService(usuario_repo, paciente_repo, vinculo_repo)
    with pytest.raises(VinculoDuplicadoError):
        servicio.ejecutar(
            VincularUsuarioPacienteCommand(
                usuario_id=usuario.id,
                paciente_id=resultado.paciente.id,
                tipo_relacion="titular",
            )
        )
