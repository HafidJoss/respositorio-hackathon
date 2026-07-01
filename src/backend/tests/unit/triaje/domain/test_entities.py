from uuid import uuid4

import pytest

from app.modules.triaje.domain.entities import NivelAtencion, Triaje
from app.modules.triaje.domain.exceptions import SignosVitalesInvalidosError


def _crear(nivel: NivelAtencion, peso: float = 60, talla: float = 1.6) -> Triaje:
    return Triaje.crear(
        paciente_id=uuid4(),
        nombres="Ana",
        apellidos="Quispe",
        dni="87654321",
        edad=34,
        peso=peso,
        talla=talla,
        presion_arterial="120/80",
        sintomas=["fiebre"],
        nivel_atencion=nivel,
    )


@pytest.mark.parametrize(
    "nivel,esperado",
    [(NivelAtencion.CRITICO, True), (NivelAtencion.MODERADO, True), (NivelAtencion.LEVE, False)],
)
def test_requiere_notificacion_medico(nivel, esperado):
    assert _crear(nivel).requiere_notificacion_medico() is esperado


@pytest.mark.parametrize("peso,talla", [(0, 1.6), (60, 0), (-1, 1.6)])
def test_peso_o_talla_invalidos_rechazados(peso, talla):
    with pytest.raises(SignosVitalesInvalidosError):
        _crear(NivelAtencion.LEVE, peso=peso, talla=talla)
