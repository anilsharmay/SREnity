"""
SREnity Agent Tools

This module contains the tools used by the SRE agent for runbook search and web search.
"""

from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from src.rag.ensemble_retriever import create_ensemble_retriever, create_ensemble_retrieval_chain
from src.utils.config import get_config, get_model_factory
from src.utils.database_utils import create_database_components


# Global cache for the Ensemble retriever chain
_cached_chain = None

def initialize_tools_with_database(vector_store, chunked_docs):
    """Initialize tools with pre-created database components"""
    global _cached_chain
    
    print("🔄 Initializing tools with provided database...")
    config = get_config()
    model_factory = get_model_factory()
    
    ensemble_retriever = create_ensemble_retriever(
        vector_store, chunked_docs, model_factory, 
        naive_k=3, bm25_k=12, rerank_k=4
    )
    _cached_chain = create_ensemble_retrieval_chain(ensemble_retriever, model_factory)
    print("✅ Tools initialized with database")

def _get_ensemble_chain():
    """Get or create the Ensemble retriever chain for runbook search (with caching)"""
    global _cached_chain
    
    # Return cached chain if it exists
    if _cached_chain is not None:
        return _cached_chain
    
    print("🔄 Initializing ensemble chain (this may take a moment)...")
    
    # Create database components and initialize tools
    vector_store, chunked_docs = create_database_components()
    initialize_tools_with_database(vector_store, chunked_docs)
    
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
        ensemble_chain = _get_ensemble_chain()
        result = ensemble_chain.invoke({"question": query})
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

# Export functions for external use
__all__ = ['TOOLS', 'search_runbooks', 'search_web', 'initialize_tools_with_database', 'create_database_components']
