from app.ingestion.embeddings.embedding_service import EmbeddingService
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class SentenceTransformerService(EmbeddingService):

    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)

    def embed_documents(
        self,
        texts: list[str],
    ):
        return self.model.encode(texts).tolist()

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        return self.model.encode(text).tolist()
