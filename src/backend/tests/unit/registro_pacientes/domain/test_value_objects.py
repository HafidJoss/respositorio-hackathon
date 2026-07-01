import pytest

from app.modules.registro_pacientes.domain.exceptions import (
    DniInvalidoError,
    TelefonoInvalidoError,
)
from app.modules.registro_pacientes.domain.value_objects import Dni, Telefono


def test_dni_valido_se_acepta():
    assert str(Dni("12345678")) == "12345678"


@pytest.mark.parametrize("valor", ["1234567", "123456789", "1234567a", "", "12 34567"])
def test_dni_invalido_rechazado(valor):
    with pytest.raises(DniInvalidoError):
        Dni(valor)


def test_telefono_valido_se_acepta():
    assert str(Telefono("+51 987654321")) == "+51 987654321"


@pytest.mark.parametrize(
    "valor", ["987654321", "+51 887654321", "+51 98765432", "+511 987654321"]
)
def test_telefono_invalido_rechazado(valor):
    with pytest.raises(TelefonoInvalidoError):
        Telefono(valor)
