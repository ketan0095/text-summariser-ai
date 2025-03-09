import base64
import io
import speech_recognition as sr
from pydub import AudioSegment
from models.summarization_request import SummarizationRequest
from .model_config import model_service

async def summarize(request: SummarizationRequest) -> str:
    try:
        # Decode base64 content
        audio_content = base64.b64decode(request.content)
        audio_file = io.BytesIO(audio_content)
        
        # Convert audio to WAV format
        audio = AudioSegment.from_file(audio_file)
        wav_file = io.BytesIO()
        audio.export(wav_file, format="wav")
        wav_file.seek(0)
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Convert audio to text
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=request.language)
            
        # Generate summary using the model service
        return await model_service.generate_summary(
            text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        
    except Exception as e:
        raise Exception(f"Error processing audio: {str(e)}") 