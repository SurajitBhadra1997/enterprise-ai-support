from uuid import uuid4

from app.ingestion.schemas import DocumentChunk, ParsedDocument


class ChunkingStrategy:

    def chunk(
        self,
        document: ParsedDocument,
    ) -> list[DocumentChunk]:
        chunks:list[DocumentChunk]=[]

        for section in document.sections:
            chunks.append(
                DocumentChunk(
                    chunk_id=str(uuid4()),
                    text=section.text,
                    section=section.section_path,
                    page_number=section.page_number,
                    tenant_id=document.tenant_id,
                    document_id=document.document_id,
                )
            )
        return chunks
