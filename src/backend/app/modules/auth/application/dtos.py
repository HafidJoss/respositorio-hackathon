from dataclasses import dataclass


@dataclass(slots=True)
class RegistrarPersonalCommand:
    dni: str
    nombre: str
    password: str
    rol: str


@dataclass(slots=True)
class AutenticarPersonalCommand:
    dni: str
    password: str
