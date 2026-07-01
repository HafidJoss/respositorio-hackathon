import logging

from fastapi import FastAPI

from app.core.errors import registrar_manejadores_dominio

logging.basicConfig(level=logging.INFO, force=True)
from app.modules.registro_pacientes.api.router import router as registro_pacientes_router
from app.modules.registro_pacientes.domain import exceptions as rp_exc
from app.modules.triaje.api.router import router as triaje_router
from app.modules.triaje.domain import exceptions as triaje_exc

app = FastAPI(
    title="Sistema de Gestión de Urgencias y Triaje — Posta Médica Rural",
    version="0.1.0",
)

app.include_router(registro_pacientes_router)
app.include_router(triaje_router)

registrar_manejadores_dominio(
    app,
    invalidos=(
        rp_exc.DniInvalidoError,
        rp_exc.TelefonoInvalidoError,
        rp_exc.EdadInvalidaError,
        rp_exc.TipoRelacionInvalidaError,
        triaje_exc.NivelAtencionInvalidoError,
        triaje_exc.SignosVitalesInvalidosError,
    ),
    duplicados=(
        rp_exc.UsuarioDuplicadoError,
        rp_exc.VinculoDuplicadoError,
    ),
    no_encontrados=(
        rp_exc.UsuarioNoEncontradoError,
        rp_exc.PacienteNoEncontradoError,
        triaje_exc.PacienteNoExisteError,
        triaje_exc.TriajeNoEncontradoError,
    ),
)


@app.get("/health", tags=["infraestructura"])
def health() -> dict[str, str]:
    return {"estado": "ok"}
