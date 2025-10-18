# SREnity - Enterprise SRE Agent Prototype

An End-to-End Agentic AI Prototype for accelerating Production Incident resolution using RAG-based runbook retrieval.

## Problem & Audience

**Problem:** SREs spend excessive time searching through documentation during production incidents, leading to delayed resolution and increased downtime.

**Target Users:** Site Reliability Engineers, DevOps teams, and incident response personnel who need rapid access to troubleshooting procedures during critical production issues.

## Solution Design

**Proposed Solution:** A RAG-based system that retrieves relevant runbook procedures from GitLab's comprehensive SRE documentation, providing contextual, step-by-step guidance for incident resolution.

**Tech Stack:**
- **LLM:** OpenAI GPT-4o-mini (cost-effective, suitable for technical content)
- **Embeddings:** OpenAI text-embedding-3-small (optimized for technical documentation)
- **Vector DB:** Qdrant (high-performance vector storage)
- **Orchestration:** LangChain (modular RAG pipeline)
- **Evaluation:** RAGAS framework (comprehensive RAG evaluation)
- **Frontend:** Streamlit (rapid prototyping and demo)

**Agent Usage:** The system employs a LangGraph ReAct agent that autonomously:
- Analyzes incident queries to determine information needs
- Selects appropriate tools (runbook search vs web search) based on query context
- Chains multiple tool calls when needed (e.g., retrieve procedure → get latest updates)
- Refuses off-topic queries with clear guardrails
- Provides step-by-step reasoning for troubleshooting decisions

## Data Sources

**Primary Data Source:** GitLab Runbooks (runbooks.gitlab.com)
- **Content:** Real production SRE procedures covering Cloud SQL, Elastic, CI/CD, Redis, and infrastructure management
- **Format:** Markdown runbooks with detailed troubleshooting procedures, commands, and configurations
- **Quality:** Comprehensive, production-tested content with rich technical detail

**Chunking Strategy:** 
- **Method:** Recursive character splitting with 1000-character chunks and 200-character overlap
- **Rationale:** Preserves complete procedures while ensuring manageable context windows for LLM processing

## End-to-End Prototype

**Deployment:** Local Streamlit application accessible via localhost
**Architecture:** 
- Document ingestion and chunking pipeline
- Vector embedding generation and storage
- Dual retrieval systems (naive vector search + advanced BM25+reranker)
- LangGraph ReAct agent with 2-tool system (runbook search + web search)
- RAGAS evaluation framework
- Performance comparison dashboard

**Demo Capabilities:**
- Real-time incident query processing with agentic reasoning
- Intelligent tool selection (runbook vs web search)
- Contextual runbook retrieval with fallback to web search
- Step-by-step troubleshooting guidance
- Guardrails preventing off-topic responses
- Performance metrics visualization

## Golden Test Dataset

**Evaluation Framework:** RAGAS with 6 core metrics
**Test Dataset:** 8 synthetic incident scenarios generated from GitLab runbooks
**Evaluation Results:**

| Metric | Naive Vector | BM25 + Reranker | Improvement |
|--------|-------------|-----------------|-------------|
| Faithfulness | 0.524 | 0.735 | +40.3% |
| Answer Relevancy | 0.838 | 0.817 | -2.5% |
| Context Precision | 0.750 | 0.500 | -33.3% |
| Context Recall | 0.708 | 0.667 | -5.8% |
| Answer Correctness | 0.537 | 0.443 | -17.5% |
| Context Entity Recall | 0.025 | 0.218 | +772.0% |

**Performance Conclusions:** BM25+Reranker shows significant improvements in factual accuracy (+40.3%) and entity coverage (+772%), but trade-offs in overall precision (-33.3%) and correctness (-17.5%). The naive vector approach provides more balanced performance for production use.

## Advanced Retrieval

**Implementation:** BM25 + Cohere Reranker pipeline
- **BM25 Retrieval:** Keyword-based retrieval of 12 candidate documents
- **Cohere Reranker:** Cross-attention reranking to select top 5 most relevant documents
- **Rationale:** Combines broad recall (BM25) with intelligent relevance scoring (reranker)

**Technical Details:**
- BM25 parameters: k=12 for broad candidate retrieval
- Cohere model: rerank-v3.5 for relevance scoring
- Final output: Top 5 documents after reranking

## Performance Assessment

**RAGAS Metrics Comparison:**
- **Faithfulness:** BM25+Reranker significantly outperforms (+40.3%) due to better factual grounding
- **Context Entity Recall:** Dramatic improvement (+772%) in finding specific commands and tools
- **Context Precision:** Notable decline (-33.3%) indicating more noise in retrieved documents
- **Answer Correctness:** Overall performance decrease (-17.5%) due to precision-recall trade-off

**Future Improvements:**
1. **Hybrid Retrieval:** Combine vector search with BM25+reranker for optimal precision-recall balance
2. **Query Expansion:** Implement multi-query retrieval to improve recall
3. **Context Filtering:** Add relevance filtering to reduce noise in retrieved documents
4. **Fine-tuning:** Optimize reranker parameters for SRE-specific content
5. **Evaluation Expansion:** Increase test dataset size and add domain-specific evaluation metrics

## Final Submission

**Demo Video:** 5-minute demonstration of incident → runbook retrieval workflow
**Documentation:** This README addresses all certification deliverables with comprehensive technical details and performance analysis.

---

*Built for AI Engineering Bootcamp Certification Challenge - Task 6: Advanced Retrieval Implementation*