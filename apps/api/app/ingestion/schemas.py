from pathlib import Path
from typing import Literal

from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    document_id: str
    tenant_id: str
    filename: str
    document_type: str
    version: str


class ParsedSection(BaseModel):
    heading: str
    text: str
    page_number: int | None = None
    section_path: str


class ParsedDocument(BaseModel):
    parsing_id: str
    document_id: str
    tenant_id: str
    sections: list[ParsedSection]
    extracted_text: str


class DocumentChunk(BaseModel):
    chunk_id: str
    text: str
    section: str
    page_number: int | None = None
    tenant_id: str
    document_id: str


class VectorSearchResult(BaseModel):
    chunk: DocumentChunk
    score: float


class IngestionResult(BaseModel):
    review_requirement: bool
    failure_message: str | None = None
    review_ids: list[str] | None = None
    chunks_under_review: list[DocumentChunk]
    chunks_successfully_indexed: list[DocumentChunk]


class PIIDetectionResult(BaseModel):
    contains_pii: bool
    detected_categories: list[str]
    requires_review: bool


class ConflictChunks(BaseModel):
    exisitng_approved_chunk: list[DocumentChunk]
    conflicitng_chunk: list[DocumentChunk]


class ConflictCheckResult(BaseModel):
    status: Literal["clear", "duplicate", "conflict", "review_required"]
    chunks_under_review: list[ConflictChunks]
    chunks_clear: list[DocumentChunk]
    conflicting_document_ids: list[str]
    explanation: str | None = None


class DocumentReviewRecord(BaseModel):
    review_id: str
    document_id: str
    tenant_id: str
    status: Literal["pending", "approved", "rejected"]
    reason: str
    reviewer_id: str | None = None
    decision_notes: str | None = None
    chunk_id: str


class ApprovalRequest(BaseModel):
    review_id: str
    tenant_id: str
    reviewer_id: str
    decision: Literal["approved", "rejected"]
    decision_notes: str | None = None
