class DominioError(Exception):
    """Base de errores de dominio de auth."""


class DniInvalidoError(DominioError):
    pass


class PasswordInvalidaError(DominioError):
    pass


class RolInvalidoError(DominioError):
    pass


class PersonalDuplicadoError(DominioError):
    pass


class CredencialesInvalidasError(DominioError):
    pass
