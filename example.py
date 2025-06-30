"""
Example usage of the Soros Chatbot
Demonstrates basic functionality without requiring PDF uploads
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def main():
    """Example usage of the Soros chatbot"""
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    try:
        # Import and initialize chatbot
        from src.soros_chatbot import SorosChatbot
        from src.soros_knowledge_base import SorosKnowledgeBase
        
        print("🤖 Initializing Soros Chatbot...")
        chatbot = SorosChatbot(api_key=api_key)
        print("✅ Chatbot initialized successfully!")
        
        # Example 1: Basic conversation
        print("\n" + "="*60)
        print("EXAMPLE 1: Basic Conversation")
        print("="*60)
        
        questions = [
            "What is your theory of reflexivity?",
            "What do you think about market regulation?",
            "How do you view the role of government in the economy?",
            "What is an open society?"
        ]
        
        for question in questions:
            print(f"\n🤔 Question: {question}")
            print("🤖 Soros Response:")
            response = chatbot.chat(question)
            print(f"   {response}")
            print("-" * 40)
        
        # Example 2: Knowledge base exploration
        print("\n" + "="*60)
        print("EXAMPLE 2: Knowledge Base Exploration")
        print("="*60)
        
        kb = chatbot.knowledge_base
        
        # Get all concepts
        concepts = kb.get_all_concepts()
        print(f"\n📚 Available Concepts ({len(concepts)}):")
        for concept_name, concept_data in concepts.items():
            print(f"   • {concept_name}: {concept_data['definition'][:100]}...")
        
        # Search for specific concepts
        print(f"\n🔍 Searching for 'market' related concepts:")
        results = kb.search_concepts("market")
        for result in results:
            print(f"   • {result['concept']}: {result['data']['definition'][:80]}...")
        
        # Get random quotes
        print(f"\n💭 Random Soros Quotes:")
        for i in range(3):
            quote = kb.get_random_quote()
            print(f"   {i+1}. \"{quote}\"")
        
        # Example 3: System statistics
        print("\n" + "="*60)
        print("EXAMPLE 3: System Statistics")
        print("="*60)
        
        stats = chatbot.get_system_stats()
        print(f"📊 System Statistics:")
        print(f"   • Loaded PDFs: {stats['loaded_pdfs']}")
        print(f"   • Total Quotes: {stats['total_quotes']}")
        print(f"   • Total Concepts: {stats['total_concepts']}")
        print(f"   • Conversation Messages: {stats['conversation_messages']}")
        
        # Example 4: Adding custom content
        print("\n" + "="*60)
        print("EXAMPLE 4: Adding Custom Content")
        print("="*60)
        
        # Add a custom concept
        chatbot.add_custom_concept(
            "sustainable_capitalism",
            "A form of capitalism that considers long-term environmental and social impacts",
            [
                "Environmental responsibility",
                "Social equity",
                "Long-term thinking",
                "Stakeholder value"
            ]
        )
        
        # Add a custom quote
        chatbot.add_custom_quote(
            "The future of capitalism depends on its ability to address the challenges of sustainability and inequality."
        )
        
        print("✅ Added custom concept: 'sustainable_capitalism'")
        print("✅ Added custom quote about sustainable capitalism")
        
        # Test the new content
        print(f"\n🤔 Question: What do you think about sustainable capitalism?")
        response = chatbot.chat("What do you think about sustainable capitalism?")
        print(f"🤖 Soros Response: {response}")
        
        print("\n🎉 Example completed successfully!")
        print("💡 You can now run 'python cli.py' for interactive chat or 'streamlit run app.py' for the web interface.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main() 