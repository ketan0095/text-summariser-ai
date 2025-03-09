FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p exports

# Copy application code
COPY . .

# Set permissions for exports directory
RUN chmod 777 exports

# Expose port
EXPOSE 8000

# Set environment variables
ENV AI_MODEL_NAME=phi \
    AI_MAX_LENGTH=500 \
    AI_MIN_LENGTH=100 \
    AI_TEMPERATURE=0.7 \
    AI_TOP_P=0.9 \
    API_HOST=0.0.0.0 \
    API_PORT=8000 \
    API_WORKERS=1 \
    OLLAMA_HOST=http://localhost:11434

# Download the Phi model
RUN ollama pull phi

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 