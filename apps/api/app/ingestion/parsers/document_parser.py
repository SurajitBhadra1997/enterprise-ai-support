from pathlib import Path

from app.ingestion.schemas import ParsedDocument, ParsedSection

from docling.document_converter import DocumentConverter

from docling.chunking import HybridChunker

from uuid import uuid4


class DocumentParser:

    def parse(
        self,
        file_path: Path,
        document_id: str,
        tenant_id: str,
    ) -> ParsedDocument:

        converter = DocumentConverter()

        result = converter.convert(file_path)

        converted_doc = result.document

        chunker = HybridChunker(max_tokens=512)

        parsedsectionlist: list[ParsedSection] = []
        extracted_text_parts: list[str] = []

        for chunk in chunker.chunk(dl_doc=converted_doc):

            raw_text = chunk.text

            enriched_text = chunker.contextualize(chunk=chunk)

            heading_path = chunk.meta.headings or []

            heading = " > ".join(heading_path)

            page_numbers = [
                provenance.page_no
                for item in chunk.meta.doc_items
                for provenance in item.prov
                if provenance.page_no is not None
            ]

            parsedsection = ParsedSection(
                heading=heading,
                text=enriched_text,
                page_number=page_numbers[0] if page_numbers else None,
                section_path=f"{document_id} > {heading}",
            )

            parsedsectionlist.append(parsedsection)
            extracted_text_parts.append(raw_text)

        return ParsedDocument(
            parsing_id=str(uuid4()),
            document_id=document_id,
            tenant_id=tenant_id,
            sections=parsedsectionlist,
            extracted_text="\n\n".join(extracted_text_parts),
        )
