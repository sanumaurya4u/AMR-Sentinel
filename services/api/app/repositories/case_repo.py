"""Repository layer for persisting clinical cases and audit evaluations via SQLAlchemy ORM."""
import uuid
from typing import Any

from app.db.models import AuditFinding, AuditRun, Case, PrescriptionLine
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class CaseRepository:
    """Async repository for managing Case entities with SQLAlchemy ORM."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_case(
        self,
        org_id: uuid.UUID,
        patient_context: dict[str, Any],
        indication_code: str,
        prescription_lines: list[dict[str, Any]],
        clinical_setting: str = "outpatient",
    ) -> Case:
        """Create and persist a clinical case with child prescription lines."""
        case = Case(
            org_id=org_id,
            patient_age_years=float(patient_context.get("ageYears", 34.0)),
            patient_gender=patient_context.get("gender", "female"),
            patient_is_pregnant=bool(patient_context.get("isPregnant", False)),
            patient_egfr_ml_min=patient_context.get("egfrMlMin"),
            patient_allergies=patient_context.get("allergies", []),
            clinical_setting=clinical_setting,
            indication_code=indication_code,
            status="confirmed",
        )
        self.session.add(case)
        await self.session.flush()

        for line in prescription_lines:
            rx_line = PrescriptionLine(
                case_id=case.id,
                drug_name=line.get("drugName", "Unknown"),
                dose_text=line.get("doseText", ""),
                frequency_text=line.get("frequencyText", ""),
                duration_days=line.get("durationDays"),
            )
            self.session.add(rx_line)

        await self.session.flush()
        return case

    async def get_case_by_id(self, case_id: uuid.UUID) -> Case | None:
        """Retrieve a case with its prescription lines and audit runs loaded."""
        stmt = (
            select(Case)
            .where(Case.id == case_id)
            .options(
                selectinload(Case.prescription_lines),
                selectinload(Case.audit_runs).selectinload(AuditRun.findings),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_recent_cases(self, org_id: uuid.UUID, limit: int = 10) -> list[Case]:
        """List most recent cases for an organization."""
        stmt = (
            select(Case)
            .where(Case.org_id == org_id)
            .order_by(desc(Case.created_at))
            .limit(limit)
            .options(selectinload(Case.prescription_lines))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def record_audit_run(
        self,
        case_id: uuid.UUID,
        overall_status: str,
        rule_set_version: str,
        findings: list[dict[str, Any]],
    ) -> AuditRun:
        """Record an immutable deterministic audit run and its findings."""
        audit_run = AuditRun(
            case_id=case_id,
            overall_status=overall_status,
            rule_set_version=rule_set_version,
        )
        self.session.add(audit_run)
        await self.session.flush()

        for f in findings:
            finding = AuditFinding(
                audit_run_id=audit_run.id,
                rule_id=f.get("rule_id", "UNKNOWN"),
                severity=f.get("severity", "NEEDS_REVIEW"),
                category=f.get("category", "CLINICAL_SAFETY"),
                message=f.get("message", ""),
                evidence_text=f.get("evidence_text"),
            )
            self.session.add(finding)

        await self.session.flush()
        return audit_run
