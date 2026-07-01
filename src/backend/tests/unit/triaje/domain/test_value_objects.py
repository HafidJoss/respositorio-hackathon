import pytest

from app.modules.triaje.domain.exceptions import SignosVitalesInvalidosError
from app.modules.triaje.domain.value_objects import PresionArterial


def test_presion_arterial_valida():
    assert str(PresionArterial("120/80")) == "120/80"


@pytest.mark.parametrize("valor", ["120-80", "120", "abc/80", ""])
def test_presion_arterial_invalida(valor):
    with pytest.raises(SignosVitalesInvalidosError):
        PresionArterial(valor)
