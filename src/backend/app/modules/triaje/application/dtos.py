from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class RegistrarTriajeCommand:
    paciente_id: UUID
    nombres: str
    apellidos: str
    dni: str
    edad: int
    peso: float
    talla: float
    presion_arterial: str
    sintomas: list[str]
    nivel_atencion: str
