#!/usr/bin/env python3
"""
Setup verification script for Agentic RAG System.
Run this script to verify that all dependencies and API keys are configured correctly.
"""

import sys
import os
from dotenv import load_dotenv


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_status(item: str, status: bool, message: str = ""):
    """Print status of a check."""
    icon = "✅" if status else "❌"
    print(f"{icon} {item}: {'OK' if status else 'MISSING'}")
    if message:
        print(f"   {message}")


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print_header("Python Version Check")
    version = sys.version_info
    is_valid = version.major == 3 and version.minor >= 8
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    print_status("Python 3.8+", is_valid)
    return is_valid


def check_dependencies():
    """Check if all required packages are installed."""
    print_header("Dependencies Check")
    
    required_packages = [
        ("crewai", "crewai"),
        ("streamlit", "streamlit"),
        ("openai", "openai"),
        ("langchain", "langchain"),
        ("faiss", "faiss_cpu"),
        ("pypdf2", "PyPDF2"),
        ("requests", "requests"),
        ("python-dotenv", "dotenv"),
    ]
    
    all_installed = True
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print_status(package_name, True)
        except ImportError:
            print_status(package_name, False, f"Install with: pip install {package_name}")
            all_installed = False
    
    return all_installed


def check_api_keys():
    """Check if all API keys are configured."""
    print_header("API Keys Check")
    
    # Load environment variables
    load_dotenv()
    
    api_keys = {
        "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY"),
        "SERPER_API_KEY": os.getenv("SERPER_API_KEY"),
        "OPENWEATHER_API_KEY": os.getenv("OPENWEATHER_API_KEY"),
    }
    
    all_configured = True
    
    for key_name, key_value in api_keys.items():
        is_valid = key_value is not None and len(key_value.strip()) > 0
        print_status(key_name, is_valid, 
                    "Configured" if is_valid else "Add to .env file")
        if not is_valid:
            all_configured = False
    
    return all_configured


def check_directories():
    """Check if required directories exist."""
    print_header("Directory Structure Check")
    
    directories = [
        "src",
        "src/tools",
        "uploads",
        "vector_store",
    ]
    
    all_exist = True
    
    for directory in directories:
        exists = os.path.exists(directory)
        print_status(directory, exists)
        if not exists:
            all_exist = False
    
    return all_exist


def check_env_file():
    """Check if .env file exists."""
    print_header("Environment File Check")
    
    env_exists = os.path.exists(".env")
    env_example_exists = os.path.exists(".env.example")
    
    print_status(".env file", env_exists, 
                "Create from .env.example" if not env_exists else "Found")
    print_status(".env.example file", env_example_exists)
    
    if not env_exists and env_example_exists:
        print("\n💡 Tip: Copy .env.example to .env and add your API keys:")
        print("   copy .env.example .env")
    
    return env_exists


def main():
    """Run all checks."""
    print("\n🔍 Agentic RAG System - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version()),
        ("Dependencies", check_dependencies()),
        ("Environment File", check_env_file()),
        ("API Keys", check_api_keys()),
        ("Directories", check_directories()),
    ]
    
    print_header("Summary")
    
    all_passed = all(result for _, result in checks)
    
    for check_name, result in checks:
        print_status(check_name, result)
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✅ All checks passed! You're ready to run the application.")
        print("\n🚀 Start the application with:")
        print("   streamlit run app.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\n📖 See README.md for detailed setup instructions.")
    
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
