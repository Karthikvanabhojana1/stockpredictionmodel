"""
PDF Reader Module for Soros Chatbot
Handles PDF text extraction and preprocessing
"""

import os
import logging
from typing import List, Dict, Optional
import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
import re
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFReader:
    """Advanced PDF reader with multiple extraction methods"""
    
    def __init__(self):
        self.extracted_texts = []
        self.metadata = {}
    
    def extract_text_pypdf2(self, pdf_path: str) -> str:
        """Extract text using PyPDF2"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
            return ""
    
    def extract_text_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {e}")
            return ""
    
    def extract_text_pymupdf(self, pdf_path: str) -> str:
        """Extract text using PyMuPDF"""
        try:
            text = ""
            doc = fitz.open(pdf_path)
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            return text
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {e}")
            return ""
    
    def extract_text_combined(self, pdf_path: str) -> str:
        """Combine multiple extraction methods for best results"""
        methods = [
            self.extract_text_pymupdf,
            self.extract_text_pdfplumber,
            self.extract_text_pypdf2
        ]
        
        best_text = ""
        for method in methods:
            try:
                text = method(pdf_path)
                if len(text) > len(best_text):
                    best_text = text
            except Exception as e:
                logger.warning(f"Method {method.__name__} failed: {e}")
                continue
        
        return best_text
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Remove common PDF artifacts
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}\"\']', '', text)
        
        # Fix common OCR issues
        text = text.replace('|', 'I')
        text = text.replace('0', 'O')  # Be careful with this one
        
        return text.strip()
    
    def extract_metadata(self, pdf_path: str) -> Dict:
        """Extract PDF metadata"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                return {
                    'title': metadata.get('/Title', ''),
                    'author': metadata.get('/Author', ''),
                    'subject': metadata.get('/Subject', ''),
                    'creator': metadata.get('/Creator', ''),
                    'producer': metadata.get('/Producer', ''),
                    'pages': len(pdf_reader.pages)
                }
        except Exception as e:
            logger.error(f"Metadata extraction failed: {e}")
            return {}
    
    def read_pdf(self, pdf_path: str) -> Dict:
        """Main method to read PDF and return structured data"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Reading PDF: {pdf_path}")
        
        # Extract text using combined method
        raw_text = self.extract_text_combined(pdf_path)
        cleaned_text = self.clean_text(raw_text)
        
        # Extract metadata
        metadata = self.extract_metadata(pdf_path)
        
        # Split into chunks for processing
        chunks = self.split_into_chunks(cleaned_text)
        
        result = {
            'file_path': pdf_path,
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'metadata': metadata,
            'chunks': chunks,
            'total_chunks': len(chunks),
            'word_count': len(cleaned_text.split())
        }
        
        self.extracted_texts.append(result)
        return result
    
    def split_into_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks for processing"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def read_multiple_pdfs(self, pdf_directory: str) -> List[Dict]:
        """Read multiple PDFs from a directory"""
        pdf_files = []
        for ext in ['*.pdf', '*.PDF']:
            pdf_files.extend(Path(pdf_directory).glob(ext))
        
        results = []
        for pdf_file in pdf_files:
            try:
                result = self.read_pdf(str(pdf_file))
                results.append(result)
                logger.info(f"Successfully processed: {pdf_file.name}")
            except Exception as e:
                logger.error(f"Failed to process {pdf_file.name}: {e}")
        
        return results
    
    def get_all_text(self) -> str:
        """Get all extracted text combined"""
        return "\n\n".join([result['cleaned_text'] for result in self.extracted_texts])
    
    def get_all_chunks(self) -> List[str]:
        """Get all text chunks from all PDFs"""
        all_chunks = []
        for result in self.extracted_texts:
            all_chunks.extend(result['chunks'])
        return all_chunks


if __name__ == "__main__":
    # Example usage
    reader = PDFReader()
    
    # Test with a sample PDF
    # result = reader.read_pdf("path/to/sample.pdf")
    # print(f"Extracted {result['word_count']} words")
    # print(f"Created {result['total_chunks']} chunks") 