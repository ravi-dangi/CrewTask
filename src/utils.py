import os
import time
from typing import Optional, Callable, Any
from functools import wraps


def ensure_directory(directory: str) -> str:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory: Path to the directory
        
    Returns:
        The directory path
    """
    os.makedirs(directory, exist_ok=True)
    return directory


def get_file_size_mb(file_path: str) -> float:
    """
    Get the size of a file in megabytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in MB
    """
    if not os.path.exists(file_path):
        return 0.0
    
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    return round(size_mb, 2)


def format_response(response: str, max_length: Optional[int] = None) -> str:
    """
    Format a response string for display.
    
    Args:
        response: Response string to format
        max_length: Optional maximum length to truncate
        
    Returns:
        Formatted response string
    """
    if not response:
        return "No response generated."
    
    # Remove excessive whitespace
    response = " ".join(response.split())
    
    # Truncate if needed
    if max_length and len(response) > max_length:
        response = response[:max_length] + "..."
    
    return response


def extract_city_from_question(question: str) -> Optional[str]:
    """
    Try to extract a city name from a weather-related question.
    
    Args:
        question: User's question
        
    Returns:
        City name if found, None otherwise
    """
    # Common patterns for weather questions
    patterns = [
        "weather in ",
        "weather at ",
        "weather for ",
        "temperature in ",
        "temperature at ",
        "how is the weather in ",
        "what's the weather in ",
        "what is the weather in "
    ]
    
    question_lower = question.lower()
    
    for pattern in patterns:
        if pattern in question_lower:
            # Extract text after the pattern
            start_idx = question_lower.index(pattern) + len(pattern)
            remaining = question[start_idx:].strip()
            
            # Take the first word/phrase (until punctuation or preposition)
            city = remaining.split()[0] if remaining.split() else None
            
            # Clean up punctuation
            if city:
                city = city.rstrip('.,;:?!')
                return city
    
    return None


def timer(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        print(f"⏱️ {func.__name__} executed in {elapsed_time:.2f} seconds")
        
        return result
    
    return wrapper


def classify_question_type(question: str) -> str:
    """
    Classify the type of question based on keywords.
    
    Args:
        question: User's question
        
    Returns:
        Question type: 'weather', 'pdf', 'web', or 'general'
    """
    question_lower = question.lower()
    
    # Weather keywords
    weather_keywords = [
        "weather", "temperature", "forecast", "rain", "sunny", 
        "cloudy", "wind", "humidity", "climate", "hot", "cold"
    ]
    
    # PDF keywords
    pdf_keywords = [
        "document", "pdf", "uploaded", "file", "paper", 
        "according to the document", "in the document"
    ]
    
    # Check for weather questions
    if any(keyword in question_lower for keyword in weather_keywords):
        return "weather"
    
    # Check for PDF questions
    if any(keyword in question_lower for keyword in pdf_keywords):
        return "pdf"
    
    # Default to web search
    return "web"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def is_valid_api_key(api_key: Optional[str]) -> bool:
    """
    Check if an API key is valid (not None and not empty).
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid, False otherwise
    """
    return api_key is not None and len(api_key.strip()) > 0


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing or replacing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename


def get_word_count(text: str) -> int:
    """
    Get the word count of a text string.
    
    Args:
        text: Text to count words in
        
    Returns:
        Number of words
    """
    return len(text.split())


def format_list_with_numbers(items: list[str]) -> str:
    """
    Format a list of items with numbers.
    
    Args:
        items: List of items to format
        
    Returns:
        Formatted string with numbered items
    """
    if not items:
        return "No items to display."
    
    formatted = []
    for idx, item in enumerate(items, 1):
        formatted.append(f"{idx}. {item}")
    
    return "\n".join(formatted)
