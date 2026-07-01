import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    dni: Mapped[str] = mapped_column(String(8), unique=True, nullable=False, index=True)
    telefono: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    pacientes_vinculados: Mapped[list["UsuarioPacienteModel"]] = relationship(
        back_populates="usuario"
    )


class PacienteModel(Base):
    __tablename__ = "pacientes"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    dni: Mapped[str] = mapped_column(String(8), unique=True, nullable=False, index=True)
    nombres: Mapped[str] = mapped_column(String, nullable=False)
    apellidos: Mapped[str] = mapped_column(String, nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    jurisdiccion_sis: Mapped[str] = mapped_column(String, nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    usuarios_vinculados: Mapped[list["UsuarioPacienteModel"]] = relationship(
        back_populates="paciente"
    )


class UsuarioPacienteModel(Base):
    __tablename__ = "usuario_paciente"
    __table_args__ = (
        UniqueConstraint(
            "usuario_id", "paciente_id", "tipo_relacion", name="uq_usuario_paciente_relacion"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False
    )
    paciente_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("pacientes.id"), nullable=False
    )
    tipo_relacion: Mapped[str] = mapped_column(String, nullable=False)
    vigente: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fecha_vinculacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    usuario: Mapped["UsuarioModel"] = relationship(back_populates="pacientes_vinculados")
    paciente: Mapped["PacienteModel"] = relationship(back_populates="usuarios_vinculados")
