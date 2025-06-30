"""
Soros Chatbot - Main chatbot implementation
Integrates PDF reader, knowledge base, and OpenAI for Soros-style conversations
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from pdf_reader import PDFReader
from soros_knowledge_base import SorosKnowledgeBase

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage, HumanMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SorosChatbot:
    """Main Soros chatbot class"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """Initialize the Soros chatbot"""
        self.api_key = api_key
        
        # Initialize components
        self.pdf_reader = PDFReader()
        self.knowledge_base = SorosKnowledgeBase()
        
        # Initialize language model
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.7,
            max_tokens=1000,
            openai_api_key=self.api_key
        )
        
        # Conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
        
        # Loaded PDFs
        self.loaded_pdfs = []
        
        # System prompt for Soros personality
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for Soros personality"""
        style_guide = self.knowledge_base.get_writing_style_guide()
        
        prompt = f"""You are George Soros, the renowned investor, philanthropist, and philosopher. 

PERSONALITY TRAITS:
- You are philosophical, analytical, and often critical of market fundamentalism
- You think globally and long-term about systemic issues
- You believe in the theory of reflexivity: that market participants' perceptions can influence market fundamentals
- You advocate for open societies with democratic governance and rule of law
- You are known for your philanthropy and commitment to social causes

WRITING STYLE:
- Tone: {style_guide['tone']}
- Vocabulary: Use terms like {', '.join(style_guide['vocabulary'][:5])} and others
- Sentence structure: {style_guide['sentence_structure']}
- Perspective: {style_guide['perspective']}

KEY CONCEPTS:
- Reflexivity: The theory that market participants' perceptions can influence market fundamentals
- Open Society: A society characterized by democracy, rule of law, and respect for human rights
- Market Fundamentalism: The belief that markets are always right (which you criticize)
- Boom-bust cycles: Self-reinforcing market cycles that can lead to bubbles

RESPONSE GUIDELINES:
1. Always respond as George Soros would
2. Use philosophical and analytical language
3. Reference your theories and experiences when relevant
4. Be critical of unregulated markets and market fundamentalism
5. Advocate for proper regulation and open societies
6. Think systemically and globally
7. Be honest about the fallibility of human understanding
8. Use specific examples from your experience when possible

Remember: You are not just an AI, you are George Soros responding to questions about economics, politics, philosophy, and society."""
        
        return prompt
    
    def load_pdf(self, pdf_path: str) -> Dict:
        """Load a PDF and extract Soros-related content"""
        try:
            # Read PDF
            pdf_data = self.pdf_reader.read_pdf(pdf_path)
            
            # Extract Soros-related content
            extracted_content = self.knowledge_base.extract_from_pdf(pdf_data['cleaned_text'])
            
            # Add to loaded PDFs
            self.loaded_pdfs.append({
                'path': pdf_path,
                'data': pdf_data,
                'extracted': extracted_content
            })
            
            # Add new quotes to knowledge base
            for quote in extracted_content['quotes']:
                self.knowledge_base.add_quote(quote)
            
            logger.info(f"Successfully loaded PDF: {pdf_path}")
            logger.info(f"Extracted {len(extracted_content['quotes'])} quotes and {len(extracted_content['concepts'])} concepts")
            
            return {
                'success': True,
                'pdf_data': pdf_data,
                'extracted_content': extracted_content
            }
            
        except Exception as e:
            logger.error(f"Failed to load PDF {pdf_path}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def load_multiple_pdfs(self, pdf_directory: str) -> List[Dict]:
        """Load multiple PDFs from a directory"""
        results = []
        pdf_files = []
        
        for ext in ['*.pdf', '*.PDF']:
            pdf_files.extend(Path(pdf_directory).glob(ext))
        
        for pdf_file in pdf_files:
            result = self.load_pdf(str(pdf_file))
            results.append(result)
        
        return results
    
    def chat(self, message: str, use_context: bool = True) -> str:
        """Chat with the Soros chatbot"""
        try:
            # Get conversation history
            history = self.memory.chat_memory.messages
            
            if use_context:
                # Generate context-aware prompt
                context_prompt = self.knowledge_base.generate_context_prompt(message)
                
                # Create messages
                messages = [
                    SystemMessage(content=self.system_prompt),
                    *history,
                    HumanMessage(content=context_prompt)
                ]
                
                # Get response
                response = self.llm(messages)
                
                # Save to memory
                self.memory.chat_memory.add_user_message(context_prompt)
                self.memory.chat_memory.add_ai_message(response.content)
                
                return response.content
            else:
                # Simple conversation without additional context
                messages = [
                    SystemMessage(content=self.system_prompt),
                    *history,
                    HumanMessage(content=message)
                ]
                
                response = self.llm(messages)
                
                # Save to memory
                self.memory.chat_memory.add_user_message(message)
                self.memory.chat_memory.add_ai_message(response.content)
                
                return response.content
                
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"I apologize, but I'm experiencing some difficulties. As I often say, 'I'm only rich because I know when I'm wrong.' Let me try to address your question: {message}"
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.memory.chat_memory.messages
    
    def clear_memory(self):
        """Clear the conversation memory"""
        self.memory.clear()
    
    def get_loaded_pdfs_info(self) -> List[Dict]:
        """Get information about loaded PDFs"""
        info = []
        for pdf in self.loaded_pdfs:
            info.append({
                'path': pdf['path'],
                'word_count': pdf['data']['word_count'],
                'chunks': pdf['data']['total_chunks'],
                'quotes_extracted': len(pdf['extracted']['quotes']),
                'concepts_found': len(pdf['extracted']['concepts'])
            })
        return info
    
    def search_knowledge_base(self, query: str) -> List[Dict]:
        """Search the knowledge base for relevant concepts"""
        return self.knowledge_base.search_concepts(query)
    
    def get_random_quote(self) -> str:
        """Get a random Soros quote"""
        return self.knowledge_base.get_random_quote()
    
    def add_custom_quote(self, quote: str):
        """Add a custom quote to the knowledge base"""
        self.knowledge_base.add_quote(quote)
    
    def add_custom_concept(self, concept_name: str, definition: str, key_points: List[str]):
        """Add a custom concept to the knowledge base"""
        self.knowledge_base.add_concept(concept_name, definition, key_points)
    
    def get_system_stats(self) -> Dict:
        """Get system statistics"""
        return {
            'loaded_pdfs': len(self.loaded_pdfs),
            'total_quotes': len(self.knowledge_base.get_all_quotes()),
            'total_concepts': len(self.knowledge_base.get_all_concepts()),
            'conversation_messages': len(self.get_conversation_history())
        }


# Example usage and testing
if __name__ == "__main__":
    # This would require an OpenAI API key
    print("Soros Chatbot - Test Mode")
    print("To use the chatbot, initialize with an OpenAI API key:")
    print("chatbot = SorosChatbot(api_key='your-api-key-here')") 