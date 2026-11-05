"""Prescription line domain schemas."""

from pydantic import BaseModel, ConfigDict, Field


class PrescriptionLine(BaseModel):
    """Structured prescription line entered or confirmed by clinician."""
    model_config = ConfigDict(populate_by_name=True)

    drug_name: str = Field(..., min_length=2, max_length=120, alias="drugName", description="Canonical or generic drug name")
    dose_text: str = Field(..., min_length=1, max_length=100, alias="doseText", description="Dose description (e.g. 500 mg)")
    frequency_text: str = Field("Once daily", min_length=1, max_length=100, alias="frequencyText", description="Administration frequency (e.g. BD, TID, Q8H)")
    duration_days: int | None = Field(None, ge=1, le=180, alias="durationDays", description="Prescribed duration in days")
    route: str = Field("oral", description="Administration route: oral, iv, im, topical")
