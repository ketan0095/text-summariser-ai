from pydantic import BaseModel, HttpUrl
from enum import Enum
from typing import Optional
from fastapi import UploadFile, File
from datetime import datetime

class DocumentType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    AUDIO = "audio"
    YOUTUBE = "youtube"
    TEXT = "text"

class ExportFormat(str, Enum):
    PDF = "pdf"
    TEXT = "text"

class SummarizationRequest(BaseModel):
    document_type: DocumentType
    url: Optional[HttpUrl] = None
    max_length: Optional[int] = 500
    min_length: Optional[int] = 100
    language: Optional[str] = "en"
    export_format: Optional[ExportFormat] = ExportFormat.PDF

class SummarizationResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    processing_time: float
    document_type: DocumentType
    export_url: Optional[str] = None  # URL to download the exported file
    timestamp: datetime = datetime.now() 