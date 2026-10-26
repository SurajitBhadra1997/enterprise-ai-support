from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, UploadFile
import tempfile

from app.ingestion.service import IngestionService
from app.ingestion.dependencies import get_ingestion_service

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
