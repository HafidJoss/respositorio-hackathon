from app.modules.auth.application.dtos import (
    AutenticarPersonalCommand,
    RegistrarPersonalCommand,
)
from app.modules.auth.domain.entities import Personal, Rol
from app.modules.auth.domain.exceptions import (
    CredencialesInvalidasError,
    PersonalDuplicadoError,
    RolInvalidoError,
)
from app.modules.auth.domain.ports import PasswordHasher, PersonalRepository
from app.modules.auth.domain.value_objects import Password


def _parsear_rol(valor: str) -> Rol:
    try:
        return Rol(valor)
    except ValueError as error:
        raise RolInvalidoError(f"rol inválido: '{valor}'") from error


class RegistrarPersonalService:
    def __init__(self, personal_repo: PersonalRepository, hasher: PasswordHasher) -> None:
        self._personal_repo = personal_repo
        self._hasher = hasher

    def ejecutar(self, cmd: RegistrarPersonalCommand) -> Personal:
        if self._personal_repo.buscar_por_dni(cmd.dni) is not None:
            raise PersonalDuplicadoError(f"Ya existe personal con DNI {cmd.dni}")
        rol = _parsear_rol(cmd.rol)
        Password(cmd.password)  # valida longitud mínima
        password_hash = self._hasher.hashear(cmd.password)
        personal = Personal.crear(
            dni=cmd.dni, nombre=cmd.nombre, rol=rol, password_hash=password_hash
        )
        return self._personal_repo.guardar(personal)


class AutenticarPersonalService:
    def __init__(self, personal_repo: PersonalRepository, hasher: PasswordHasher) -> None:
        self._personal_repo = personal_repo
        self._hasher = hasher

    def ejecutar(self, cmd: AutenticarPersonalCommand) -> Personal:
        personal = self._personal_repo.buscar_por_dni(cmd.dni)
        if personal is None or not self._hasher.verificar(cmd.password, personal.password_hash):
            raise CredencialesInvalidasError("DNI o contraseña incorrectos")
        return personal
