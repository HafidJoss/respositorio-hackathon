class DominioError(Exception):
    """Base de errores de dominio de registro-pacientes."""


class DniInvalidoError(DominioError):
    pass


class TelefonoInvalidoError(DominioError):
    pass


class EdadInvalidaError(DominioError):
    pass


class TipoRelacionInvalidaError(DominioError):
    pass


class UsuarioDuplicadoError(DominioError):
    pass


class UsuarioNoEncontradoError(DominioError):
    pass


class PacienteNoEncontradoError(DominioError):
    pass


class VinculoDuplicadoError(DominioError):
    pass
