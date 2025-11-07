"""
Application tier RAG tool for analyzing application logs.
Extracted from app_worker.py
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


class AppLogAnalysisState(TypedDict):
    """State for app log RAG analysis"""
    log_input: str
    context: List[Document]
    analysis_result: str


def create_app_rag_tool():
    """
    Create a RAG tool for app log analysis.
    Reuses pattern from app_worker.py
    """
    # Load knowledge base for app tier
    # Get backend directory and find knowledge base
    current_file = os.path.abspath(__file__)
    tools_dir = os.path.dirname(current_file)
    analysis_dir = os.path.dirname(tools_dir)
    backend_dir = os.path.dirname(analysis_dir)
    app_kb_path = os.path.join(backend_dir, "data", "knowledge_base", "app")
    
    app_docs = []
    if os.path.isdir(app_kb_path):
        loader = DirectoryLoader(app_kb_path, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
        app_docs = loader.load()
        app_docs = [doc for doc in app_docs if doc.page_content and doc.page_content.strip()]
    else:
        raise FileNotFoundError(f"App knowledge base directory not found. Checked: {app_kb_path}")
    
    if not app_docs:
        raise ValueError(f"No documents with content loaded from {app_kb_path}.")
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", chunk_size=100)
    vectorstore = Qdrant.from_documents(app_docs, embeddings, location=":memory:", batch_size=10)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    
    # Create RAG chain
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an APPLICATION tier log analyst. First determine if logs contain errors or are healthy. INFO level logs with successful operations indicate healthy state."),
        ("human", "Analyze the logs carefully:\n\nLogs:\n{query}\n\nContext:\n{context}\n\n**First check if logs contain errors:**\n- Look for [ERROR], [WARN], exceptions, failures, timeouts, or any issues\n- Check if logs are only [INFO] with successful operations (e.g., 'Processing request', 'Request completed successfully')\n\n**If logs are HEALTHY (only [INFO], successful operations, normal processing):**\n1. Status: Healthy\n2. Severity: None/Low\n3. Summary: All operations successful, no errors detected\n4. Optional: Brief performance summary if relevant\n\n**If logs contain ERRORS:**\n1. Error type and severity\n2. Root cause analysis\n3. Immediate remediation steps\n4. Prevention recommendations")
    ])
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    chain = prompt | llm | StrOutputParser()
    
    def retrieve_log_context(state: AppLogAnalysisState):
        # Extract only app logs for faster retrieval
        log_input = state["log_input"]
        app_logs = log_input
        if "=== APP TIER LOGS ===" in log_input:
            parts = log_input.split("=== APP TIER LOGS ===")
            if len(parts) > 1:
                app_section = parts[1].split("===")[0]
                app_logs = f"=== APP TIER LOGS ==={app_section}"
        query_text = app_logs[:2000] if len(app_logs) > 2000 else app_logs
        retrieved_docs = retriever.invoke(query_text)
        return {"context": retrieved_docs}
    
    def analyze_log(state: AppLogAnalysisState):
        context_text = "\n\n".join([d.page_content for d in state["context"]]) if state["context"] else "No similar incidents."
        log_input = state["log_input"]
        app_logs = log_input
        if "=== APP TIER LOGS ===" in log_input:
            parts = log_input.split("=== APP TIER LOGS ===")
            if len(parts) > 1:
                app_section = parts[1].split("===")[0]
                app_logs = f"=== APP TIER LOGS ==={app_section}"
        query_text = app_logs[:5000] if len(app_logs) > 5000 else app_logs
        analysis_result = chain.invoke({"query": query_text, "context": context_text})
        return {"analysis_result": analysis_result}
    
    # Build graph
    graph = StateGraph(AppLogAnalysisState)
    graph.add_sequence([retrieve_log_context, analyze_log])
    graph.add_edge(START, "retrieve_log_context")
    compiled_analyzer = graph.compile()
    
    @tool
    def analyze_app_logs(
        query: Annotated[str, "application log entries to analyze for incidents and remediation"]
    ):
        """Use Retrieval Augmented Generation to analyze application logs and provide incident insights"""
        result = compiled_analyzer.invoke({"log_input": query})
        return result["analysis_result"]
    
    return analyze_app_logs
