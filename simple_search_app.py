"""Simple search interface that directly calls the web search API."""
import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Direct Web Search", page_icon="🔍")

st.title("🔍 Direct Web Search")
st.markdown("This version directly calls SerpApi without using AI agents.")

# Input
query = st.text_input("Enter your search query:", placeholder="e.g., who won the FIFA World Cup 2022")

if st.button("Search") and query:
    with st.spinner("Searching..."):
        api_key = os.getenv("SERPER_API_KEY")
        
        if not api_key:
            st.error("API key not found! Check your .env file.")
        else:
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
                
                # Display answer box if available
                if "answer_box" in data:
                    answer = data["answer_box"]
                    st.success("📌 Quick Answer")
                    if "answer" in answer:
                        st.info(answer['answer'])
                    elif "snippet" in answer:
                        st.info(answer['snippet'])
                
                # Display organic results
                if "organic_results" in data and data["organic_results"]:
                    st.markdown("### 🔍 Search Results")
                    
                    for idx, result in enumerate(data["organic_results"][:5], 1):
                        with st.expander(f"{idx}. {result.get('title', 'No title')}"):
                            st.write(result.get('snippet', 'No description available'))
                            st.markdown(f"🔗 [{result.get('link', '')}]({result.get('link', '')})")
                else:
                    st.warning("No results found.")
                    
            except requests.exceptions.HTTPError as e:
                st.error(f"HTTP Error: {e}")
                st.error(f"Status Code: {response.status_code}")
                st.error(f"Response: {response.text[:500]}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("💡 **Tip**: This directly calls the SerpApi to verify it's working correctly.")
