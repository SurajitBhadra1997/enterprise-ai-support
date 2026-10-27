from typing import Literal
import uuid

from app.ingestion.review.review_queue import ReviewQueue
from app.ingestion.schemas import DocumentChunk, DocumentReviewRecord


class ReviewService(ReviewQueue):
    def __init__(self):
        self.chunk_records: dict[tuple[str, str], list[DocumentChunk]] = {}
        self.review_records: list[DocumentReviewRecord] = []

    def submit_for_review(
        self,
        document_id: str,
        tenant_id: str,
        reason: str,
    ) -> DocumentReviewRecord:
        review_details = DocumentReviewRecord(
            review_id=str(uuid.uuid4()),
            document_id=document_id,
            tenant_id=tenant_id,
            status="pending",
            reason=reason,
            reviewer_id=None,
            decision_notes=None,
        )
        self.review_records.append(review_details)
        return review_details

    def get_review_status(
        self,
        document_id: str,
        tenant_id: str,
    ) -> DocumentReviewRecord | None:

        filter_iter = filter(
            lambda x: x.tenant_id == tenant_id and x.document_id == document_id,
            self.review_records,
        )

        review_record = [p for p in filter_iter]

        if len(review_record) == 0:
            return None
        else:
            return review_record[-1]

    def record_decision(
        self,
        review_id: str,
        tenant_id: str,
        reviewer_id: str,
        decision: Literal["approved", "rejected"],
        decision_notes: str | None = None,
    ) -> DocumentReviewRecord:
        filtered_list = [
            x
            for x in self.review_records
            if x.review_id == review_id and x.tenant_id == tenant_id
        ]

        review_record = filtered_list[0] if filtered_list else None

        if review_record is None:
            raise ValueError("Review Does not exists")
        else:
            if review_record.status == "pending":
                review_record.status = decision
                review_record.reviewer_id = reviewer_id
                review_record.decision_notes = decision_notes
            else:
                raise ValueError("The review is already processed")
        return review_record

    def store_pending_context(
        self, review_id: str, tenant_id: str, chunk: list[DocumentChunk]
    ) -> None:
        self.chunk_records[(review_id, tenant_id)] = chunk

    def get_pending_context(
        self, review_id: str, tenant_id: str
    ) -> list[DocumentChunk] | None:
        return self.chunk_records.get((review_id, tenant_id))

    def remove_pending_context(self, review_id: str, tenant_id: str) -> None:
        self.chunk_records.pop((review_id, tenant_id), None)

    def get_review_by_id(
        self, review_id: str, tenant_id: str
    ) -> DocumentReviewRecord | None:

        reviewExists = [
            x
            for x in self.review_records
            if x.review_id == review_id and x.tenant_id == tenant_id
        ]

        return reviewExists[-1] if len(reviewExists) > 0 else None
