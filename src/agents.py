from ._compat import ensure_pkg_resources

ensure_pkg_resources()

import os
from crewai import Agent
from langchain_openai import ChatOpenAI

from .tools import get_weather, search_web, query_pdf


def get_llm() -> ChatOpenAI:
    """OpenRouter-backed chat model for CrewAI 0.28.x (uses LangChain ChatOpenAI).

    Notes
    - Some versions of `langchain` / `langchain-openai` expect the model argument
      to be called `model_name` instead of `model`. Passing the wrong keyword
      causes a pydantic validation error during instantiation (seen in the app
      logs). This helper tries the canonical `model_name` first and falls back
      to `model` if necessary.
    - Ensure an API key is provided via `OPENROUTER_API_KEY` (preferred) or
      `OPENAI_API_KEY` as a fallback.
    """
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

    if not api_key:
        # Fail fast with a clear error so Streamlit shows a helpful message
        raise RuntimeError(
            "Missing API key: set OPENROUTER_API_KEY (preferred) or OPENAI_API_KEY"
        )

    # Try the most common/modern parameter name first (model_name).
    try:
        return ChatOpenAI(
            model_name=model_name,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.0,
        )
    except TypeError:
        # Some older/alternate wrappers expect `model` instead of `model_name`.
        return ChatOpenAI(
            model=model_name,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.0,
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
