class DominioError(Exception):
    """Base de errores de dominio de triaje."""


class NivelAtencionInvalidoError(DominioError):
    pass


class SignosVitalesInvalidosError(DominioError):
    pass


class PacienteNoExisteError(DominioError):
    pass


class TriajeNoEncontradoError(DominioError):
    pass
