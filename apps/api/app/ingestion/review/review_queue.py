from abc import ABC, abstractmethod
from typing import Literal

from app.ingestion.schemas import DocumentChunk, DocumentReviewRecord


class ReviewQueue(ABC):

    @abstractmethod
    def submit_for_review(
        self,
        document_id: str,
        tenant_id: str,
        reason: str,
    ) -> DocumentReviewRecord: ...

    @abstractmethod
    def get_review_status(
        self,
        document_id: str,
        tenant_id: str,
    ) -> DocumentReviewRecord | None: ...

    @abstractmethod
    def record_decision(
        self,
        review_id: str,
        tenant_id: str,
        reviewer_id: str,
        decision: Literal["approved", "rejected"],
        decision_notes: str | None = None,
    ) -> DocumentReviewRecord: ...

    def store_pending_context(
        review_id: str, tenant_id: str, chunk: list[DocumentChunk]
    ): ...

    def get_pending_context(
        self, review_id: str, tenant_id: str
    ) -> list[DocumentChunk] | None: ...

    def remove_pending_context(self, review_id: str, tenant_id: str) -> None: ...

    def get_review_by_id(
        self, review_id: str, tenant_id: str
    ) -> DocumentReviewRecord | None: ...
