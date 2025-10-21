# SREnity - Enterprise SRE Agent

![SREnity](SREnity.png)

**SREnity** is an End-to-End Agentic AI Prototype designed to accelerate Production Incident resolution using RAG-based runbook retrieval. The broader vision encompasses a comprehensive SRE assistant covering all infrastructure components (Redis, Elasticsearch, Cloud SQL, CI/CD, etc.) with advanced retrieval techniques and agentic reasoning.

**For this Certification Challenge, the implementation focuses on Redis-specific query response to demonstrate core capabilities and evaluation methodology.** This focused implementation showcases the technical architecture, advanced retrieval methods, and RAGAS evaluation framework that can be extended to the full SREnity vision.

## 🎯 Problem & Audience

**Problem:** SREs waste critical time searching through runbooks during production incidents, leading to extended MTTR and increased business impact.

**Target Users:** Site Reliability Engineers, DevOps teams, and incident response personnel who need rapid access to troubleshooting procedures during critical production issues.

**Why It's Critical:** In high-pressure incident scenarios, every minute counts. Traditional documentation search is slow, fragmented, and often misses critical context needed for effective resolution.

## 🏗️ Solution Design

**Proposed Solution:** An intelligent RAG-based system that retrieves relevant runbook procedures from GitLab's comprehensive SRE documentation, providing contextual, step-by-step guidance for incident resolution.

**Technology Stack with Justifications:**
- **LLM:** OpenAI GPT-4o-mini - Cost-effective and suitable for technical content processing
- **Embeddings:** OpenAI text-embedding-3-large - Optimized for technical documentation understanding
- **Vector Database:** Qdrant - High-performance vector storage with local deployment
- **Retrieval:** Ensemble Retriever (Naive Vector + BM25 + Reranker) - Combines semantic understanding with keyword precision
- **Orchestration:** LangChain - Modular RAG pipeline with comprehensive tool integration
- **Agent Framework:** LangGraph - ReAct pattern for autonomous reasoning and tool selection
- **Frontend:** Streamlit - Rapid prototyping with interactive chat interface
- **Evaluation:** RAGAS framework - Comprehensive RAG evaluation across 6 metrics

**Agentic Reasoning:** The system employs a LangGraph ReAct agent that autonomously:
- Analyzes incident queries to determine information needs
- Selects appropriate tools (runbook search vs web search) based on query context
- Chains multiple tool calls when needed (e.g., retrieve procedure → get latest updates)
- Refuses off-topic queries with clear guardrails
- Provides step-by-step reasoning for troubleshooting decisions

## 📊 Data Sources

**Primary Data Source:** GitLab Runbooks (runbooks.gitlab.com)
- **Full Corpus:** Real production SRE procedures covering Cloud SQL, Elastic, CI/CD, Redis, and infrastructure management
- **Certification Challenge Data Scope:** Redis-focused subset (33 documents, 685 chunks) for focused evaluation
- **Format:** Markdown runbooks with detailed troubleshooting procedures, commands, and configurations
- **Quality:** Comprehensive, production-tested content with rich technical detail

**External APIs and Use Cases:**
- **Tavily Search:** Latest updates, CVEs, version-specific issues not covered in runbooks
- **Cohere Rerank:** Advanced relevance scoring for retrieved documents
- **OpenAI API:** LLM reasoning, embeddings, and response generation

**Chunking Strategy:** 
- **Method:** Recursive character splitting with tiktoken encoding (1000-character chunks, 200-character overlap)
- **Rationale:** Preserves complete procedures while ensuring manageable context windows for LLM processing
- **Separators:** Hierarchical splitting by paragraphs, lines, and words for optimal content preservation

## 🚀 End-to-End Prototype

**Deployment:** Local Streamlit application accessible via localhost:8509
**Architecture:** 
- Document ingestion and chunking pipeline with HTML-to-Markdown preprocessing
- Vector embedding generation and Qdrant storage
- Ensemble retrieval system (Naive Vector + BM25 + Cohere Reranker)
- LangGraph ReAct agent with 2-tool system (search_runbooks + search_web)
- RAGAS evaluation framework with comprehensive metrics
- Interactive chat interface with real-time processing

**Demo Capabilities:**
- Real-time query processing with agentic reasoning
- Intelligent tool selection (runbook vs web search) based on query context
- Contextual runbook retrieval with fallback to web search for latest updates
- Step-by-step troubleshooting guidance with command examples
- Guardrails preventing off-topic responses with clear error messages
- Performance metrics visualization and comparison

**Repository Structure:**
- `notebooks/`: RAG evaluation and agent demonstration notebooks
- `src/agents/`: SREAgent class with LangGraph implementation
- `src/rag/`: Retrieval implementations (naive, BM25+reranker, ensemble)
- `src/utils/`: Configuration, document loading, and evaluation utilities
- `app/`: Streamlit deployment with custom styling and caching
- `data/`: Processed runbooks and evaluation datasets

## 📈 Performance Highlights

**Advanced Retrieval:** Ensemble approach combining semantic and keyword-based retrieval
**Agentic Reasoning:** LangGraph ReAct pattern for intelligent tool selection
**Production Ready:** Comprehensive evaluation with RAGAS framework
**Scalable Architecture:** Extensible to full GitLab runbook corpus

## 🔍 Key Features

**Intelligent Retrieval:** 
- Semantic understanding with vector embeddings
- Keyword precision with BM25 + Cohere reranking
- Ensemble combination for optimal performance

**Agentic Reasoning:**
- LangGraph ReAct pattern for autonomous tool selection
- Context-aware query processing
- Multi-step reasoning for complex incidents

**Production Ready:**
- Comprehensive RAGAS evaluation
- Redis-focused implementation with extensibility
- Real-time processing with caching

## 🎯 Quick Start

**Prerequisites:**
```bash
# Clone repository
git clone https://github.com/anilsharmay/SREnity.git
cd SREnity

# Install dependencies
pip install -e .

# Set up environment variables
cp env.example .env
# Edit .env with your API keys
```

**Run the Agent:**
```bash
# Start Streamlit app
cd app
streamlit run streamlit_app.py --server.port 8509
```

**Demo Questions:**
- "How do I restart Redis service without losing data?"
- "Redis memory usage is high, what should I check?"
- "How to configure Redis persistence for production?"

## 📚 Documentation

**Certification Report:** See `certification-challenge-report.md` for detailed evaluation results and certification deliverables.

**Development Notebooks:** 
- `notebooks/rag_evaluation.ipynb` - RAG pipeline development and evaluation
- `notebooks/agent_demo.ipynb` - Agent demonstration and testing

---

*SREnity - Enterprise SRE Agent for Production Incident Response*