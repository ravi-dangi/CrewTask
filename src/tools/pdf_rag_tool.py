import os
import pickle
from typing import Optional
from crewai.tools import tool

import faiss
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader


# Global variables to store the vector store
_vector_store: Optional[FAISS] = None
_pdf_loaded: bool = False


@tool("PDF RAG Tool")
def query_pdf(question: str) -> str:
    """
    Answer questions based on PDF content using RAG.
    
    Args:
        question: Question to answer from PDF
        
    Returns:
        Answer with relevant context from PDF
    """
    global _vector_store, _pdf_loaded
    
    if not _pdf_loaded or _vector_store is None:
        return "Error: No PDF has been uploaded yet. Please upload a PDF document first."
    
    try:
        # Retrieve relevant documents using invoke instead of get_relevant_documents
        retriever = _vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}  # Retrieve top 3 most relevant chunks
        )
        
        relevant_docs = retriever.invoke(question)
        
        if not relevant_docs:
            return "No relevant information found in the PDF for your question."
        
        # Format the context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Create a response with context
        response = f"""
Based on the PDF content, here's the relevant information:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Retrieved Context:

{context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Answer:
{context[:500]}...

(Note: The full context has been retrieved. An LLM agent will synthesize a complete answer based on this information.)
"""
        return response.strip()
        
    except Exception as e:
        return f"Error retrieving information from PDF: {str(e)}"


def load_pdf(pdf_path: str) -> str:
    """
    Load and process a PDF file, creating embeddings and vector store.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Status message
    """
    global _vector_store, _pdf_loaded
    
    try:
        # Check if API key is configured
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return "Error: OPENROUTER_API_KEY not found in environment variables."
        
        # Set OpenAI API key and base URL for OpenRouter
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
        
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        if not documents:
            return "Error: No content extracted from PDF."
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_documents(documents)
        
        # Create embeddings
        embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        # Create FAISS vector store
        _vector_store = FAISS.from_documents(chunks, embeddings)
        _pdf_loaded = True
        
        # Save vector store for persistence
        vector_store_path = os.getenv("VECTOR_STORE_PATH", "./vector_store")
        os.makedirs(vector_store_path, exist_ok=True)
        
        _vector_store.save_local(os.path.join(vector_store_path, "faiss_index"))
        
        return f"✅ PDF loaded successfully! Processed {len(documents)} pages into {len(chunks)} chunks."
        
    except Exception as e:
        return f"Error loading PDF: {str(e)}"


def clear_pdf() -> str:
    """Clear the loaded PDF and vector store."""
    global _vector_store, _pdf_loaded
    _vector_store = None
    _pdf_loaded = False
    return "PDF cleared from memory."


def is_pdf_loaded() -> bool:
    """Check if a PDF is currently loaded."""
    return _pdf_loaded
