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


def get_ingestion_pipeline() -> IngestionPipeline:
    return IngestionPipeline(
        parser=DocumentParser(),
        chunker=ChunkingStrategy(),
        pii_detector=PIIDetector(),
        embedding_service=SentenceTransformerService(),
        vector_store=PineconeService()
    )


def get_document_parser() -> DocumentParser:
    return DocumentParser()


def get_ingestion_service(
    pipeline: IngestionPipeline = Depends(get_ingestion_pipeline),
) -> IngestionService:
    return IngestionService(pipeline)
