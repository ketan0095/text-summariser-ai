from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from models.summarization_request import SummarizationRequest, SummarizationResponse, DocumentType, ExportFormat
from services import pdf_summarizer, docx_summarizer, audio_summarizer, youtube_summarizer
from services.export_service import export_service
import time
import base64
import os

router = APIRouter()

@router.post("/summarize/file", response_model=SummarizationResponse)
async def summarize_file(
    file: UploadFile = File(...),
    document_type: DocumentType = Form(...),
    max_length: int = Form(500),
    min_length: int = Form(100),
    language: str = Form("en"),
    export_format: ExportFormat = Form(ExportFormat.PDF)
):
    start_time = time.time()
    
    try:
        # Read file content
        content = await file.read()
        content_base64 = base64.b64encode(content).decode()

        # Create request object
        request = SummarizationRequest(
            document_type=document_type,
            max_length=max_length,
            min_length=min_length,
            language=language,
            export_format=export_format
        )

        # Process based on document type
        if document_type == DocumentType.PDF:
            summary = await pdf_summarizer.summarize(request, content_base64)
        elif document_type == DocumentType.DOCX:
            summary = await docx_summarizer.summarize(request, content_base64)
        elif document_type == DocumentType.AUDIO:
            summary = await audio_summarizer.summarize(request, content_base64)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Export summary
        export_path = export_service.export_summary(summary, document_type.value, export_format)
        
        processing_time = time.time() - start_time
        
        return SummarizationResponse(
            summary=summary,
            original_length=len(content),
            summary_length=len(summary),
            processing_time=processing_time,
            document_type=document_type,
            export_url=f"/api/v1/download/{export_path.split('/')[-1]}"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize/youtube", response_model=SummarizationResponse)
async def summarize_youtube(
    url: str = Form(...),
    max_length: int = Form(500),
    min_length: int = Form(100),
    language: str = Form("en"),
    export_format: ExportFormat = Form(ExportFormat.PDF)
):
    start_time = time.time()
    
    try:
        request = SummarizationRequest(
            document_type=DocumentType.YOUTUBE,
            url=url,
            max_length=max_length,
            min_length=min_length,
            language=language,
            export_format=export_format
        )

        summary = await youtube_summarizer.summarize(request)
        
        # Export summary
        export_path = export_service.export_summary(summary, DocumentType.YOUTUBE.value, export_format)
        
        processing_time = time.time() - start_time
        
        return SummarizationResponse(
            summary=summary,
            original_length=0,  # YouTube video length could be added here
            summary_length=len(summary),
            processing_time=processing_time,
            document_type=DocumentType.YOUTUBE,
            export_url=f"/api/v1/download/{export_path.split('/')[-1]}"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"exports/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type='application/octet-stream',
        filename=filename
    ) 