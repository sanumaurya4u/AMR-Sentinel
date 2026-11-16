"""Patient context domain schemas."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PatientContext(BaseModel):
    """Confirmed patient demographic and clinical context."""
    model_config = ConfigDict(populate_by_name=True)

    age_years: float = Field(..., ge=0.0, le=125.0, alias="ageYears", description="Patient age in years")
    gender: Literal["female", "male", "other"] = Field("other", description="Biological gender")
    is_pregnant: bool = Field(False, alias="isPregnant", description="Whether patient is documented as currently pregnant")
    egfr_ml_min: float | None = Field(None, ge=0.0, le=250.0, alias="egfrMlMin", description="Estimated GFR in mL/min/1.73m²")
    weight_kg: float | None = Field(None, ge=0.5, le=300.0, alias="weightKg", description="Patient weight in kg (critical for pediatric dosing)")
    allergies: list[str] = Field(default_factory=list, description="List of documented drug allergies")
