from pytube import YouTube
import os
import tempfile
from models.summarization_request import SummarizationRequest
from . import audio_summarizer

async def summarize(request: SummarizationRequest) -> str:
    try:
        # Download YouTube video
        yt = YouTube(str(request.url))
        
        # Get audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download audio
            audio_path = audio_stream.download(output_path=temp_dir)
            
            # Read the audio file
            with open(audio_path, 'rb') as audio_file:
                audio_content = audio_file.read()
            
            # Create a new request for audio summarization
            audio_request = SummarizationRequest(
                content=audio_content,
                document_type="audio",
                max_length=request.max_length,
                min_length=request.min_length,
                language=request.language
            )
            
            # Use audio summarizer to process the content
            return await audio_summarizer.summarize(audio_request)
            
    except Exception as e:
        raise Exception(f"Error processing YouTube video: {str(e)}") 