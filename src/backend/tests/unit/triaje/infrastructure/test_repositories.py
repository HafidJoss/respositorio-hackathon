import uuid

from app.modules.registro_pacientes.domain.entities import Paciente
from app.modules.registro_pacientes.infrastructure.repositories import SqlAlchemyPacienteRepository
from app.modules.triaje.domain.entities import NivelAtencion, Triaje
from app.modules.triaje.infrastructure.adapters import PacienteLookupAdapter
from app.modules.triaje.infrastructure.repositories import (
    SqlAlchemyCatalogoSintomasRepository,
    SqlAlchemyTriajeRepository,
    sembrar_catalogo_si_vacio,
)


def _crear_paciente(db_session) -> Paciente:
    repo = SqlAlchemyPacienteRepository(db_session)
    return repo.guardar(
        Paciente.crear(
            dni="87654321", nombres="Ana", apellidos="Quispe", edad=34, jurisdiccion_sis="Ayacucho"
        )
    )


def test_guardar_y_listar_triaje_por_paciente(db_session):
    paciente = _crear_paciente(db_session)
    repo = SqlAlchemyTriajeRepository(db_session)
    triaje = Triaje.crear(
        paciente_id=paciente.id,
        nombres="Ana",
        apellidos="Quispe",
        dni="87654321",
        edad=34,
        peso=60,
        talla=1.6,
        presion_arterial="140/95",
        sintomas=["fiebre"],
        nivel_atencion=NivelAtencion.CRITICO,
    )
    repo.guardar(triaje)

    listados = repo.listar_por_paciente(paciente.id)

    assert len(listados) == 1
    assert listados[0].nivel_atencion == NivelAtencion.CRITICO


def test_paciente_lookup_adapter_reutiliza_registro_pacientes(db_session):
    paciente = _crear_paciente(db_session)
    adapter = PacienteLookupAdapter(db_session)

    assert adapter.existe_paciente(paciente.id) is True
    assert adapter.existe_paciente(uuid.uuid4()) is False


def test_catalogo_sintomas_seed_y_lectura(db_session):
    sembrar_catalogo_si_vacio(db_session, ["fiebre", "tos"])
    repo = SqlAlchemyCatalogoSintomasRepository(db_session)

    assert repo.listar() == ["fiebre", "tos"]


def test_catalogo_sintomas_seed_no_duplica_si_ya_hay_datos(db_session):
    sembrar_catalogo_si_vacio(db_session, ["fiebre"])
    sembrar_catalogo_si_vacio(db_session, ["tos", "mareo"])
    repo = SqlAlchemyCatalogoSintomasRepository(db_session)

    assert repo.listar() == ["fiebre"]


def test_buscar_triaje_por_id(db_session):
    paciente = _crear_paciente(db_session)
    repo = SqlAlchemyTriajeRepository(db_session)
    triaje = repo.guardar(
        Triaje.crear(
            paciente_id=paciente.id,
            nombres="Ana",
            apellidos="Quispe",
            dni="87654321",
            edad=34,
            peso=60,
            talla=1.6,
            presion_arterial="140/95",
            sintomas=["fiebre"],
            nivel_atencion=NivelAtencion.LEVE,
        )
    )

    assert repo.buscar_por_id(triaje.id).id == triaje.id
    assert repo.buscar_por_id(uuid.uuid4()) is None
