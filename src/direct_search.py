"""Direct web search without agent overhead."""
import os
import requests


def direct_web_search(query: str) -> str:
    """
    Directly search the web using SerpApi without agent overhead.
    
    Args:
        query: Search query string
        
    Returns:
        Formatted search results with sources
    """
    api_key = os.getenv("SERPER_API_KEY")
    
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
        results.append(f"🔍 **Web Search Results for: '{query}'**\n")
        
        # Add answer box if available
        if "answer_box" in data:
            answer = data["answer_box"]
            if "answer" in answer:
                results.append(f"📌 **Quick Answer:** {answer['answer']}\n")
            elif "snippet" in answer:
                results.append(f"📌 **Quick Answer:** {answer['snippet']}\n")
        
        # Add organic search results
        if "organic_results" in data and data["organic_results"]:
            results.append("**Detailed Results:**")
            results.append("━" * 60)
            
            for idx, result in enumerate(data["organic_results"][:5], 1):
                title = result.get("title", "No title")
                link = result.get("link", "")
                snippet = result.get("snippet", "No description available")
                
                results.append(f"\n**{idx}. {title}**")
                results.append(f"{snippet}")
                results.append(f"🔗 Source: {link}")
            
            results.append("━" * 60)
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
                "3. Restart the application"
            )
        return f"Error with search API: {str(e)}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to search service: {str(e)}"
    except Exception as e:
        return f"Unexpected error during search: {str(e)}"
