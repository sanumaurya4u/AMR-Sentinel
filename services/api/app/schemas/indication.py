"""Clinical indication schemas."""
from typing import Literal

from pydantic import BaseModel, Field


class ClinicalIndication(BaseModel):
    """Clinical indication and care setting."""
    code: str = Field(..., description="Canonical condition code, e.g. SYN_CAP_MILD")
    setting: Literal["outpatient", "inpatient"] = Field("outpatient", description="Care setting")
