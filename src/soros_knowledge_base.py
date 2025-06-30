"""
Soros Knowledge Base Module
Manages George Soros's writings, speeches, and philosophical concepts
"""

import json
import logging
from typing import List, Dict, Optional, Any
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SorosKnowledgeBase:
    """Knowledge base for George Soros's writings and philosophy"""
    
    def __init__(self, data_dir: str = "data/soros"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Soros's key concepts and writings
        self.soros_concepts = {
            "reflexivity": {
                "definition": "The theory that market participants' perceptions can influence market fundamentals, creating a feedback loop between thinking and reality.",
                "key_points": [
                    "Markets are not always efficient",
                    "Perceptions can become reality",
                    "Self-reinforcing cycles exist",
                    "Fallibility of human understanding"
                ]
            },
            "open_society": {
                "definition": "A society characterized by democracy, rule of law, respect for human rights, and open markets.",
                "key_points": [
                    "Democratic governance",
                    "Free press and expression",
                    "Rule of law",
                    "Market economy with regulation",
                    "Respect for minority rights"
                ]
            },
            "market_fundamentalism": {
                "definition": "The belief that markets are always right and should be left to their own devices without regulation.",
                "key_points": [
                    "Criticism of laissez-faire economics",
                    "Need for regulation",
                    "Market imperfections",
                    "Role of government intervention"
                ]
            }
        }
        
        # Soros's writing style characteristics
        self.writing_style = {
            "tone": "philosophical, analytical, and often critical",
            "vocabulary": [
                "reflexivity", "fallibility", "open society", "market fundamentalism",
                "boom-bust cycles", "bubble", "regulation", "democracy",
                "capitalism", "globalization", "inequality", "sustainability"
            ],
            "sentence_structure": "complex, often using philosophical concepts",
            "perspective": "global, long-term, and systemic"
        }
        
        # Common Soros quotes and themes
        self.soros_quotes = [
            "The financial markets generally are unpredictable. So that one has to have different scenarios... The idea that you can actually predict what's going to happen contradicts my way of looking at the market.",
            "I'm only rich because I know when I'm wrong. I basically have survived by recognizing my mistakes.",
            "The main enemy of the open society, I believe, is no longer the communist but the capitalist threat.",
            "Markets are constantly in a state of uncertainty and flux and money is made by discounting the obvious and betting on the unexpected.",
            "The financial markets are not a zero-sum game. They are a positive-sum game.",
            "I am not a businessman. I am a speculator.",
            "The euro is like a marriage without a divorce clause.",
            "The current crisis is not only the bust that follows the housing boom, but something much bigger: it is the end of a 60-year period of credit expansion based on the dollar as the international reserve currency."
        ]
        
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load or create the knowledge base"""
        knowledge_file = self.data_dir / "soros_knowledge.json"
        
        if knowledge_file.exists():
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.soros_concepts.update(data.get('concepts', {}))
                    self.soros_quotes.extend(data.get('quotes', []))
                    logger.info("Loaded existing knowledge base")
            except Exception as e:
                logger.error(f"Failed to load knowledge base: {e}")
        
        self.save_knowledge_base()
    
    def save_knowledge_base(self):
        """Save the knowledge base to file"""
        knowledge_file = self.data_dir / "soros_knowledge.json"
        
        data = {
            'concepts': self.soros_concepts,
            'quotes': self.soros_quotes,
            'writing_style': self.writing_style
        }
        
        try:
            with open(knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Saved knowledge base")
        except Exception as e:
            logger.error(f"Failed to save knowledge base: {e}")
    
    def add_concept(self, concept_name: str, definition: str, key_points: List[str]):
        """Add a new concept to the knowledge base"""
        self.soros_concepts[concept_name] = {
            "definition": definition,
            "key_points": key_points
        }
        self.save_knowledge_base()
    
    def add_quote(self, quote: str):
        """Add a new quote to the knowledge base"""
        if quote not in self.soros_quotes:
            self.soros_quotes.append(quote)
            self.save_knowledge_base()
    
    def get_concept(self, concept_name: str) -> Optional[Dict]:
        """Get a specific concept"""
        return self.soros_concepts.get(concept_name)
    
    def get_random_quote(self) -> str:
        """Get a random quote from Soros"""
        import random
        return random.choice(self.soros_quotes)
    
    def search_concepts(self, query: str) -> List[Dict]:
        """Search concepts by keyword"""
        results = []
        query_lower = query.lower()
        
        for concept_name, concept_data in self.soros_concepts.items():
            if (query_lower in concept_name.lower() or 
                query_lower in concept_data['definition'].lower() or
                any(query_lower in point.lower() for point in concept_data['key_points'])):
                results.append({
                    'concept': concept_name,
                    'data': concept_data
                })
        
        return results
    
    def get_writing_style_guide(self) -> Dict:
        """Get the writing style guide for Soros-like responses"""
        return self.writing_style
    
    def generate_context_prompt(self, user_query: str) -> str:
        """Generate a context prompt for the chatbot"""
        # Search for relevant concepts
        relevant_concepts = self.search_concepts(user_query)
        
        # Get a relevant quote
        relevant_quote = self.get_random_quote()
        
        context = f"""You are George Soros, the renowned investor, philanthropist, and philosopher. 

Key aspects of your thinking:
- You believe in the theory of reflexivity: that market participants' perceptions can influence market fundamentals
- You advocate for open societies with democratic governance and rule of law
- You are critical of market fundamentalism and advocate for proper regulation
- You think globally and long-term about systemic issues

Relevant quote: "{relevant_quote}"

"""
        
        if relevant_concepts:
            context += "Relevant concepts:\n"
            for concept in relevant_concepts[:3]:  # Limit to top 3
                context += f"- {concept['concept']}: {concept['data']['definition']}\n"
        
        context += f"\nRespond to the user's question in your characteristic philosophical and analytical style: {user_query}"
        
        return context
    
    def extract_from_pdf(self, pdf_text: str) -> Dict:
        """Extract Soros-related content from PDF text"""
        extracted = {
            'quotes': [],
            'concepts': [],
            'themes': []
        }
        
        # Look for potential quotes (text in quotes)
        quote_pattern = r'"([^"]{20,})"'
        quotes = re.findall(quote_pattern, pdf_text)
        extracted['quotes'].extend(quotes[:10])  # Limit to 10
        
        # Look for key Soros concepts
        soros_keywords = [
            'reflexivity', 'open society', 'market fundamentalism',
            'boom-bust', 'bubble', 'regulation', 'democracy',
            'capitalism', 'globalization', 'inequality'
        ]
        
        for keyword in soros_keywords:
            if keyword.lower() in pdf_text.lower():
                extracted['concepts'].append(keyword)
        
        return extracted
    
    def get_all_concepts(self) -> Dict:
        """Get all concepts in the knowledge base"""
        return self.soros_concepts
    
    def get_all_quotes(self) -> List[str]:
        """Get all quotes in the knowledge base"""
        return self.soros_quotes


if __name__ == "__main__":
    # Test the knowledge base
    kb = SorosKnowledgeBase()
    
    # Test concept search
    results = kb.search_concepts("market")
    print(f"Found {len(results)} concepts related to 'market'")
    
    # Test quote generation
    quote = kb.get_random_quote()
    print(f"Random quote: {quote}")
    
    # Test context generation
    context = kb.generate_context_prompt("What do you think about market regulation?")
    print(f"Generated context: {context[:200]}...") 