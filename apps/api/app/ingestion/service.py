from pathlib import Path

from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.schemas import IngestionResult


class IngestionService:

    def __init__(
        self,
        pipeline: IngestionPipeline,
    ) -> None:
        self.pipeline = pipeline

    def ingest_document(
        self,
        file_path: Path,
        document_id: str,
        tenant_id: str,
    ) -> IngestionResult:
        return self.pipeline.process(file_path, document_id, tenant_id)
