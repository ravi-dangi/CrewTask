import os
import requests
from langchain.tools import tool

# Try to get environment variable with fallback
def get_env_var(key: str) -> str:
    """Get environment variable with Streamlit secrets fallback."""
    try:
        import streamlit as st
        if hasattr(st, 'secrets'):
            return st.secrets.get(key, os.getenv(key))
    except:
        pass
    return os.getenv(key)


@tool("Web Search Tool")
def search_web(query: str) -> str:
    """
    Search the web using SerpApi.
    
    Args:
        query: Search query string
        
    Returns:
        Formatted search results with sources
    """
    api_key = get_env_var("SERPER_API_KEY")  # Using SERPER_API_KEY env var for SerpApi key
    
    if not api_key:
        return "Error: API key not found. Please configure SERPER_API_KEY in .env file with your SerpApi key."
    
    try:
        # SerpApi uses GET request with parameters
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": api_key,
            "num": 5,  # Number of results
            "engine": "google"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Format search results
        results = []
        
        # Add answer box if available
        if "answer_box" in data:
            answer = data["answer_box"]
            if "answer" in answer:
                results.append(f"📌 Quick Answer: {answer['answer']}")
            elif "snippet" in answer:
                results.append(f"📌 Quick Answer: {answer['snippet']}")
            results.append("")
        
        # Add organic search results
        if "organic_results" in data and data["organic_results"]:
            results.append("🔍 Search Results:")
            results.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            
            for idx, result in enumerate(data["organic_results"][:5], 1):
                title = result.get("title", "No title")
                link = result.get("link", "")
                snippet = result.get("snippet", "No description available")
                
                results.append(f"\n{idx}. {title}")
                results.append(f"   {snippet}")
                results.append(f"   🔗 Source: {link}")
            
            results.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        else:
            return f"No results found for query: {query}"
        
        return "\n".join(results)
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            return (
                "⚠️ Web Search is currently unavailable - Invalid or expired SerpApi key.\n\n"
                "To fix this:\n"
                "1. Visit https://serpapi.com/dashboard and verify your API key\n"
                "2. Update SERPER_API_KEY in your .env file\n"
                "3. Restart the application\n\n"
                "💡 You can still use Weather and PDF features!"
            )
        return f"Error with search API: {str(e)}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to search service: {str(e)}"
    except KeyError as e:
        return f"Error parsing search results: Missing field {str(e)}"
    except Exception as e:
        return f"Unexpected error during search: {str(e)}"
