from typing import Literal

from pydantic import BaseModel

from app.ingestion.schemas import ConflictCheckResult, DocumentChunk


class ConflictChecker:

    def check(
        self,
        document_id: str,
        tenant_id: str,
        chunks: list[DocumentChunk],
    ) -> ConflictCheckResult:
        ...