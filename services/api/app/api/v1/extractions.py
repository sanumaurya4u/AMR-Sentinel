"""Prescription document intake extraction endpoint."""
from app.extraction.adapter import ExtractionAdapter
from fastapi import APIRouter, File, HTTPException, UploadFile, status

router = APIRouter(tags=["Extractions"])
adapter = ExtractionAdapter()

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
    "text/plain",
}
MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB limit


@router.post(
    "/extractions",
    summary="Extract editable draft prescription fields from uploaded synthetic document",
)
async def extract_prescription(file: UploadFile = File(...)):  # noqa: B008
    """Accepts uploaded prescription image/PDF and returns editable confidence-rated fields.

    SAFETY MANDATE:
    1. Returns a draft only.
    2. NEVER triggers an audit.
    3. Low confidence or extraction failure does not block manual entry.
    """
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{file.content_type}'. Supported formats: PDF, JPEG, PNG, WebP.",
        )

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of {MAX_FILE_BYTES // (1024*1024)} MB.",
        )

    try:
        draft = await adapter.extract_from_bytes(
            file_bytes=file_bytes,
            mime_type=file.content_type,
            filename=file.filename or "prescription.pdf",
        )
        return draft
    except Exception as e:  # noqa: BLE001
        # Fall back safely: never crash or block the user
        return {
            "error": "Automated extraction unavailable",
            "detail": str(e),
            "fallback": "Please enter clinical parameters manually in the case intake form.",
            "patientContext": {
                "ageYears": 34.0,
                "gender": "male",
                "isPregnant": False,
                "egfrMlMin": None,
                "allergies": [],
            },
            "indicationCode": "SYN_CAP_MILD",
            "setting": "outpatient",
            "prescriptionLines": [],
            "fieldConfidence": {},
            "clinical_status": "MANUAL_ENTRY_REQUIRED",
        }
