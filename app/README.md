# SREnity Streamlit App

Enterprise SRE incident response agent with interactive chat interface.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment activated
- Environment variables configured (`.env` file)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open in browser:**
   - The app will automatically open at `http://localhost:8501`
   - Or manually navigate to the URL shown in terminal

## 🎯 Features

### Interactive Chat Interface
- **Real-time conversation** with the SRE agent
- **Message history** with user and agent messages
- **Professional styling** with custom CSS
- **Responsive design** for different screen sizes

### Agent Capabilities
- **Runbook Search**: BM25 + Cohere Reranker for GitLab runbooks
- **Web Search**: Tavily for latest updates and CVEs
- **Multi-service Support**: Redis, PostgreSQL, Elastic, GitLab, etc.
- **Enterprise Scale**: Full GitLab runbook repository coverage

### User Experience
- **Sidebar information** about agent capabilities
- **Status indicators** for agent initialization
- **Clear chat** functionality
- **Error handling** with user-friendly messages

## 🔧 Configuration

### Environment Variables
Ensure your `.env` file contains:
```
OPENAI_API_KEY=your_openai_key
COHERE_API_KEY=your_cohere_key
TAVILY_API_KEY=your_tavily_key
```

### Customization
- **Styling**: Modify CSS in `streamlit_app.py`
- **Agent behavior**: Update `src/agents/sre_agent.py`
- **Tools**: Modify `src/agents/tools.py`

## 📊 Demo Scenarios

### Test Queries
Try these example queries:

1. **Redis Monitoring:**
   ```
   How to monitor Redis memory usage?
   ```

2. **PostgreSQL Issues:**
   ```
   PostgreSQL connection pool exhaustion in production - how to diagnose and fix?
   ```

3. **Version-specific:**
   ```
   Redis 7.2 memory leak issues and fixes
   ```

4. **Command Syntax:**
   ```
   Show me the exact syntax for Redis MEMORY STATS command
   ```

5. **Off-topic (Guardrails):**
   ```
   What's the weather like today?
   ```

## 🚀 Deployment

### Local Development
```bash
streamlit run streamlit_app.py
```

### Production Deployment
- **Streamlit Cloud**: Deploy directly from GitHub
- **Docker**: Containerize the application
- **Cloud Platforms**: AWS, GCP, Azure with Streamlit support

## 🛠️ Troubleshooting

### Common Issues

1. **Agent initialization fails:**
   - Check environment variables
   - Verify document files exist
   - Check API key validity

2. **Import errors:**
   - Ensure virtual environment is activated
   - Install all dependencies
   - Check Python path configuration

3. **Performance issues:**
   - Monitor memory usage
   - Check API rate limits
   - Optimize document loading

## 📈 Performance

### Expected Performance
- **Initialization**: 10-30 seconds (document loading)
- **Response time**: 5-15 seconds per query
- **Memory usage**: ~500MB-1GB (document storage)
- **Token usage**: Fixed per query (BM25 + Reranker)

### Optimization Tips
- **Document caching**: Documents loaded once per session
- **Agent reuse**: Single agent instance per session
- **Error handling**: Graceful degradation on failures

## 🎯 Certification Demo

### Key Points to Highlight
1. **Enterprise Scale**: Full GitLab runbook repository
2. **Advanced Retrieval**: BM25 + Reranker outperforms naive vector search
3. **Agentic Reasoning**: LangGraph ReAct pattern with tool selection
4. **Multi-service Support**: Redis, PostgreSQL, Elastic, etc.
5. **Production Ready**: Error handling, guardrails, professional UI

### Demo Flow
1. **Show agent initialization** and capabilities
2. **Demonstrate runbook search** with Redis queries
3. **Show web search fallback** for version-specific issues
4. **Test guardrails** with off-topic queries
5. **Highlight enterprise features** and scalability
