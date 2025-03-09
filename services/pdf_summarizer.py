import base64
import io
from PyPDF2 import PdfReader
from models.summarization_request import SummarizationRequest
from .model_config import model_service

async def summarize(request: SummarizationRequest) -> str:
    try:
        # Decode base64 content
        pdf_content = base64.b64decode(request.content)
        pdf_file = io.BytesIO(pdf_content)
        
        # Read PDF
        reader = PdfReader(pdf_file)
        text = ""
        
        # Extract text from all pages
        for page in reader.pages:
            text += page.extract_text()
            
        # Generate summary using the model service
        return await model_service.generate_summary(
            text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}") 