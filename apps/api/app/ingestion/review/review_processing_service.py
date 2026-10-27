from app.ingestion.embeddings.embedding_service import EmbeddingService
from app.ingestion.vector_store.pinecone_store import VectorStore
from app.ingestion.review.review_service import ReviewService


class ReviewProcessingService:
    def __init__(
        self,
        review_service: ReviewService,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self.review_service = review_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def approve_and_process(
        self,
        review_id: str,
        tenant_id: str,
        reviewer_id: str,
        decision_notes: str | None = None,
    ) -> bool:

        validate_review_record = self.review_service.get_review_by_id(
            review_id, tenant_id
        )

        if validate_review_record is None:
            raise ValueError("Review does not exists")

        if validate_review_record.status == "rejected":
            raise ValueError("Review is already rejected")

        if validate_review_record.status == "pending":
            self.review_service.record_decision(
                review_id, tenant_id, reviewer_id, "approved", decision_notes
            )

        pending_context = self.review_service.get_pending_context(review_id, tenant_id)

        if pending_context is None:
            raise ValueError("No chunk is associate with this review")

        embedded_docs = self.embedding_service.embed_documents(
            [chunk.text for chunk in pending_context]
        )

        if len(embedded_docs) != len(pending_context):
            raise ValueError("Chunk and embedding size are not equal")

        self.vector_store.upsert_chunks(pending_context, embedded_docs)

        self.review_service.remove_pending_context(review_id, tenant_id)

        return True

    def reject_review(
        self,
        review_id: str,
        tenant_id: str,
        reviewer_id: str,
        decision_notes: str | None = None,
    ) -> bool:

        validate_review_record = self.review_service.get_review_by_id(
            review_id, tenant_id
        )

        if validate_review_record is None:
            raise ValueError("Review does not exists")

        if validate_review_record.status != "pending":
            raise ValueError("Review is not pending")

        if validate_review_record.status == "pending":
            self.review_service.record_decision(
                review_id, tenant_id, reviewer_id, "rejected", decision_notes
            )

        self.review_service.remove_pending_context(review_id, tenant_id)

        return True
