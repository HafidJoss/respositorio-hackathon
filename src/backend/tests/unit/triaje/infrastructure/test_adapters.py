from uuid import uuid4

from app.modules.triaje.domain.entities import NivelAtencion, Triaje
from app.modules.triaje.infrastructure.adapters import NotificacionAdapterPendiente


def test_notificacion_adapter_pendiente_no_lanza_excepcion(caplog):
    triaje = Triaje.crear(
        paciente_id=uuid4(),
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

    with caplog.at_level("INFO"):
        NotificacionAdapterPendiente().notificar_triaje_urgente(triaje)

    assert "Notificación pendiente" in caplog.text
