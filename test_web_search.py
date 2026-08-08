"""Test script to verify web search tool works correctly."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test the web search directly
import requests

api_key = os.getenv("SERPER_API_KEY")
query = "who won the FIFA World Cup 2022"

print("Testing SerpApi directly...")
print("=" * 60)
print(f"\nQuery: {query}\n")

try:
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": api_key,
        "num": 5,
        "engine": "google"
    }
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    
    # Check what we got
    print("Keys in response:", list(data.keys()))
    
    if "answer_box" in data:
        print("\nAnswer Box found:")
        print(data["answer_box"])
    
    if "organic_results" in data:
        print(f"\nFound {len(data['organic_results'])} organic results")
        for i, result in enumerate(data["organic_results"][:3], 1):
            print(f"\n{i}. {result.get('title', 'No title')}")
            print(f"   {result.get('snippet', 'No snippet')}")
            print(f"   {result.get('link', 'No link')}")
    
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
