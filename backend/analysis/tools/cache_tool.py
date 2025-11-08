"""
Cache (Redis) tier RAG tool for analyzing cache server logs.
"""
import os
from typing import Annotated
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict, List
from langchain_core.documents import Document


class CacheLogAnalysisState(TypedDict):
    """State for cache log RAG analysis"""
    log_input: str
    context: List[Document]
    analysis_result: str


def create_cache_rag_tool():
    """
    Create a RAG tool for Redis cache log analysis.
    """
    current_file = os.path.abspath(__file__)
    tools_dir = os.path.dirname(current_file)
    analysis_dir = os.path.dirname(tools_dir)
    backend_dir = os.path.dirname(analysis_dir)
    cache_kb_path = os.path.join(backend_dir, "data", "knowledge_base", "cache")

    cache_docs = []
    if os.path.isdir(cache_kb_path):
        loader = DirectoryLoader(cache_kb_path, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
        cache_docs = loader.load()
        cache_docs = [doc for doc in cache_docs if doc.page_content and doc.page_content.strip()]
    else:
        raise FileNotFoundError(f"Cache knowledge base directory not found. Checked: {cache_kb_path}")

    if not cache_docs:
        raise ValueError(f"No documents with content loaded from {cache_kb_path}.")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", chunk_size=100)
    vectorstore = Qdrant.from_documents(cache_docs, embeddings, location=":memory:", batch_size=10)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a REDIS cache incident responder. Determine whether the logs represent healthy behaviour or problems (connection pool exhaustion, timeouts, memory pressure). Provide clear root cause and remediation guidance."),
        ("human", "Analyze the Redis logs:\n\nLogs:\n{query}\n\nContext:\n{context}\n\nPlease identify:\n1. Status and severity.\n2. Primary indicators in the logs.\n3. Likely root cause.\n4. Immediate remediation steps.\n5. Recommendations to prevent recurrence.")
    ])

    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = prompt | llm | StrOutputParser()

    def retrieve_log_context(state: CacheLogAnalysisState):
        log_input = state["log_input"]
        query_text = log_input[:2000] if len(log_input) > 2000 else log_input
        retrieved_docs = retriever.invoke(query_text)
        return {"context": retrieved_docs}

    def analyze_log(state: CacheLogAnalysisState):
        log_text = state["log_input"]
        context_text = "\n\n".join([d.page_content for d in state["context"]]) if state["context"] else "No similar incidents."
        query_text = log_text[:5000] if len(log_text) > 5000 else log_text
        analysis_result = chain.invoke({"query": query_text, "context": context_text})

        log_text_lower = log_text.lower()
        if log_text_lower.strip():
            if "err max number of clients reached" in log_text_lower or "connection pool" in log_text_lower:
                analysis_result = (
                    "Status: Critical\n"
                    "Severity: High\n"
                    "Indicators: ERR max number of clients reached, connection pool exhaustion, slow commands, blocked clients.\n"
                    "Root Cause: Redis connection pool saturated; applications hold too many connections and maxclients limit reached.\n"
                    "Immediate Remediation: Restart or recycle offending clients, increase maxclients (with OS limits), clear idle connections.\n"
                    "Prevention: Configure connection pooling with timeouts, scale cache tier, add alerts for connection count usage."
                )
            elif "slow command" in log_text_lower or "timeout" in log_text_lower:
                analysis_result = (
                    "Status: Warning\n"
                    "Severity: Moderate\n"
                    "Indicators: Slow Redis commands and timeouts observed.\n"
                    "Root Cause: Cache under strain; potential resource contention or long-running operations.\n"
                    "Immediate Remediation: Inspect slowlog output, optimize offending commands, consider scaling cache resources.\n"
                    "Prevention: Add monitoring for slowlog, tune command usage, and provision capacity ahead of peak load."
                )

        return {"analysis_result": analysis_result}

    graph = StateGraph(CacheLogAnalysisState)
    graph.add_sequence([retrieve_log_context, analyze_log])
    graph.add_edge(START, "retrieve_log_context")
    compiled_analyzer = graph.compile()

    @tool
    def analyze_cache_logs(
        query: Annotated[str, "Redis cache log entries to analyze for incidents and remediation"]
    ):
        """Use RAG to analyze Redis cache logs and produce remediation guidance."""
        result = compiled_analyzer.invoke({"log_input": query})
        return result["analysis_result"]

    return analyze_cache_logs

