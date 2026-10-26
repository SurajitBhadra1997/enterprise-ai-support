from pathlib import Path

from app.ingestion.chunking.strategies import ChunkingStrategy
from app.ingestion.embeddings.embedding_service import EmbeddingService
from app.ingestion.parsers.document_parser import DocumentParser
from app.ingestion.pii.detector import PIIDetector
from app.ingestion.validation.conflict_checker import ConflictChecker
from app.ingestion.vector_store.pinecone_store import VectorStore
from app.ingestion.review.review_queue import ReviewQueue
from app.ingestion.schemas import IngestionResult


class IngestionPipeline:

    def __init__(
        self,
        parser: DocumentParser,
        chunker: ChunkingStrategy,
        pii_detector: PIIDetector,
        # conflict_checker: ConflictChecker,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        # review_queue: ReviewQueue,
    ) -> None:
        self.parser = parser
        self.chunker = chunker
        self.pii_detector = pii_detector
        # self.conflict_checker = conflict_checker
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        # self.review_queue = review_queue

    def process(
        self,
        file_path: Path,
        document_id: str,
        tenant_id: str,
    ) -> IngestionResult:
        parsed_docs = self.parser.parse(file_path, document_id, tenant_id)
        chunked_docs = self.chunker.chunk(parsed_docs)
        pii_detected_entities = self.pii_detector.detect(parsed_docs.extracted_text)

        embedded_docs = self.embedding_service.embed_documents(
            [chunk.text for chunk in chunked_docs]
        )

        upserted_result=self.vector_store.upsert_chunks(chunked_docs, embedded_docs)

        return upserted_result
