"""
FastAPI Backend for Soros Chatbot
Provides REST API endpoints for the React frontend
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
import logging

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Import configuration
sys.path.append(str(Path(__file__).parent.parent))
from config import Config

from src.soros_chatbot import SorosChatbot
from src.pdf_reader import PDFReader
from src.soros_knowledge_base import SorosKnowledgeBase

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Soros Chatbot API",
    description="API for the Soros Chatbot with PDF processing capabilities",
    version="1.0.0"
)

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://localhost:{Config.FRONTEND_PORT}",
        f"http://127.0.0.1:{Config.FRONTEND_PORT}",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chatbot instance
chatbot: Optional[SorosChatbot] = None

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    use_context: bool = True

class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None

class SystemStatsResponse(BaseModel):
    loaded_pdfs: int
    total_quotes: int
    total_concepts: int
    conversation_messages: int

class PDFInfoResponse(BaseModel):
    path: str
    word_count: int
    chunks: int
    quotes_extracted: int
    concepts_found: int

class ConceptSearchResponse(BaseModel):
    concept: str
    definition: str
    key_points: List[str]

class UploadResponse(BaseModel):
    success: bool
    filename: str
    word_count: int
    quotes_extracted: int
    concepts_found: int
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize the chatbot on startup"""
    global chatbot
    
    try:
        # Validate configuration
        Config.validate()
        logger.info("Configuration validated successfully")
        
        # Initialize chatbot with configuration
        chatbot = SorosChatbot(
            api_key=Config.OPENAI_API_KEY,
            model=Config.OPENAI_MODEL
        )
        logger.info("Soros Chatbot initialized successfully")
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please check your .env file and ensure OPENAI_API_KEY is set")
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Soros Chatbot API", 
        "status": "running",
        "version": "1.0.0",
        "model": Config.OPENAI_MODEL
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "chatbot_available": chatbot is not None,
        "api_key_set": bool(Config.OPENAI_API_KEY),
        "model": Config.OPENAI_MODEL,
        "temperature": Config.OPENAI_TEMPERATURE
    }

@app.get("/config")
async def get_config():
    """Get current configuration (without sensitive data)"""
    return {
        "model": Config.OPENAI_MODEL,
        "temperature": Config.OPENAI_TEMPERATURE,
        "max_tokens": Config.OPENAI_MAX_TOKENS,
        "api_host": Config.API_HOST,
        "api_port": Config.API_PORT,
        "frontend_port": Config.FRONTEND_PORT,
        "debug": Config.DEBUG,
        "log_level": Config.LOG_LEVEL
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the Soros chatbot"""
    if not chatbot:
        raise HTTPException(
            status_code=503, 
            detail="Chatbot not available. Check your .env file and ensure OPENAI_API_KEY is set."
        )
    
    try:
        response = chatbot.chat(request.message, use_context=request.use_context)
        return ChatResponse(response=response, success=True)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return ChatResponse(
            response="I apologize, but I'm experiencing some difficulties.",
            success=False,
            error=str(e)
        )

@app.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats():
    """Get system statistics"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not available")
    
    stats = chatbot.get_system_stats()
    return SystemStatsResponse(**stats)

@app.get("/pdfs", response_model=List[PDFInfoResponse])
async def get_loaded_pdfs():
    """Get information about loaded PDFs"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not available")
    
    pdf_info = chatbot.get_loaded_pdfs_info()
    return [PDFInfoResponse(**info) for info in pdf_info]

@app.post("/upload-pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not available")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Process PDF
        result = chatbot.load_pdf(tmp_path)
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        if result['success']:
            return UploadResponse(
                success=True,
                filename=file.filename,
                word_count=result['pdf_data']['word_count'],
                quotes_extracted=len(result['extracted_content']['quotes']),
                concepts_found=len(result['extracted_content']['concepts'])
            )
        else:
            return UploadResponse(
                success=False,
                filename=file.filename,
                word_count=0,
                quotes_extracted=0,
                concepts_found=0,
                error=result.get('error', 'Unknown error')
            )
    
    except Exception as e:
        logger.error(f"PDF upload error: {e}")
        return UploadResponse(
            success=False,
            filename=file.filename,
            word_count=0,
            quotes_extracted=0,
            concepts_found=0,
            error=str(e)
        )

@app.get("/search-concepts")
async def search_concepts(query: str):
    """Search for concepts in the knowledge base"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not available")
    
    try:
        results = chatbot.search_knowledge_base(query)
        return {
            "success": True,
            "results": [
                {
                    "concept": result['concept'],
                    "definition": result['data']['definition'],
                    "key_points": result['data']['key_points']
                }
                for result in results
            ]
        }
    except Exception as e:
        logger.error(f"Concept search error: {e}")
        return {"success": False, "error": str(e), "results": []}

@app.get("/random-quote")
async def get_random_quote():
    """Get a random Soros quote"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not available")
    
    try:
        quote = chatbot.get_random_quote()
        return {"success": True, "quote": quote}
    except Exception as e:
        logger.error(f"Quote generation error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/add-quote")
async def add_custom_quote(quote: str = Form(...)):
    """Add a custom quote to the knowledge base"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not available")
    
    try:
        chatbot.add_custom_quote(quote)
        return {"success": True, "message": "Quote added successfully"}
    except Exception as e:
        logger.error(f"Add quote error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/add-concept")
async def add_custom_concept(
    concept_name: str = Form(...),
    definition: str = Form(...),
    key_points: str = Form(...)
):
    """Add a custom concept to the knowledge base"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not available")
    
    try:
        # Parse key points (comma-separated)
        points = [point.strip() for point in key_points.split(',') if point.strip()]
        chatbot.add_custom_concept(concept_name, definition, points)
        return {"success": True, "message": "Concept added successfully"}
    except Exception as e:
        logger.error(f"Add concept error: {e}")
        return {"success": False, "error": str(e)}

@app.delete("/clear-memory")
async def clear_conversation_memory():
    """Clear the conversation memory"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not available")
    
    try:
        chatbot.clear_memory()
        return {"success": True, "message": "Memory cleared successfully"}
    except Exception as e:
        logger.error(f"Clear memory error: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Create .env file if it doesn't exist
    from config import create_env_file
    create_env_file()
    
    # Print configuration
    Config.print_config()
    
    # Start the server
    uvicorn.run(
        app, 
        host=Config.API_HOST, 
        port=Config.API_PORT,
        log_level=Config.LOG_LEVEL.lower()
    ) 