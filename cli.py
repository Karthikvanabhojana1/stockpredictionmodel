"""
Soros Chatbot Command Line Interface
Simple CLI for testing the chatbot without web dependencies
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Import configuration
sys.path.append(str(Path(__file__).parent))
from config import Config, create_env_file

from src.soros_chatbot import SorosChatbot
from src.pdf_reader import PDFReader
from src.soros_knowledge_base import SorosKnowledgeBase


def main():
    """Main CLI function"""
    print("🤖 Soros Chatbot - Command Line Interface")
    print("=" * 50)
    
    # Create .env file if it doesn't exist
    create_env_file()
    
    # Check for API key
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\n📝 To fix this:")
        print("1. Edit the .env file in the project root")
        print("2. Replace 'your-api-key-here' with your actual OpenAI API key")
        print("3. Get an API key from: https://platform.openai.com/api-keys")
        return
    
    try:
        # Initialize chatbot
        print("🔄 Initializing Soros Chatbot...")
        chatbot = SorosChatbot(
            api_key=Config.OPENAI_API_KEY,
            model=Config.OPENAI_MODEL
        )
        print("✅ Chatbot initialized successfully!")
        
        # Show configuration
        print(f"\n🔧 Configuration:")
        print(f"   Model: {Config.OPENAI_MODEL}")
        print(f"   Temperature: {Config.OPENAI_TEMPERATURE}")
        print(f"   Max Tokens: {Config.OPENAI_MAX_TOKENS}")
        
        # Show initial stats
        stats = chatbot.get_system_stats()
        print(f"\n📊 System Stats:")
        print(f"   Loaded PDFs: {stats['loaded_pdfs']}")
        print(f"   Total Quotes: {stats['total_quotes']}")
        print(f"   Total Concepts: {stats['total_concepts']}")
        
        # Main interaction loop
        print("\n💬 Start chatting with George Soros! (Type 'quit' to exit)")
        print("💡 Try asking about: reflexivity, market regulation, open society, etc.")
        print("-" * 50)
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! As Soros would say, 'I'm only rich because I know when I'm wrong.'")
                    break
                
                if not user_input:
                    continue
                
                # Get Soros response
                print("🤔 George Soros is thinking...")
                response = chatbot.chat(user_input)
                print(f"\nGeorge Soros: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Let's continue with the conversation...")
    
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        print("Please check your API key and internet connection.")


def test_pdf_loading():
    """Test PDF loading functionality"""
    print("\n📄 Testing PDF Loading...")
    
    # Check if there are any PDFs in the current directory
    pdf_files = list(Path(".").glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in current directory.")
        print("You can add PDF files to test the PDF loading functionality.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s):")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")
    
    # Test PDF reader
    try:
        reader = PDFReader()
        for pdf_file in pdf_files:
            print(f"\n📖 Processing {pdf_file.name}...")
            result = reader.read_pdf(str(pdf_file))
            print(f"   Words extracted: {result['word_count']}")
            print(f"   Chunks created: {result['total_chunks']}")
            print(f"   Metadata: {result['metadata'].get('title', 'No title')}")
    except Exception as e:
        print(f"❌ PDF processing error: {e}")


def test_knowledge_base():
    """Test knowledge base functionality"""
    print("\n🧠 Testing Knowledge Base...")
    
    try:
        kb = SorosKnowledgeBase()
        
        # Test concept search
        print("🔍 Searching for 'market' concepts...")
        results = kb.search_concepts("market")
        print(f"Found {len(results)} concepts:")
        for result in results:
            print(f"  - {result['concept']}: {result['data']['definition'][:100]}...")
        
        # Test quote generation
        print("\n💭 Getting random quote...")
        quote = kb.get_random_quote()
        print(f'"{quote}"')
        
        # Test context generation
        print("\n📝 Testing context generation...")
        context = kb.generate_context_prompt("What do you think about market regulation?")
        print(f"Generated context ({len(context)} characters):")
        print(context[:200] + "..." if len(context) > 200 else context)
        
    except Exception as e:
        print(f"❌ Knowledge base error: {e}")


def setup_env():
    """Setup environment and configuration"""
    print("🔧 Setting up Soros Chatbot environment...")
    
    # Create .env file
    if create_env_file():
        print("✅ .env file created successfully")
        print("📝 Please edit .env and set your OpenAI API key")
    else:
        print("❌ Failed to create .env file")
    
    # Print configuration
    Config.print_config()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Soros Chatbot CLI")
    parser.add_argument("--test-pdf", action="store_true", help="Test PDF loading functionality")
    parser.add_argument("--test-kb", action="store_true", help="Test knowledge base functionality")
    parser.add_argument("--setup", action="store_true", help="Setup environment and configuration")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_env()
    elif args.test_pdf:
        test_pdf_loading()
    elif args.test_kb:
        test_knowledge_base()
    else:
        main() 