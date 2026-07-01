from fastapi import FastAPI

app = FastAPI(title="Sistema de Gestión de Urgencias y Triaje - Posta Médica Rural")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Emergency and Triage Management System API"}

# Module routers will be included here:
# from src.registro_pacientes.infrastructure.api import router as registro_pacientes_router
# app.include_router(registro_pacientes_router)
