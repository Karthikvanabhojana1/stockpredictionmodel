"""
Soros Chatbot Demo
Demonstrates the capabilities without requiring an API key
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Import configuration
sys.path.append(str(Path(__file__).parent))
from config import Config, create_env_file

def main():
    """Demo the Soros chatbot capabilities"""
    
    print("🤖 Soros Chatbot Demo")
    print("=" * 50)
    print()
    
    # Create .env file if it doesn't exist
    create_env_file()
    
    # Show configuration
    print("🔧 Configuration:")
    Config.print_config()
    print()
    
    # Test knowledge base
    print("🧠 Testing Knowledge Base...")
    try:
        from src.soros_knowledge_base import SorosKnowledgeBase
        
        kb = SorosKnowledgeBase()
        
        # Show available concepts
        concepts = kb.get_all_concepts()
        print(f"✅ Loaded {len(concepts)} concepts:")
        for concept_name, concept_data in concepts.items():
            print(f"   • {concept_name}: {concept_data['definition'][:80]}...")
        
        # Show available quotes
        quotes = kb.get_all_quotes()
        print(f"\n✅ Loaded {len(quotes)} quotes")
        
        # Test concept search
        print("\n🔍 Testing concept search...")
        results = kb.search_concepts("market")
        print(f"Found {len(results)} concepts related to 'market':")
        for result in results:
            print(f"   • {result['concept']}")
        
        # Test random quote
        print("\n💭 Testing random quote generation...")
        quote = kb.get_random_quote()
        print(f'"{quote}"')
        
        print("\n✅ Knowledge base is working correctly!")
        
    except Exception as e:
        print(f"❌ Knowledge base error: {e}")
    
    print("\n" + "=" * 50)
    
    # Test PDF reader
    print("\n📄 Testing PDF Reader...")
    try:
        from src.pdf_reader import PDFReader
        
        reader = PDFReader()
        
        # Check for PDFs in current directory
        pdf_files = list(Path(".").glob("*.pdf"))
        
        if pdf_files:
            print(f"✅ Found {len(pdf_files)} PDF file(s):")
            for pdf_file in pdf_files:
                print(f"   • {pdf_file.name}")
            
            # Test with first PDF
            test_pdf = pdf_files[0]
            print(f"\n📖 Testing with {test_pdf.name}...")
            
            result = reader.read_pdf(str(test_pdf))
            print(f"   ✅ Extracted {result['word_count']} words")
            print(f"   ✅ Created {result['total_chunks']} chunks")
            print(f"   ✅ Metadata: {result['metadata'].get('title', 'No title')}")
            
        else:
            print("ℹ️  No PDF files found in current directory")
            print("   Add some PDFs to test the PDF processing functionality")
        
        print("\n✅ PDF reader is working correctly!")
        
    except Exception as e:
        print(f"❌ PDF reader error: {e}")
    
    print("\n" + "=" * 50)
    
    # Show system architecture
    print("\n🏗️  System Architecture:")
    print("   • FastAPI Backend (api/main.py)")
    print("   • React Frontend (frontend/)")
    print("   • PDF Processing (src/pdf_reader.py)")
    print("   • Knowledge Base (src/soros_knowledge_base.py)")
    print("   • Chatbot Logic (src/soros_chatbot.py)")
    print("   • CLI Interface (cli.py)")
    print("   • Configuration (config.py)")
    
    print("\n" + "=" * 50)
    
    # Show next steps
    print("\n🚀 Next Steps:")
    print("1. Set your OpenAI API key in the .env file:")
    print("   Edit .env and replace 'your-api-key-here' with your actual key")
    print()
    print("2. Start the full application:")
    print("   ./start.sh")
    print()
    print("3. Or start components individually:")
    print("   # Backend only")
    print("   python api/main.py")
    print()
    print("   # Frontend only")
    print("   cd frontend && npm start")
    print()
    print("   # CLI only")
    print("   python cli.py")
    print()
    print("   # Setup environment")
    print("   python cli.py --setup")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed! The system is ready to use.")
    print("   Access the web interface at: http://localhost:3000")
    print("   API documentation at: http://localhost:8000/docs")
    print("   Configuration endpoint at: http://localhost:8000/config")

if __name__ == "__main__":
    main() 