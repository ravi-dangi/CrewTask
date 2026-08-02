#!/usr/bin/env python3
"""
Example usage script for Agentic RAG System.
Demonstrates how to use the system programmatically without the Streamlit UI.
"""

from src import RAGCrew, PDFRAGTool
from src.config import Config
import sys


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def example_weather_query():
    """Example: Query weather information."""
    print_header("Example 1: Weather Query")
    
    crew = RAGCrew()
    question = "What's the weather like in Paris?"
    
    print(f"Question: {question}\n")
    print("Processing...\n")
    
    response = crew.process_question_simple(question)
    print(f"Response:\n{response}\n")


def example_web_search():
    """Example: Web search query."""
    print_header("Example 2: Web Search Query")
    
    crew = RAGCrew()
    question = "What is CrewAI and how does it work?"
    
    print(f"Question: {question}\n")
    print("Processing...\n")
    
    response = crew.process_question_simple(question)
    print(f"Response:\n{response}\n")


def example_pdf_query():
    """Example: PDF query (requires uploaded PDF)."""
    print_header("Example 3: PDF Query")
    
    # First, check if a PDF is loaded
    if not PDFRAGTool.pdf_loaded:
        print("⚠️  No PDF loaded. To use this example:")
        print("1. Upload a PDF using the Streamlit UI first, or")
        print("2. Use PDFRAGTool.load_pdf('path/to/your/document.pdf')\n")
        return
    
    crew = RAGCrew()
    question = "What is the main topic of the uploaded document?"
    
    print(f"Question: {question}\n")
    print("Processing...\n")
    
    response = crew.process_question_simple(question)
    print(f"Response:\n{response}\n")


def example_auto_routing():
    """Example: Auto-routing with manager agent."""
    print_header("Example 4: Auto-Routing (Manager Agent)")
    
    crew = RAGCrew()
    question = "What's the weather in London and what are popular tourist attractions there?"
    
    print(f"Question: {question}\n")
    print("Processing... (Manager will coordinate multiple agents)\n")
    
    response = crew.process_question(question, task_type="auto")
    print(f"Response:\n{response}\n")


def example_load_pdf():
    """Example: Load a PDF programmatically."""
    print_header("Example 5: Load PDF Programmatically")
    
    # Example path - replace with your actual PDF path
    pdf_path = "uploads/sample.pdf"
    
    print(f"Attempting to load: {pdf_path}\n")
    
    import os
    if not os.path.exists(pdf_path):
        print(f"⚠️  PDF not found at {pdf_path}")
        print("Please provide a valid PDF path or upload via Streamlit UI\n")
        return
    
    result = PDFRAGTool.load_pdf(pdf_path)
    print(f"Result: {result}\n")


def example_direct_tool_usage():
    """Example: Use tools directly without agents."""
    print_header("Example 6: Direct Tool Usage")
    
    from src.tools import WeatherTool, WebSearchTool
    
    # Weather Tool
    print("Using Weather Tool directly:")
    weather_tool = WeatherTool()
    weather_result = weather_tool._run("Tokyo")
    print(f"{weather_result}\n")
    
    # Web Search Tool
    print("\nUsing Web Search Tool directly:")
    search_tool = WebSearchTool()
    search_result = search_tool._run("What is artificial intelligence?")
    print(f"{search_result}\n")


def main():
    """Run all examples."""
    print("\n🤖 Agentic RAG System - Example Usage")
    print("=" * 70)
    
    # Validate configuration
    is_valid, missing_keys = Config.validate()
    
    if not is_valid:
        print("\n⚠️  Configuration Error!")
        print(f"Missing API keys: {', '.join(missing_keys)}")
        print("\nPlease configure all API keys in .env file before running examples.")
        print("See .env.example for reference.\n")
        return 1
    
    print("\n✅ Configuration validated successfully!")
    
    # Menu
    print("\nAvailable Examples:")
    print("1. Weather Query")
    print("2. Web Search Query")
    print("3. PDF Query (requires uploaded PDF)")
    print("4. Auto-Routing with Manager")
    print("5. Load PDF Programmatically")
    print("6. Direct Tool Usage")
    print("7. Run All Examples")
    print("0. Exit")
    
    choice = input("\nSelect an example (0-7): ").strip()
    
    examples = {
        "1": example_weather_query,
        "2": example_web_search,
        "3": example_pdf_query,
        "4": example_auto_routing,
        "5": example_load_pdf,
        "6": example_direct_tool_usage,
    }
    
    if choice == "0":
        print("\nGoodbye! 👋\n")
        return 0
    
    if choice == "7":
        # Run all examples
        for example_func in examples.values():
            try:
                example_func()
            except Exception as e:
                print(f"❌ Error: {str(e)}\n")
    elif choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
    else:
        print("\n❌ Invalid choice. Please select 0-7.\n")
        return 1
    
    print("=" * 70)
    print("\n✨ Example completed!")
    print("\n💡 Tip: Use 'streamlit run app.py' for the full interactive UI.\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
