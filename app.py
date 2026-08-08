import streamlit as st
import os
from dotenv import load_dotenv

# crewai 0.28.x needs pkg_resources; Streamlit Cloud may omit setuptools
from src._compat import ensure_pkg_resources
ensure_pkg_resources()

from src.crew import RAGCrew
from src.tools.pdf_rag_tool import load_pdf, clear_pdf, is_pdf_loaded

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Agentic RAG System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
    .agent-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    .weather-badge {
        background-color: #87ceeb;
        color: #000;
    }
    .web-badge {
        background-color: #90ee90;
        color: #000;
    }
    .pdf-badge {
        background-color: #ffb6c1;
        color: #000;
    }
    .manager-badge {
        background-color: #dda0dd;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'crew' not in st.session_state:
        st.session_state.crew = RAGCrew()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'pdf_loaded' not in st.session_state:
        st.session_state.pdf_loaded = False
    if 'pdf_filename' not in st.session_state:
        st.session_state.pdf_filename = None


def render_header():
    """Render the main header."""
    st.markdown('<div class="main-header">🤖 Agentic RAG System</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Multi-Agent Question Answering System powered by CrewAI</div>',
        unsafe_allow_html=True
    )


def render_sidebar():
    """Render the sidebar with agent information and PDF upload."""
    with st.sidebar:
        st.header("📋 System Information")
        
        # Agent badges
        st.subheader("Available Agents")
        st.markdown("""
        <span class="agent-badge manager-badge">👔 Manager</span>
        <span class="agent-badge pdf-badge">📄 PDF RAG</span>
        <span class="agent-badge web-badge">🌐 Web Search</span>
        <span class="agent-badge weather-badge">🌤️ Weather</span>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # PDF Upload Section
        st.subheader("📄 PDF Document")
        uploaded_file = st.file_uploader(
            "Upload a PDF for analysis",
            type=['pdf'],
            help="Upload a PDF document to ask questions about its content"
        )
        
        if uploaded_file is not None:
            # Save uploaded file
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, uploaded_file.name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Load PDF into RAG system
            with st.spinner("Processing PDF..."):
                result = load_pdf(file_path)
                
                if "successfully" in result:
                    st.success(result)
                    st.session_state.pdf_loaded = True
                    st.session_state.pdf_filename = uploaded_file.name
                else:
                    st.error(result)
                    st.session_state.pdf_loaded = False
        
        # Display current PDF status
        if st.session_state.pdf_loaded and st.session_state.pdf_filename:
            st.info(f"📌 Loaded: {st.session_state.pdf_filename}")
            if st.button("Clear PDF"):
                clear_pdf()
                st.session_state.pdf_loaded = False
                st.session_state.pdf_filename = None
                st.rerun()
        
        st.markdown("---")
        
        # Agent Routing Mode
        st.subheader("🎯 Routing Mode")
        routing_mode = st.radio(
            "Select routing mode:",
            options=["Auto (Smart Routing)", "Weather Agent", "Web Search Agent", "PDF Agent"],
            help="Choose how questions are routed to agents"
        )
        
        st.markdown("---")
        
        # Information
        st.subheader("ℹ️ How It Works")
        st.markdown("""
        **Auto Mode**: Manager agent automatically routes your question to the appropriate specialist(s).
        
        **Manual Mode**: Directly send your question to a specific agent.
        
        **Agents**:
        - 👔 **Manager**: Routes & coordinates
        - 📄 **PDF RAG**: Analyzes uploaded PDFs
        - 🌐 **Web Search**: Searches online
        - 🌤️ **Weather**: Provides weather info
        """)
        
        return routing_mode


def render_chat_history():
    """Render the chat history."""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_task_type(routing_mode: str) -> str:
    """Convert routing mode to task type."""
    mode_map = {
        "Auto (Smart Routing)": "auto",
        "Weather Agent": "weather",
        "Web Search Agent": "web",
        "PDF Agent": "pdf"
    }
    return mode_map.get(routing_mode, "auto")


def main():
    """Main application function."""
    # Initialize
    initialize_session_state()
    
    # Render UI
    render_header()
    routing_mode = render_sidebar()
    
    # Main chat interface
    st.markdown("### 💬 Chat Interface")
    
    # Display chat history
    render_chat_history()
    
    # Chat input
    user_question = st.chat_input("Ask me anything about weather, web info, or uploaded PDFs...")
    
    if user_question:
        # Add user message to chat
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Get response from crew
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                task_type = get_task_type(routing_mode)
                
                # Check if PDF question but no PDF loaded
                if task_type == "pdf" and not st.session_state.pdf_loaded:
                    response = "⚠️ Please upload a PDF document first before asking PDF-related questions."
                else:
                    # Process question
                    try:
                        response = st.session_state.crew.process_question_simple(user_question)
                    except Exception as e:
                        response = f"❌ Error: {str(e)}"
                
                st.markdown(response)
        
        # Add assistant response to chat
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
    
    # Clear chat button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
        "Built with CrewAI 🤖 | Powered by OpenRouter 🚀"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
