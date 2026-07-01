from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.auth.domain.entities import Personal


class PersonalRepository(ABC):
    @abstractmethod
    def guardar(self, personal: Personal) -> Personal: ...

    @abstractmethod
    def buscar_por_id(self, personal_id: UUID) -> Personal | None: ...

    @abstractmethod
    def buscar_por_dni(self, dni: str) -> Personal | None: ...


class PasswordHasher(ABC):
    @abstractmethod
    def hashear(self, password: str) -> str: ...

    @abstractmethod
    def verificar(self, password: str, password_hash: str) -> bool: ...
