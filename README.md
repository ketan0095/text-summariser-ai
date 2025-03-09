# Text Summarizer AI

An intelligent text summarization tool that uses AI to create concise and accurate summaries of various document types. Built with FastAPI, Next.js, and Ollama's Phi-4 model.

## Features

- Support for multiple document formats:
  - PDF documents
  - DOCX files
  - Audio files (with speech-to-text)
  - YouTube videos
- AI-powered summarization using Ollama's Phi-4 model
- Adjustable summary length and language settings
- Export summaries in PDF or text format
- Modern, responsive web interface
- Real-time processing feedback

## Tech Stack

### Backend
- FastAPI (Python web framework)
- Ollama (AI model integration)
- PyPDF2 (PDF processing)
- python-docx (DOCX processing)
- SpeechRecognition & pydub (Audio processing)
- pytube (YouTube video processing)

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- React Hook Form

## Prerequisites

1. Python 3.11 or higher
2. Node.js 18 or higher
3. Ollama installed and running locally

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ketan0095/text-summariser-ai.git
cd text-summariser-ai
```

2. Set up the backend:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama and download the Phi model
curl -fsSL https://ollama.com/install.sh | sh
ollama pull phi
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Create environment files:

Backend (.env):
```env
AI_MODEL_NAME=phi
AI_MAX_LENGTH=500
AI_MIN_LENGTH=100
AI_TEMPERATURE=0.7
AI_TOP_P=0.9
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1
OLLAMA_HOST=http://localhost:11434
```

Frontend (.env.local):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running the Application

1. Start the backend:
```bash
# From the root directory
python main.py
```

2. Start the frontend:
```bash
# From the frontend directory
npm run dev
```

3. Access the application at http://localhost:3000

## Usage

1. Select the document type (PDF, DOCX, Audio, or YouTube)
2. Upload a file or enter a YouTube URL
3. Configure summarization parameters:
   - Minimum length
   - Maximum length
   - Language
   - Export format
4. Click "Generate Summary"
5. View the generated summary and download in your preferred format

## Docker Support

Build and run using Docker:

```bash
docker build -t text-summarizer .
docker run -p 8000:8000 text-summarizer
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 