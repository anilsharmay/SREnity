"""
SREnity Agent Tools

This module contains the tools used by the SRE agent for runbook search and web search.
"""

from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from src.rag.advanced_retrieval import create_bm25_reranker_chain
from src.utils.config import get_config, get_model_factory
from src.utils.document_loader import load_saved_documents, preprocess_html_documents
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken


def filter_by_service(documents, services=['redis']):
    """Filter documents by service type"""
    filtered = []
    for doc in documents:
        source = doc.metadata.get('source', '').lower()
        if any(service in source for service in services):
            filtered.append(doc)
    return filtered


# Global cache for the BM25 + Reranker chain
_cached_chain = None

def _get_bm25_reranker_chain():
    """Get or create the BM25 + Reranker chain for runbook search (with caching)"""
    global _cached_chain
    
    # Return cached chain if it exists
    if _cached_chain is not None:
        return _cached_chain
    
    print("🔄 Initializing BM25 + Reranker chain (this may take a moment)...")
    
    # Load configuration
    config = get_config()
    model_factory = get_model_factory()
    
    # Load documents
    documents = load_saved_documents()
    print(f"📚 Loaded {len(documents)} documents")
    
    # Filter to Redis services only for focused responses
    documents = filter_by_service(documents, ['redis'])
    print(f"🔍 Filtered to {len(documents)} Redis documents")
    
    # Preprocess HTML documents to markdown
    print("🔄 Preprocessing documents...")
    processed_documents = preprocess_html_documents(documents)
    
    # Chunk documents with tiktoken
    def chunk_documents_with_tiktoken(documents, chunk_size=1000, chunk_overlap=200):
        encoding = tiktoken.encoding_for_model(config.openai_model)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=lambda text: len(encoding.encode(text)),
            separators=["\n\n", "\n", " ", ""]
        )
        return text_splitter.split_documents(documents)
    
    print("🔄 Chunking documents...")
    chunked_docs = chunk_documents_with_tiktoken(processed_documents, chunk_size=1000, chunk_overlap=200)
    print(f"📄 Created {len(chunked_docs)} chunks")
    
    # Create BM25 + Reranker chain
    print("🔄 Creating BM25 + Reranker chain...")
    _cached_chain = create_bm25_reranker_chain(chunked_docs, model_factory, bm25_k=12, rerank_k=5)
    print("✅ BM25 + Reranker chain ready!")
    
    return _cached_chain


@tool
def search_runbooks(query: str) -> str:
    """
    Search GitLab SRE runbooks for troubleshooting procedures, commands, and best practices.
    
    Use this tool for:
    - Standard SRE procedures
    - Troubleshooting steps
    - Command syntax and usage
    - Infrastructure best practices
    
    Args:
        query: The SRE question or issue to search for
    
    Returns:
        Formatted response with runbook guidance
    """
    try:
        bm25_reranker_chain = _get_bm25_reranker_chain()
        result = bm25_reranker_chain.invoke({"question": query})
        return result["response"]
    except Exception as e:
        return f"Error searching runbooks: {str(e)}"


@tool
def search_web(query: str) -> str:
    """
    Search the web for latest updates, CVEs, version-specific issues, and recent changes.
    
    Use this tool for:
    - Recent vulnerabilities or security updates
    - Version-specific issues not in runbooks
    - Latest best practices or changes
    - Breaking changes in tools or services
    
    Args:
        query: The technical question to search for on the web
    
    Returns:
        Recent web information and updates
    """
    try:
        # Initialize Tavily search
        tavily_tool = TavilySearchResults(
            max_results=3,
            search_depth="advanced"
        )
        
        # Search with the raw query
        search_query = query
        results = tavily_tool.invoke(search_query)
        
        # Format results
        if results:
            formatted_results = "\n\n".join([
                f"**Source:** {result.get('title', 'Unknown')}\n"
                f"**URL:** {result.get('url', 'N/A')}\n"
                f"**Content:** {result.get('content', 'No content available')}"
                for result in results
            ])
            return f"""
**SOURCE NOTICE**: This information was not available in our current runbooks and was retrieved from recent web sources.

{formatted_results}

**IMPORTANT**: This information comes from external web sources, not from our internal runbooks.
"""
        else:
            return """**SOURCE NOTICE**: This information was not available in our current runbooks. No recent web information found for this query.

**IMPORTANT**: This information comes from external web sources, not from our internal runbooks."""
            
    except Exception as e:
        return f"Error searching web: {str(e)}"


# Export tools list
TOOLS = [search_runbooks, search_web]
