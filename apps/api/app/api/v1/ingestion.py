from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, UploadFile
import tempfile

from app.ingestion.service import IngestionService
from app.ingestion.dependencies import (
    get_ingestion_service,
    get_review_processing_service,
)
from app.ingestion.schemas import ApprovalRequest

from app.ingestion.review.review_processing_service import ReviewProcessingService

router = APIRouter(tags=["Ingestion"])


@router.post("/upload/docs")
async def ingestdocs(
    file: UploadFile = File(...),
    document_id: str = Form(...),
    tenant_id: str = Form(...),
    ingestion: IngestionService = Depends(get_ingestion_service),
):

    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_file:
        content = await file.read()

        temp_file.write(content)

        temp_file.flush()

        result = ingestion.ingest_document(Path(temp_file.name), document_id, tenant_id)

        return result


@router.post("/reviews/{review_id}/decision")
def review_decision(
    request: ApprovalRequest,
    review_processing_service: ReviewProcessingService = Depends(
        get_review_processing_service
    ),
):
    result = (
        review_processing_service.approve_and_process(
            request.review_id,
            request.tenant_id,
            request.reviewer_id,
            request.decision_notes,
        )
        if request.decision == "approved"
        else review_processing_service.reject_review(
            request.review_id,
            request.tenant_id,
            request.reviewer_id,
            request.decision_notes,
        )
    )

    return result
