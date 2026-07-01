from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def _manejador(status_code: int):
    async def manejar(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": str(exc)})

    return manejar


def registrar_manejadores_dominio(
    app: FastAPI,
    *,
    invalidos: tuple[type[Exception], ...] = (),
    duplicados: tuple[type[Exception], ...] = (),
    no_encontrados: tuple[type[Exception], ...] = (),
) -> None:
    """Traduce excepciones de dominio a respuestas HTTP estructuradas.

    Ningún endpoint atrapa estas excepciones con print()/exit(); el
    contexto (mensaje de dominio) viaja intacto en el body de error.
    """
    for excepcion in invalidos:
        app.add_exception_handler(excepcion, _manejador(400))
    for excepcion in duplicados:
        app.add_exception_handler(excepcion, _manejador(409))
    for excepcion in no_encontrados:
        app.add_exception_handler(excepcion, _manejador(404))
