import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv
import ollama

# Load environment variables
load_dotenv()

class ModelConfig(BaseModel):
    model_name: str
    max_length: int
    min_length: int
    temperature: float
    top_p: float
    system_prompt: str

class ModelService:
    _instance = None
    _model_config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the model configuration with default values or from environment variables"""
        self._model_config = ModelConfig(
            model_name=os.getenv("AI_MODEL_NAME", "phi"),
            max_length=int(os.getenv("AI_MAX_LENGTH", "500")),
            min_length=int(os.getenv("AI_MIN_LENGTH", "100")),
            temperature=float(os.getenv("AI_TEMPERATURE", "0.7")),
            top_p=float(os.getenv("AI_TOP_P", "0.9")),
            system_prompt=os.getenv(
                "AI_SYSTEM_PROMPT",
                "You are a helpful assistant that summarizes text. "
                "Create a concise and accurate summary of the following text."
            )
        )

    @property
    def config(self) -> ModelConfig:
        return self._model_config

    def update_config(self, **kwargs):
        """Update model configuration with new values"""
        current_config = self._model_config.dict()
        current_config.update({k: v for k, v in kwargs.items() if v is not None})
        self._model_config = ModelConfig(**current_config)

    async def generate_summary(self, text: str, max_length: Optional[int] = None, min_length: Optional[int] = None) -> str:
        """Generate a summary using the configured model"""
        try:
            # Prepare the prompt
            prompt = f"{self._model_config.system_prompt}\n\nText: {text}\n\nSummary:"

            # Generate response using Ollama
            response = ollama.generate(
                model=self._model_config.model_name,
                prompt=prompt,
                temperature=self._model_config.temperature,
                top_p=self._model_config.top_p,
                max_length=max_length or self._model_config.max_length,
            )

            return response['response'].strip()

        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

# Create a singleton instance
model_service = ModelService() 