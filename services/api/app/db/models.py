"""SQLAlchemy ORM models for AMR Sentinel PostgreSQL schema."""
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

try:
    from pgvector.sqlalchemy import Vector
    PGVECTOR_AVAILABLE = True
except ImportError:
    PGVECTOR_AVAILABLE = False


def utc_now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    cases: Mapped[list["Case"]] = relationship("Case", back_populates="organization", cascade="all, delete-orphan")


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    patient_age_years: Mapped[float] = mapped_column(Float, nullable=False)
    patient_gender: Mapped[str] = mapped_column(String(32), default="female", nullable=False)
    patient_is_pregnant: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    patient_egfr_ml_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    patient_allergies: Mapped[list[str]] = mapped_column(JSONB if "JSONB" in locals() else Text, default=list)
    clinical_setting: Mapped[str] = mapped_column(String(64), default="outpatient", nullable=False)
    indication_code: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(64), default="draft", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="cases")
    prescription_lines: Mapped[list["PrescriptionLine"]] = relationship("PrescriptionLine", back_populates="case", cascade="all, delete-orphan")
    audit_runs: Mapped[list["AuditRun"]] = relationship("AuditRun", back_populates="case", cascade="all, delete-orphan")


class PrescriptionLine(Base):
    __tablename__ = "prescription_lines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    drug_name: Mapped[str] = mapped_column(String(255), nullable=False)
    dose_text: Mapped[str] = mapped_column(String(128), nullable=False)
    frequency_text: Mapped[str] = mapped_column(String(128), nullable=False)
    duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    case: Mapped["Case"] = relationship("Case", back_populates="prescription_lines")


class AuditRun(Base):
    __tablename__ = "audit_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cases.id", ondelete="CASCADE"), nullable=False)
    overall_status: Mapped[str] = mapped_column(String(64), nullable=False)
    rule_set_version: Mapped[str] = mapped_column(String(64), default="1.0.0", nullable=False)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    case: Mapped["Case"] = relationship("Case", back_populates="audit_runs")
    findings: Mapped[list["AuditFinding"]] = relationship("AuditFinding", back_populates="audit_run", cascade="all, delete-orphan")


class AuditFinding(Base):
    __tablename__ = "audit_findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("audit_runs.id", ondelete="CASCADE"), nullable=False)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    audit_run: Mapped["AuditRun"] = relationship("AuditRun", back_populates="findings")


class AMRGuidelineChunk(Base):
    __tablename__ = "amr_guideline_chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_category: Mapped[str] = mapped_column(String(64), nullable=False)
    file_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    chunk_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    heading: Mapped[str | None] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB if "JSONB" in locals() else Text, default=dict)
    
    # Vector embedding column (768 dimensions for Gemini text-embedding-004)
    if PGVECTOR_AVAILABLE:
        embedding: Mapped[Any] = mapped_column(Vector(768), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
