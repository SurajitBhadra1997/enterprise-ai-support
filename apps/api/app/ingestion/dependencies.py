from fastapi import Depends

from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.service import IngestionService
from app.ingestion.parsers.document_parser import DocumentParser
from app.ingestion.chunking.strategies import ChunkingStrategy
from app.ingestion.pii.detector import PIIDetector
from app.ingestion.embeddings.sentence_transformer_service import (
    SentenceTransformerService,
)
from app.ingestion.vector_store.pinecone_service import PineconeService
from app.ingestion.review.review_service import ReviewService
from app.ingestion.review.review_processing_service import ReviewProcessingService

review_service = ReviewService()


def get_ingestion_pipeline() -> IngestionPipeline:
    return IngestionPipeline(
        parser=DocumentParser(),
        chunker=ChunkingStrategy(),
        pii_detector=PIIDetector(),
        embedding_service=SentenceTransformerService(),
        vector_store=PineconeService(),
        review_queue=review_service,
    )


def get_document_parser() -> DocumentParser:
    return DocumentParser()


def get_ingestion_service(
    pipeline: IngestionPipeline = Depends(get_ingestion_pipeline),
) -> IngestionService:
    return IngestionService(pipeline)


def get_review_processing_service() -> ReviewProcessingService:
    return ReviewProcessingService(
        review_service=review_service,
        embedding_service=SentenceTransformerService(),
        vector_store=PineconeService(),
    )
