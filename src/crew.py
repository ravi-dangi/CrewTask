from crewai import Crew, Task, Process
from .agents import AgentFactory


class RAGCrew:
    """Orchestrates the multi-agent RAG system."""
    
    def __init__(self):
        """Initialize the crew with all agents."""
        self.agents = AgentFactory.create_all_agents()
        self.crew = None
    
    def create_task(self, question: str, task_type: str = "auto") -> Task:
        """
        Create a task based on the question and type.
        
        Args:
            question: User's question
            task_type: Type of task - 'auto', 'weather', 'web', 'pdf'
            
        Returns:
            Task object
        """
        if task_type == "weather":
            return Task(
                description=f"Answer this weather-related question: {question}",
                agent=self.agents["weather_agent"],
                expected_output="Detailed weather information with temperature, conditions, humidity, and wind speed."
            )
        
        elif task_type == "web":
            return Task(
                description=f"Search the web and answer this question: {question}",
                agent=self.agents["web_search_agent"],
                expected_output="Comprehensive answer with information from credible sources and source links."
            )
        
        elif task_type == "pdf":
            return Task(
                description=f"Answer this question based on the uploaded PDF: {question}",
                agent=self.agents["pdf_agent"],
                expected_output="Accurate answer based on PDF content with relevant excerpts and context."
            )
        
        else:  # auto-routing through manager
            return Task(
                description=(
                    f"Analyze this question and route it to the appropriate specialist agent(s): {question}\n\n"
                    "Available agents:\n"
                    "- Weather Agent: for weather-related questions about specific locations\n"
                    "- Web Search Agent: for general knowledge, current events, and online information\n"
                    "- PDF Agent: for questions about uploaded PDF documents\n\n"
                    "You can delegate to one or multiple agents as needed. "
                    "Synthesize their responses into a coherent, comprehensive answer."
                ),
                agent=self.agents["manager"],
                expected_output="A complete, well-formatted answer that addresses all aspects of the user's question."
            )
    
    def process_question(self, question: str, task_type: str = "auto") -> str:
        """
        Process a question through the crew.
        
        Args:
            question: User's question
            task_type: Type of routing - 'auto', 'weather', 'web', 'pdf'
            
        Returns:
            Answer from the crew
        """
        try:
            # Create task based on question type
            task = self.create_task(question, task_type)
            
            # Determine which agents to include based on task type
            if task_type == "auto":
                # Manager can delegate to any agent
                agents = [
                    self.agents["manager"],
                    self.agents["weather_agent"],
                    self.agents["web_search_agent"],
                    self.agents["pdf_agent"]
                ]
            elif task_type == "weather":
                agents = [self.agents["weather_agent"]]
            elif task_type == "web":
                agents = [self.agents["web_search_agent"]]
            elif task_type == "pdf":
                agents = [self.agents["pdf_agent"]]
            else:
                agents = [self.agents["manager"]]
            
            # Create crew with hierarchical process for manager, sequential for others
            self.crew = Crew(
                agents=agents,
                tasks=[task],
                process=Process.hierarchical if task_type == "auto" else Process.sequential,
                manager_llm=AgentFactory.get_llm() if task_type == "auto" else None,
                verbose=True
            )
            
            # Execute the crew synchronously (recommended for Streamlit)
            result = self.crew.kickoff()
            
            return str(result)
            
        except Exception as e:
            return f"Error processing question: {str(e)}"
    
    async def process_question_async(self, question: str, task_type: str = "auto") -> str:
        """
        Process a question through the crew asynchronously.
        
        Args:
            question: User's question
            task_type: Type of routing - 'auto', 'weather', 'web', 'pdf'
            
        Returns:
            Answer from the crew
        """
        try:
            # Create task based on question type
            task = self.create_task(question, task_type)
            
            # Determine which agents to include based on task type
            if task_type == "auto":
                agents = [
                    self.agents["manager"],
                    self.agents["weather_agent"],
                    self.agents["web_search_agent"],
                    self.agents["pdf_agent"]
                ]
            elif task_type == "weather":
                agents = [self.agents["weather_agent"]]
            elif task_type == "web":
                agents = [self.agents["web_search_agent"]]
            elif task_type == "pdf":
                agents = [self.agents["pdf_agent"]]
            else:
                agents = [self.agents["manager"]]
            
            # Create crew
            self.crew = Crew(
                agents=agents,
                tasks=[task],
                process=Process.hierarchical if task_type == "auto" else Process.sequential,
                manager_llm=AgentFactory.get_llm() if task_type == "auto" else None,
                verbose=True
            )
            
            # Execute the crew asynchronously
            result = await self.crew.kickoff_async()
            
            return str(result)
            
        except Exception as e:
            return f"Error processing question: {str(e)}"
    
    def process_question_simple(self, question: str) -> str:
        """
        Simplified processing without auto-routing. Analyzes question and calls appropriate agent directly.
        
        Args:
            question: User's question
            
        Returns:
            Answer from the appropriate agent
        """
        try:
            # Simple keyword-based routing
            question_lower = question.lower()
            
            # Determine agent based on keywords
            if any(word in question_lower for word in ["weather", "temperature", "forecast", "rain", "sunny", "cloudy", "wind"]):
                task_type = "weather"
                agent = self.agents["weather_agent"]
                description = f"Provide weather information for: {question}"
                expected_output = "Detailed weather information including temperature, conditions, humidity, and wind speed."
            
            elif any(word in question_lower for word in ["pdf", "document", "uploaded", "file"]):
                task_type = "pdf"
                agent = self.agents["pdf_agent"]
                description = f"Answer based on the PDF document: {question}"
                expected_output = "Answer with relevant information extracted from the PDF document."
            
            else:
                # Default to web search for general questions
                task_type = "web"
                agent = self.agents["web_search_agent"]
                description = f"Search the web and answer: {question}"
                expected_output = "Comprehensive answer with sources from the web."
            
            # Create task
            task = Task(
                description=description,
                agent=agent,
                expected_output=expected_output
            )
            
            # Create crew with single agent
            self.crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute
            result = self.crew.kickoff()
            
            return str(result)
            
        except Exception as e:
            return f"Error processing question: {str(e)}"
