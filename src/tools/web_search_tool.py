import os
import requests
from crewai.tools import tool


@tool("Web Search Tool")
def search_web(query: str) -> str:
    """
    Search the web using Serper API.
    
    Args:
        query: Search query string
        
    Returns:
        Formatted search results with sources
    """
    api_key = os.getenv("SERPER_API_KEY")
    
    if not api_key:
        return "Error: Serper API key not found. Please configure SERPER_API_KEY in .env file."
    
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": 5  # Number of results
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Format search results
        results = []
        
        # Add answer box if available
        if "answerBox" in data:
            answer = data["answerBox"]
            if "answer" in answer:
                results.append(f"📌 Quick Answer: {answer['answer']}")
            elif "snippet" in answer:
                results.append(f"📌 Quick Answer: {answer['snippet']}")
            results.append("")
        
        # Add organic search results
        if "organic" in data and data["organic"]:
            results.append("🔍 Search Results:")
            results.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            
            for idx, result in enumerate(data["organic"][:5], 1):
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
        return f"Error with search API: {str(e)}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to search service: {str(e)}"
    except KeyError as e:
        return f"Error parsing search results: Missing field {str(e)}"
    except Exception as e:
        return f"Unexpected error during search: {str(e)}"
