from abc import ABC, abstractmethod
from typing import Literal

from app.ingestion.schemas import DocumentReviewRecord


class ReviewQueue(ABC):

    @abstractmethod
    def submit_for_review(
        self,
        document_id: str,
        tenant_id: str,
        reason: str,
    ) -> DocumentReviewRecord:
        ...

    @abstractmethod
    def get_review_status(
        self,
        document_id: str,
        tenant_id: str,
    ) -> DocumentReviewRecord | None:
        ...

    @abstractmethod
    def record_decision(
        self,
        review_id: str,
        tenant_id: str,
        reviewer_id: str,
        decision: Literal["approved", "rejected"],
        decision_notes: str | None = None,
    ) -> DocumentReviewRecord:
        ...