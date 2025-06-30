# 🤖 Soros Chatbot

A sophisticated AI chatbot that speaks like George Soros, built with PDF processing capabilities, a comprehensive knowledge base, and a modern React frontend.

## 🌟 Features

- **Soros-Style Conversations**: Chat with an AI that mimics George Soros's philosophical and economic thinking
- **PDF Processing**: Upload and analyze PDF documents to extract knowledge
- **Knowledge Base**: Built-in knowledge of Soros's key concepts (reflexivity, open society, etc.)
- **Modern Web Interface**: Beautiful React frontend with real-time chat
- **REST API**: FastAPI backend with comprehensive endpoints
- **CLI Interface**: Command-line interface for testing and development
- **Configuration Management**: Easy setup with .env file support

## 🏗️ Architecture

```
stockpredictionmodel/
├── api/                 # FastAPI backend
│   └── main.py         # API endpoints
├── frontend/           # React frontend
│   ├── src/
│   │   ├── components/ # React components
│   │   └── App.js      # Main app
│   └── package.json    # Frontend dependencies
├── src/                # Core Python modules
│   ├── soros_chatbot.py      # Main chatbot logic
│   ├── pdf_reader.py         # PDF processing
│   └── soros_knowledge_base.py # Knowledge base
├── data/               # Data storage
│   └── soros/          # Soros knowledge data
├── config.py           # Configuration management
├── cli.py              # Command-line interface
├── demo.py             # Demo script
├── start.sh            # Startup script
└── .env                # Environment variables (auto-created)
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd stockpredictionmodel
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 3. Configure API Key

The system will automatically create a `.env` file on first run. Edit it to add your OpenAI API key:

```bash
# The .env file will be created automatically with this structure:
OPENAI_API_KEY=your-actual-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=1000
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_PORT=3000
DEBUG=true
LOG_LEVEL=INFO
```

**Get an API key from:** https://platform.openai.com/api-keys

### 4. Start the Application

```bash
# Start both backend and frontend
./start.sh

# Or start components individually:
# Backend only
python api/main.py

# Frontend only
cd frontend && npm start

# CLI only
python cli.py
```

### 5. Access the Application

- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Configuration**: http://localhost:8000/config
- **Health Check**: http://localhost:8000/health

## 📚 Usage

### Web Interface

1. **Chat**: Start conversations with the Soros chatbot
2. **Upload PDFs**: Drag and drop PDF files for analysis
3. **Search Knowledge**: Browse Soros's concepts and quotes
4. **View Stats**: Monitor system performance and loaded content

### Command Line Interface

```bash
# Interactive chat
python cli.py

# Test PDF functionality
python cli.py --test-pdf

# Test knowledge base
python cli.py --test-kb

# Setup environment
python cli.py --setup
```

### API Endpoints

- `POST /chat` - Send messages to the chatbot
- `POST /upload-pdf` - Upload and process PDF files
- `GET /stats` - Get system statistics
- `GET /pdfs` - List loaded PDFs
- `GET /search-concepts` - Search knowledge base
- `GET /random-quote` - Get random Soros quote
- `POST /add-quote` - Add custom quotes
- `POST /add-concept` - Add custom concepts
- `DELETE /clear-memory` - Clear conversation memory

## 🔧 Configuration

### Environment Variables

The system uses a `.env` file for configuration. Key settings:

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `OPENAI_MODEL` - AI model to use (default: gpt-3.5-turbo)
- `OPENAI_TEMPERATURE` - Response creativity (0.0-1.0)
- `OPENAI_MAX_TOKENS` - Maximum response length
- `API_PORT` - Backend port (default: 8000)
- `FRONTEND_PORT` - Frontend port (default: 3000)

### Configuration Management

```bash
# View current configuration
python config.py

# Create .env file
python cli.py --setup
```

## 🧠 Knowledge Base

The system includes a comprehensive knowledge base of George Soros's key concepts:

- **Reflexivity**: The feedback loop between perception and reality
- **Open Society**: Democratic governance and human rights
- **Market Regulation**: Financial market oversight
- **Philanthropy**: Social responsibility and giving
- **Globalization**: International cooperation and trade

### Adding Custom Knowledge

```bash
# Add custom quote via API
curl -X POST "http://localhost:8000/add-quote" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "quote=Your custom quote here"

# Add custom concept via API
curl -X POST "http://localhost:8000/add-concept" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "concept_name=Your Concept&definition=Definition here&key_points=Point 1,Point 2,Point 3"
```

## 📄 PDF Processing

The system can process PDF documents to extract:

- Text content and metadata
- Key quotes and concepts
- Structured knowledge chunks
- Document statistics

### Supported PDF Features

- Multiple PDF libraries (PyPDF2, pdfplumber, PyMuPDF)
- Text extraction and cleaning
- Metadata extraction
- Chunking for AI processing
- Quote and concept identification

## 🛠️ Development

### Project Structure

- `src/soros_chatbot.py` - Main chatbot implementation
- `src/pdf_reader.py` - PDF processing utilities
- `src/soros_knowledge_base.py` - Knowledge base management
- `api/main.py` - FastAPI backend
- `frontend/src/` - React frontend components
- `config.py` - Configuration management

### Testing

```bash
# Run demo
python demo.py

# Test individual components
python cli.py --test-pdf
python cli.py --test-kb

# Check configuration
python config.py
```

### Adding Features

1. **New Knowledge**: Add to `data/soros/soros_knowledge.json`
2. **New Endpoints**: Add to `api/main.py`
3. **New UI Components**: Add to `frontend/src/components/`
4. **New PDF Processing**: Extend `src/pdf_reader.py`

## 🔍 Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```bash
   # Check .env file exists and has correct API key
   cat .env
   # Edit if needed
   nano .env
   ```

2. **Port Already in Use**
   ```bash
   # Change ports in .env file
   API_PORT=8001
   FRONTEND_PORT=3001
   ```

3. **PDF Processing Errors**
   ```bash
   # Test PDF functionality
   python cli.py --test-pdf
   ```

4. **Frontend Build Issues**
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Debug Mode

Enable debug mode in `.env`:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

### Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check configuration
curl http://localhost:8000/config
```

## 📝 License

This project is for educational and research purposes. Please respect OpenAI's terms of service and George Soros's intellectual property.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Test with the demo script
4. Check configuration with `python config.py`

---

**Note**: This chatbot is designed to mimic George Soros's style and knowledge for educational purposes. It does not represent actual financial advice or George Soros's current views.