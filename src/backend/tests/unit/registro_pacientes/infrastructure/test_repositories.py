from app.modules.registro_pacientes.domain.entities import Paciente, TipoRelacion, Usuario, UsuarioPaciente
from app.modules.registro_pacientes.infrastructure.repositories import (
    SqlAlchemyPacienteRepository,
    SqlAlchemyUsuarioPacienteRepository,
    SqlAlchemyUsuarioRepository,
)


def test_guardar_y_buscar_usuario_por_dni(db_session):
    repo = SqlAlchemyUsuarioRepository(db_session)
    usuario = Usuario.crear(dni="12345678", telefono="+51 987654321")
    repo.guardar(usuario)

    encontrado = repo.buscar_por_dni("12345678")

    assert encontrado is not None
    assert encontrado.id == usuario.id
    assert str(encontrado.telefono) == "+51 987654321"


def test_buscar_por_dni_inexistente_retorna_none(db_session):
    repo = SqlAlchemyUsuarioRepository(db_session)
    assert repo.buscar_por_dni("00000000") is None


def test_buscar_usuario_por_id_y_telefono(db_session):
    repo = SqlAlchemyUsuarioRepository(db_session)
    usuario = repo.guardar(Usuario.crear(dni="12345678", telefono="+51 987654321"))

    assert repo.buscar_por_id(usuario.id).id == usuario.id
    assert repo.buscar_por_telefono("+51 987654321").id == usuario.id
    assert repo.buscar_por_telefono("+51 900000000") is None


def test_buscar_usuario_por_id_inexistente_retorna_none(db_session):
    from uuid import uuid4

    repo = SqlAlchemyUsuarioRepository(db_session)
    assert repo.buscar_por_id(uuid4()) is None


def test_buscar_paciente_por_id(db_session):
    repo = SqlAlchemyPacienteRepository(db_session)
    paciente = repo.guardar(
        Paciente.crear(
            dni="87654321", nombres="Ana", apellidos="Quispe", edad=34, jurisdiccion_sis="Ayacucho"
        )
    )
    assert repo.buscar_por_id(paciente.id).id == paciente.id


def test_buscar_paciente_por_dni(db_session):
    repo = SqlAlchemyPacienteRepository(db_session)
    repo.guardar(
        Paciente.crear(
            dni="87654321", nombres="Ana", apellidos="Quispe", edad=34, jurisdiccion_sis="Ayacucho"
        )
    )
    assert repo.buscar_por_dni("87654321") is not None
    assert repo.buscar_por_dni("00000000") is None


def test_guardar_paciente_y_vinculo(db_session):
    usuario_repo = SqlAlchemyUsuarioRepository(db_session)
    paciente_repo = SqlAlchemyPacienteRepository(db_session)
    vinculo_repo = SqlAlchemyUsuarioPacienteRepository(db_session)

    usuario = usuario_repo.guardar(Usuario.crear(dni="11111111", telefono="+51 911111111"))
    paciente = paciente_repo.guardar(
        Paciente.crear(
            dni="87654321", nombres="Ana", apellidos="Quispe", edad=34, jurisdiccion_sis="Ayacucho"
        )
    )
    vinculo = vinculo_repo.guardar(
        UsuarioPaciente.crear(usuario.id, paciente.id, TipoRelacion.TITULAR)
    )

    assert vinculo_repo.existe_vinculo_vigente(usuario.id, paciente.id, TipoRelacion.TITULAR)
    listados = vinculo_repo.listar_por_usuario(usuario.id)
    assert len(listados) == 1
    assert listados[0].id == vinculo.id
