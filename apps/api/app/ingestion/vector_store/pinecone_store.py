from abc import ABC, abstractmethod

from app.ingestion.schemas import DocumentChunk, VectorSearchResult


class VectorStore(ABC):

    @abstractmethod
    def upsert_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        ...

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        tenant_id: str,
        top_k: int,
    ) -> list[VectorSearchResult]:
        ...