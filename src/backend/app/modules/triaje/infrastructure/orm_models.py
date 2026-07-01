import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TriajeModel(Base):
    __tablename__ = "triajes"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    paciente_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("pacientes.id"), nullable=False, index=True
    )
    nombres: Mapped[str] = mapped_column(String, nullable=False)
    apellidos: Mapped[str] = mapped_column(String, nullable=False)
    dni: Mapped[str] = mapped_column(String(8), nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    talla: Mapped[float] = mapped_column(Float, nullable=False)
    presion_arterial: Mapped[str] = mapped_column(String, nullable=False)
    sintomas: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    nivel_atencion: Mapped[str] = mapped_column(String, nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class CatalogoSintomaModel(Base):
    __tablename__ = "catalogo_sintomas"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
