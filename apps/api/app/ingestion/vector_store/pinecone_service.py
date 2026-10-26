import json

from app.ingestion.vector_store.pinecone_store import VectorStore
from app.ingestion.schemas import DocumentChunk, VectorSearchResult
from pinecone import Pinecone
from app.core.config import settings


class PineconeService(VectorStore):

    def __init__(self):
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index = self.pc.Index(settings.index_name)

    def upsert_chunks(
        self,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        vectors_to_upsert = []
        if len(chunks)!=len(embeddings):
            raise ValueError(
                "The chunk and embedding lengths afre not equal"
            )
        for chunk, embedding in zip(chunks, embeddings):
            vectors_to_upsert.append(
                {
                    "id": chunk.chunk_id,
                    "values": embedding,
                    "metadata": {
                        "text": chunk.text,
                        "tenant_id": chunk.tenant_id,
                        "document_id": chunk.document_id,
                        "section":chunk.section,
                        "page_number":chunk.page_number
                    },
                }
            )

        response= self.index.upsert(vectors=vectors_to_upsert)

        return json.dumps({
            "upserted_count":response.upserted_count
        }) 

    def search(
        self,
        query_embedding: list[float],
        tenant_id: str,
        top_k: int,
    ) -> list[VectorSearchResult]: ...
