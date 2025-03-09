import base64
import io
from docx import Document
from models.summarization_request import SummarizationRequest
from .model_config import model_service

async def summarize(request: SummarizationRequest) -> str:
    try:
        # Decode base64 content
        docx_content = base64.b64decode(request.content)
        docx_file = io.BytesIO(docx_content)
        
        # Read DOCX
        doc = Document(docx_file)
        text = ""
        
        # Extract text from all paragraphs
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
            
        # Generate summary using the model service
        return await model_service.generate_summary(
            text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
    except Exception as e:
        raise Exception(f"Error processing DOCX: {str(e)}") 