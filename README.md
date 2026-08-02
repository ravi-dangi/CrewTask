# 🤖 Agentic RAG System Using CrewAI

A multi-agent question-answering system that intelligently routes user questions to specialized AI agents using CrewAI framework. The system features a Manager Agent that coordinates between PDF RAG, Web Search, and Weather agents to provide comprehensive answers.

## 🎯 Features

- **🧠 Multi-Agent Architecture**: Four specialized agents working together
  - **Manager Agent**: Intelligent question routing and coordination
  - **PDF RAG Agent**: Document analysis using FAISS vector store
  - **Web Search Agent**: Real-time web information retrieval
  - **Weather Agent**: Live weather data from OpenWeather API

- **📄 PDF Processing**: Upload and analyze PDF documents with semantic search
- **🌐 Web Search**: Get current information with source citations
- **🌤️ Weather Data**: Real-time weather information for any location
- **💬 Interactive UI**: Clean Streamlit interface with chat history
- **🔄 Smart Routing**: Automatic or manual agent selection

## 📁 Project Structure

```
CrewTask/
├── app.py                      # Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
│
├── src/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration management
│   ├── utils.py              # Utility functions
│   ├── agents.py             # Agent definitions
│   ├── crew.py               # Crew orchestration
│   │
│   └── tools/
│       ├── __init__.py       # Tools package init
│       ├── weather_tool.py   # Weather API tool
│       ├── web_search_tool.py # Web search tool
│       └── pdf_rag_tool.py   # PDF RAG tool
│
├── uploads/                   # PDF upload directory
└── vector_store/             # FAISS vector store
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- API keys for:
  - [OpenRouter](https://openrouter.ai/) (for LLM)
  - [Serper](https://serper.dev/) (for web search)
  - [OpenWeather](https://openweathermap.org/api) (for weather data)

### Step 1: Clone or Download the Project

```bash
cd d:\futureness-agentic-ai\Demo_Projects\CrewTask
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (CMD):
.\venv\Scripts\activate.bat

# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```env
   # OpenRouter API Configuration
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_MODEL=openai/gpt-4-turbo-preview

   # Web Search Configuration (Serper API)
   SERPER_API_KEY=your_serper_api_key_here

   # Weather API Configuration (OpenWeather)
   OPENWEATHER_API_KEY=your_openweather_api_key_here

   # Vector Store Configuration
   VECTOR_STORE_PATH=./vector_store
   ```

## 🔑 Getting API Keys

### OpenRouter API Key
1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy the key to your `.env` file

### Serper API Key
1. Visit [Serper.dev](https://serper.dev/)
2. Sign up for a free account
3. Go to Dashboard
4. Copy your API key
5. Add it to your `.env` file

### OpenWeather API Key
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Create a free account
3. Navigate to API Keys section
4. Generate a new key
5. Add it to your `.env` file

## ✅ Verify Setup

Before running the application, verify your setup:

```bash
python check_setup.py
```

This will check:
- Python version
- Required dependencies
- Environment variables
- API keys configuration
- Directory structure

## 🎮 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Programmatic Usage

For command-line or script usage without the UI:

```bash
python example_usage.py
```

This provides interactive examples of:
- Weather queries
- Web searches
- PDF analysis
- Auto-routing
- Direct tool usage

### Using the System

#### 1. Upload PDF (Optional)
- Click the **"Browse files"** button in the sidebar
- Select a PDF document
- Wait for processing confirmation
- Now you can ask questions about the PDF content

#### 2. Select Routing Mode
- **Auto (Smart Routing)**: Manager automatically routes to appropriate agent
- **Weather Agent**: Directly use weather agent
- **Web Search Agent**: Directly use web search agent
- **PDF Agent**: Directly use PDF analysis agent

#### 3. Ask Questions
Type your question in the chat input and press Enter.

**Example Questions:**

**Weather:**
```
What's the weather in London?
Tell me the temperature in New York
How's the weather in Tokyo today?
```

**Web Search:**
```
What are the latest trends in AI?
Who won the Nobel Prize in Physics in 2023?
What is the capital of Australia?
```

**PDF (after uploading a document):**
```
Summarize the main points of this document
What does the document say about [topic]?
Extract key findings from the PDF
```

## 🏗️ Architecture

### Agent Hierarchy

```
┌─────────────────────────────────────┐
│        Manager Agent                │
│   (Question Router & Coordinator)   │
└─────────────┬───────────────────────┘
              │
              │ Delegates to:
              │
    ┌─────────┼─────────┬─────────┐
    │         │         │         │
    ▼         ▼         ▼         ▼
┌──────┐ ┌────────┐ ┌──────┐ ┌─────────┐
│ PDF  │ │  Web   │ │Weather│ │ Manager │
│Agent │ │ Search │ │ Agent │ │Combines │
│      │ │ Agent  │ │       │ │ Results │
└──────┘ └────────┘ └───────┘ └─────────┘
```

### Data Flow

1. **User Input** → Streamlit UI
2. **Question Analysis** → Manager Agent (Auto mode) or Direct Agent
3. **Tool Execution** → Specialized tools (Weather/Web/PDF)
4. **Result Synthesis** → Agent processing
5. **Response Display** → Streamlit UI with formatting

## 🛠️ Customization

### Changing the LLM Model

Edit `.env`:
```env
OPENROUTER_MODEL=anthropic/claude-3-opus
```

Available models on OpenRouter:
- `openai/gpt-4-turbo-preview`
- `openai/gpt-3.5-turbo`
- `anthropic/claude-3-opus`
- `anthropic/claude-3-sonnet`
- `meta-llama/llama-3-70b`

### Adjusting Chunk Size for PDF Processing

Edit `src/config.py`:
```python
CHUNK_SIZE: int = 1000        # Characters per chunk
CHUNK_OVERLAP: int = 200      # Overlap between chunks
```

### Modifying Number of Search Results

Edit `src/config.py`:
```python
MAX_SEARCH_RESULTS: int = 5   # Number of web search results
```

## 🧪 Testing the System

### Test Weather Agent
```
What's the weather in Paris?
```

### Test Web Search Agent
```
What is CrewAI framework?
```

### Test PDF Agent
1. Upload a PDF file
2. Ask: "What is this document about?"

### Test Auto Routing
```
What's the weather in Berlin and what are the top tourist attractions there?
```
*(Manager will coordinate both Weather and Web Search agents)*

## 📝 Configuration Files

### `config.py` - Main Configuration
- API key management
- Model settings
- Path configurations
- Validation logic

### `utils.py` - Helper Functions
- File operations
- Text formatting
- Question classification
- Performance timing

### `agents.py` - Agent Definitions
- Agent roles and goals
- Tool assignments
- LLM configuration

### `crew.py` - Orchestration
- Task creation
- Agent coordination
- Routing logic

## 🔧 Troubleshooting

### Issue: "API key not found"
**Solution**: Ensure `.env` file exists and contains valid API keys

### Issue: "No PDF loaded"
**Solution**: Upload a PDF document before asking PDF-related questions

### Issue: "Error connecting to weather service"
**Solution**: Check your OPENWEATHER_API_KEY and internet connection

### Issue: "Import errors"
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "FAISS errors on Windows"
**Solution**: Use `faiss-cpu` instead of `faiss-gpu`:
```bash
pip install faiss-cpu==1.7.4
```

## 📊 Performance Tips

1. **Use Simple Routing**: For faster responses, use direct agent routing instead of auto mode
2. **PDF Size**: Keep PDFs under 50 pages for optimal performance
3. **Cache**: Vector stores are cached after first PDF load
4. **API Limits**: Be aware of API rate limits on free tiers

## 🔐 Security Notes

- Never commit `.env` file to version control
- Keep API keys confidential
- Rotate API keys periodically
- Use environment-specific `.env` files for different deployments

## 🤝 Contributing

To extend the system:

1. **Add New Agent**: 
   - Create agent in `src/agents.py`
   - Add to `AgentFactory.create_all_agents()`

2. **Add New Tool**:
   - Create tool file in `src/tools/`
   - Inherit from `BaseTool`
   - Import in `src/tools/__init__.py`

3. **Modify UI**:
   - Edit `app.py`
   - Update Streamlit components

## 📚 Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)

## 📄 License

This project is open source and available for educational purposes.

## 🙋 Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section
2. Review configuration files
3. Verify API keys are valid
4. Check console logs for detailed errors

---

**Built with ❤️ using CrewAI, Streamlit, and OpenRouter**
