"""
Soros Chatbot Web Application
Streamlit interface for the Soros chatbot
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.soros_chatbot import SorosChatbot
from src.pdf_reader import PDFReader
from src.soros_knowledge_base import SorosKnowledgeBase

# Page configuration
st.set_page_config(
    page_title="Soros Chatbot",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .soros-quote {
        font-style: italic;
        color: #666;
        text-align: center;
        margin: 1rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .soros-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .sidebar-section {
        margin: 1rem 0;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Initialize the Soros chatbot"""
    api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, 'secrets') else os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error("⚠️ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable or add it to Streamlit secrets.")
        st.info("You can get an API key from: https://platform.openai.com/api-keys")
        return None
    
    try:
        return SorosChatbot(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {e}")
        return None

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Soros Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="soros-quote">"The financial markets generally are unpredictable. So that one has to have different scenarios..."</p>', unsafe_allow_html=True)
    
    # Initialize chatbot
    chatbot = initialize_chatbot()
    if not chatbot:
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("📚 Knowledge Base")
        
        # System stats
        stats = chatbot.get_system_stats()
        st.metric("Loaded PDFs", stats['loaded_pdfs'])
        st.metric("Total Quotes", stats['total_quotes'])
        st.metric("Total Concepts", stats['total_concepts'])
        
        st.divider()
        
        # PDF Upload
        st.header("📄 Upload PDFs")
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload PDFs containing Soros's writings or related content"
        )
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    try:
                        # Load PDF
                        result = chatbot.load_pdf(tmp_path)
                        
                        if result['success']:
                            st.success(f"✅ {uploaded_file.name} loaded successfully!")
                            st.info(f"Extracted {len(result['extracted_content']['quotes'])} quotes")
                        else:
                            st.error(f"❌ Failed to load {uploaded_file.name}")
                    
                    finally:
                        # Clean up temporary file
                        os.unlink(tmp_path)
        
        st.divider()
        
        # Knowledge base search
        st.header("🔍 Search Knowledge")
        search_query = st.text_input("Search concepts:", placeholder="e.g., reflexivity, market regulation")
        if search_query:
            results = chatbot.search_knowledge_base(search_query)
            if results:
                st.write("Found concepts:")
                for result in results:
                    with st.expander(result['concept']):
                        st.write(result['data']['definition'])
                        st.write("Key points:")
                        for point in result['data']['key_points']:
                            st.write(f"• {point}")
            else:
                st.info("No concepts found.")
        
        st.divider()
        
        # Random quote
        st.header("💭 Random Soros Quote")
        if st.button("Get Quote"):
            quote = chatbot.get_random_quote()
            st.info(f'"{quote}"')
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation"):
            chatbot.clear_memory()
            st.rerun()
    
    # Main chat area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("💬 Chat with George Soros")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask George Soros anything..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get Soros response
            with st.chat_message("assistant"):
                with st.spinner("George Soros is thinking..."):
                    response = chatbot.chat(prompt)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    with col2:
        st.header("📊 Quick Stats")
        
        # Loaded PDFs info
        if chatbot.loaded_pdfs:
            st.subheader("Loaded PDFs")
            for pdf_info in chatbot.get_loaded_pdfs_info():
                with st.expander(Path(pdf_info['path']).name):
                    st.write(f"Words: {pdf_info['word_count']}")
                    st.write(f"Chunks: {pdf_info['chunks']}")
                    st.write(f"Quotes: {pdf_info['quotes_extracted']}")
                    st.write(f"Concepts: {pdf_info['concepts_found']}")
        
        # Conversation stats
        st.subheader("Conversation")
        st.write(f"Messages: {len(st.session_state.messages)}")
        
        # Model info
        st.subheader("Model")
        st.write(f"Model: {chatbot.model}")
        st.write("Temperature: 0.7")

if __name__ == "__main__":
    main() 