from ._compat import ensure_pkg_resources

ensure_pkg_resources()

import os
import warnings
from crewai import Agent
from langchain_openai import ChatOpenAI

from .tools import get_weather, search_web, query_pdf

# pydantic v2 exposes a v1 compatibility layer at pydantic.v1
try:
    from pydantic.v1.error_wrappers import ValidationError as PydanticV1ValidationError
except Exception:
    PydanticV1ValidationError = None


def get_llm() -> ChatOpenAI:
    """OpenRouter-backed chat model for CrewAI 0.28.x (uses LangChain ChatOpenAI).

    Notes
    - Different versions of the langchain/langchain-openai wrappers expect different
      keyword names for the model parameter: some expect `model_name`, others `model`.
      Passing the wrong keyword can raise a pydantic ValidationError or a TypeError.
      This helper tries `model_name` first, and falls back to `model` if the first
      attempt fails.
    - Ensure an API key is provided via `OPENROUTER_API_KEY` (preferred) or
      `OPENAI_API_KEY` as a fallback.
    """
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

    if not api_key:
        # Fail fast with a clear error so Streamlit surfaces a helpful message
        raise RuntimeError(
            "Missing API key: set OPENROUTER_API_KEY (preferred) or OPENAI_API_KEY"
        )

    # Common kwargs used for both instantiations
    common_kwargs = dict(
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.0,
    )

    first_exc = None

    # Try the modern/most-common parameter name first
    try:
        return ChatOpenAI(
            model_name=model_name,
            **common_kwargs,
        )
    except Exception as e:
        first_exc = e
        # If it's a pydantic v1 ValidationError or a TypeError, we'll try the alternative
        should_fallback = (
            isinstance(e, TypeError)
            or (PydanticV1ValidationError is not None and isinstance(e, PydanticV1ValidationError))
        )
        if not should_fallback:
            # Unknown error type — re-raise to avoid masking unexpected issues.
            raise

    # Fallback: try the older/alternate parameter name
    try:
        warnings.warn(
            "ChatOpenAI(model_name=...) failed; retrying with ChatOpenAI(model=...) as a fallback.",
            UserWarning,
        )
        return ChatOpenAI(
            model=model_name,
            **common_kwargs,
        )
    except Exception as e2:
        # Both attempts failed — raise a helpful error including both exception messages.
        raise RuntimeError(
            "Failed to instantiate ChatOpenAI with both 'model_name' and 'model' parameters. "
            f"First error: {type(first_exc).__name__}: {str(first_exc)}; "
            f"Second error: {type(e2).__name__}: {str(e2)}"
        )


class AgentFactory:
    """Factory class to create all agents for the RAG system."""
    
    @staticmethod
    def create_manager_agent() -> Agent:
        """
        Create the Manager Agent that routes questions to appropriate specialists.
        """
        return Agent(
            role="Question Router and Manager",
            goal=(
                "Understand user questions and intelligently route them to the appropriate specialist agent. "
                "Combine answers from multiple agents when needed to provide comprehensive responses."
            ),
            backstory=(
                "You are an experienced project manager with expertise in understanding user intent "
                "and delegating tasks to specialists. You analyze each question carefully to determine "
                "whether it requires weather information, web search, PDF analysis, or a combination. "
                "You ensure users get accurate, well-formatted answers from the right sources."
            ),
            verbose=True,
            allow_delegation=True,
            llm=get_llm()
        )
    
    @staticmethod
    def create_pdf_agent() -> Agent:
        """
        Create the PDF RAG Agent for answering questions from uploaded PDFs.
        """
        return Agent(
            role="PDF Document Analyst",
            goal=(
                "Extract and analyze information from uploaded PDF documents to answer user questions accurately. "
                "Provide precise answers with relevant context from the document."
            ),
            backstory=(
                "You are a meticulous document analyst specializing in information retrieval and synthesis. "
                "You excel at understanding complex documents, finding relevant information quickly, "
                "and presenting it in a clear, concise manner. You always cite the specific sections "
                "of the document that support your answers."
            ),
            tools=[query_pdf],
            verbose=True,
            allow_delegation=False,
            llm=get_llm()
        )
    
    @staticmethod
    def create_web_search_agent() -> Agent:
        """
        Create the Web Search Agent for finding current information online.
        """
        return Agent(
            role="Web Research Specialist",
            goal=(
                "Search the web for current, real-time information using the web search tool. "
                "ALWAYS use the search_web tool for every query - never rely on your training data. "
                "Provide accurate answers with credible sources and links."
            ),
            backstory=(
                "You are a skilled researcher with expertise in finding reliable information online. "
                "You MUST use the web search tool for EVERY query to get current information. "
                "You never answer questions from memory - you always search first. "
                "You know how to formulate effective search queries, evaluate source credibility, "
                "and synthesize information from multiple sources. You always provide source links "
                "so users can verify the information themselves."
            ),
            tools=[search_web],
            verbose=True,
            allow_delegation=False,
            llm=get_llm()
        )
    
    @staticmethod
    def create_weather_agent() -> Agent:
        """
        Create the Weather Agent for providing weather information.
        """
        return Agent(
            role="Weather Information Specialist",
            goal=(
                "Provide accurate, up-to-date weather information for any location worldwide. "
                "Present weather data in a clear, easy-to-understand format."
            ),
            backstory=(
                "You are a meteorology expert who specializes in communicating weather information "
                "to the general public. You understand weather patterns, can interpret meteorological data, "
                "and present it in a user-friendly way. You always include key details like temperature, "
                "conditions, humidity, and wind speed."
            ),
            tools=[get_weather],
            verbose=True,
            allow_delegation=False,
            llm=get_llm()
        )
    
    @staticmethod
    def create_all_agents() -> dict:
        """
        Create and return all agents as a dictionary.
        
        Returns:
            Dictionary with agent names as keys and Agent instances as values
        """
        return {
            "manager": AgentFactory.create_manager_agent(),
            "pdf_agent": AgentFactory.create_pdf_agent(),
            "web_search_agent": AgentFactory.create_web_search_agent(),
            "weather_agent": AgentFactory.create_weather_agent()
        }
