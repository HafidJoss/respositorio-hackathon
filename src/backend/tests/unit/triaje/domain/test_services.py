from uuid import uuid4

import pytest

from app.modules.triaje.application.dtos import RegistrarTriajeCommand
from app.modules.triaje.application.services import (
    ListarCatalogoSintomasService,
    ListarTriajesDePacienteService,
    ObtenerTriajeService,
    RegistrarTriajeService,
)
from app.modules.triaje.domain.exceptions import (
    NivelAtencionInvalidoError,
    PacienteNoExisteError,
    TriajeNoEncontradoError,
)
from tests.unit.triaje.fakes import (
    FakeCatalogoSintomasRepository,
    FakeNotificacionPort,
    FakePacienteLookupPort,
    FakeTriajeRepository,
)


def _cmd(paciente_id, nivel_atencion="leve", **overrides):
    base = dict(
        paciente_id=paciente_id,
        nombres="Ana",
        apellidos="Quispe",
        dni="87654321",
        edad=34,
        peso=60.0,
        talla=1.6,
        presion_arterial="120/80",
        sintomas=["fiebre"],
        nivel_atencion=nivel_atencion,
    )
    base.update(overrides)
    return RegistrarTriajeCommand(**base)


def test_registrar_triaje_rechaza_paciente_inexistente():
    servicio = RegistrarTriajeService(
        FakeTriajeRepository(), FakePacienteLookupPort(), FakeNotificacionPort()
    )
    with pytest.raises(PacienteNoExisteError):
        servicio.ejecutar(_cmd(uuid4()))


def test_registrar_triaje_rechaza_nivel_atencion_vacio():
    paciente_id = uuid4()
    servicio = RegistrarTriajeService(
        FakeTriajeRepository(), FakePacienteLookupPort({paciente_id}), FakeNotificacionPort()
    )
    with pytest.raises(NivelAtencionInvalidoError):
        servicio.ejecutar(_cmd(paciente_id, nivel_atencion=""))


def test_registrar_triaje_rechaza_nivel_atencion_invalido():
    paciente_id = uuid4()
    servicio = RegistrarTriajeService(
        FakeTriajeRepository(), FakePacienteLookupPort({paciente_id}), FakeNotificacionPort()
    )
    with pytest.raises(NivelAtencionInvalidoError):
        servicio.ejecutar(_cmd(paciente_id, nivel_atencion="grave"))


def test_obtener_triaje_inexistente_lanza_error():
    with pytest.raises(TriajeNoEncontradoError):
        ObtenerTriajeService(FakeTriajeRepository()).ejecutar(uuid4())


def test_obtener_triaje_existente():
    paciente_id = uuid4()
    triaje_repo = FakeTriajeRepository()
    servicio = RegistrarTriajeService(
        triaje_repo, FakePacienteLookupPort({paciente_id}), FakeNotificacionPort()
    )
    creado = servicio.ejecutar(_cmd(paciente_id))
    encontrado = ObtenerTriajeService(triaje_repo).ejecutar(creado.id)
    assert encontrado.id == creado.id


def test_listar_triajes_de_paciente_inexistente_lanza_error():
    with pytest.raises(PacienteNoExisteError):
        ListarTriajesDePacienteService(
            FakeTriajeRepository(), FakePacienteLookupPort()
        ).ejecutar(uuid4())


def test_listar_triajes_de_paciente_existente():
    paciente_id = uuid4()
    triaje_repo = FakeTriajeRepository()
    lookup = FakePacienteLookupPort({paciente_id})
    RegistrarTriajeService(triaje_repo, lookup, FakeNotificacionPort()).ejecutar(_cmd(paciente_id))
    triajes = ListarTriajesDePacienteService(triaje_repo, lookup).ejecutar(paciente_id)
    assert len(triajes) == 1


def test_listar_catalogo_sintomas():
    servicio = ListarCatalogoSintomasService(FakeCatalogoSintomasRepository(["fiebre", "tos"]))
    assert servicio.ejecutar() == ["fiebre", "tos"]


def test_registrar_triaje_critico_dispara_notificacion():
    paciente_id = uuid4()
    notificacion = FakeNotificacionPort()
    servicio = RegistrarTriajeService(
        FakeTriajeRepository(), FakePacienteLookupPort({paciente_id}), notificacion
    )
    servicio.ejecutar(_cmd(paciente_id, nivel_atencion="critico"))
    assert len(notificacion.notificaciones_enviadas) == 1


def test_registrar_triaje_leve_no_dispara_notificacion():
    paciente_id = uuid4()
    notificacion = FakeNotificacionPort()
    servicio = RegistrarTriajeService(
        FakeTriajeRepository(), FakePacienteLookupPort({paciente_id}), notificacion
    )
    servicio.ejecutar(_cmd(paciente_id, nivel_atencion="leve"))
    assert notificacion.notificaciones_enviadas == []


def test_fallo_de_notificacion_no_revierte_guardado_del_triaje():
    paciente_id = uuid4()
    triaje_repo = FakeTriajeRepository()
    notificacion = FakeNotificacionPort(falla=True)
    servicio = RegistrarTriajeService(
        triaje_repo, FakePacienteLookupPort({paciente_id}), notificacion
    )
    triaje = servicio.ejecutar(_cmd(paciente_id, nivel_atencion="critico"))
    assert triaje_repo.buscar_por_id(triaje.id) is not None
