"""
Web tier RAG tool for analyzing web server logs.
Extracted from web_worker.py
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


class WebLogAnalysisState(TypedDict):
    """State for web log RAG analysis"""
    log_input: str
    context: List[Document]
    analysis_result: str


def create_web_rag_tool():
    """
    Create a RAG tool for web log analysis.
    Reuses pattern from web_worker.py
    """
    # Load knowledge base for web tier
    # Get backend directory and find knowledge base
    current_file = os.path.abspath(__file__)
    tools_dir = os.path.dirname(current_file)
    analysis_dir = os.path.dirname(tools_dir)
    backend_dir = os.path.dirname(analysis_dir)
    web_kb_path = os.path.join(backend_dir, "data", "knowledge_base", "web")
    
    web_docs = []
    if os.path.isdir(web_kb_path):
        loader = DirectoryLoader(web_kb_path, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
        web_docs = loader.load()
        web_docs = [doc for doc in web_docs if doc.page_content and doc.page_content.strip()]
    else:
        raise FileNotFoundError(f"Web knowledge base directory not found. Checked: {web_kb_path}")
    
    if not web_docs:
        raise ValueError(f"No documents with content loaded from {web_kb_path}.")
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", chunk_size=100)
    vectorstore = Qdrant.from_documents(web_docs, embeddings, location=":memory:", batch_size=10)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    # Create RAG chain
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a WEB tier log analyst. First determine if logs contain errors or are healthy. INFO level logs with successful requests indicate healthy state."),
        ("human", "Analyze the logs carefully:\n\nLogs:\n{query}\n\nContext:\n{context}\n\n**First check if logs contain errors:**\n- Look for [ERROR], [WARN], 502, 503, 504, timeouts, connection errors, or any issues\n- Check if logs are only [INFO] with successful operations (e.g., '200 OK', 'Request completed successfully')\n\n**If logs are HEALTHY (only [INFO], successful requests, normal processing):**\n1. Status: Healthy\n2. Severity: None/Low\n3. Summary: All operations successful, no errors detected\n4. Optional: Brief performance summary if relevant\n\n**If logs contain ERRORS:**\n1. Error type and severity\n2. Root cause analysis\n3. Immediate remediation steps\n4. Prevention recommendations")
    ])
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = prompt | llm | StrOutputParser()
    
    def retrieve_log_context(state: WebLogAnalysisState):
        # Extract only web logs for faster retrieval
        log_input = state["log_input"]
        web_logs = log_input
        if "=== WEB TIER LOGS ===" in log_input:
            parts = log_input.split("=== WEB TIER LOGS ===")
            if len(parts) > 1:
                web_section = parts[1].split("===")[0]
                web_logs = f"=== WEB TIER LOGS ==={web_section}"
        query_text = web_logs[:2000] if len(web_logs) > 2000 else web_logs
        retrieved_docs = retriever.invoke(query_text)
        return {"context": retrieved_docs}
    
    def analyze_log(state: WebLogAnalysisState):
        context_text = "\n\n".join([d.page_content for d in state["context"]]) if state["context"] else "No similar incidents."
        log_input = state["log_input"]
        web_logs = log_input
        if "=== WEB TIER LOGS ===" in log_input:
            parts = log_input.split("=== WEB TIER LOGS ===")
            if len(parts) > 1:
                web_section = parts[1].split("===")[0]
                web_logs = f"=== WEB TIER LOGS ==={web_section}"
        query_text = web_logs[:5000] if len(web_logs) > 5000 else web_logs
        analysis_result = chain.invoke({"query": query_text, "context": context_text})
        return {"analysis_result": analysis_result}
    
    # Build graph
    graph = StateGraph(WebLogAnalysisState)
    graph.add_sequence([retrieve_log_context, analyze_log])
    graph.add_edge(START, "retrieve_log_context")
    compiled_analyzer = graph.compile()
    
    @tool
    def analyze_web_logs(
        query: Annotated[str, "web server log entries to analyze for incidents and remediation"]
    ):
        """Use Retrieval Augmented Generation to analyze web server logs and provide incident insights"""
        result = compiled_analyzer.invoke({"log_input": query})
        return result["analysis_result"]
    
    return analyze_web_logs

