"""
Runbook RAG Service - Search runbooks with metadata extraction

This service uses the existing ensemble retriever to search runbooks
and extracts structured information (action titles, steps, source URLs) for display.
"""
from typing import List, Dict, Optional
import json

# Cache for database components (singleton pattern)
_cached_vector_store = None
_cached_chunked_docs = None
_cached_ensemble_retriever = None

# Lazy imports to avoid loading database on startup
def _get_ensemble_retriever():
    from src.rag.ensemble_retriever import create_ensemble_retriever
    return create_ensemble_retriever

def _get_database_components():
    from src.utils.database_utils import create_database_components
    return create_database_components

def _get_model_factory():
    from src.utils.config import get_model_factory
    return get_model_factory

def _get_chat_prompt_template():
    from langchain_core.prompts import ChatPromptTemplate
    return ChatPromptTemplate

def _get_or_create_database_components():
    """Get cached database components or create them once"""
    global _cached_vector_store, _cached_chunked_docs
    
    if _cached_vector_store is None or _cached_chunked_docs is None:
        create_database_components = _get_database_components()
        _cached_vector_store, _cached_chunked_docs = create_database_components()
        print("✅ Database components initialized and cached")
    
    return _cached_vector_store, _cached_chunked_docs


async def search_runbooks_with_metadata(
    rca_recommendations: List[str],
    root_cause: str,
    max_results: int = 5
) -> List[Dict]:
    """
    Search runbooks using RCA recommendations and return full content results.
    """
    recommendations_text = ", ".join(rca_recommendations)
    search_query = f"{root_cause}. Recommended actions: {recommendations_text}"

    vector_store, chunked_docs = _get_or_create_database_components()

    global _cached_ensemble_retriever
    if _cached_ensemble_retriever is None:
        get_model_factory = _get_model_factory()
        create_ensemble_retriever = _get_ensemble_retriever()
        model_factory = get_model_factory()

        _cached_ensemble_retriever = create_ensemble_retriever(
            vector_store, chunked_docs, model_factory,
            naive_k=3, bm25_k=12, rerank_k=max_results
        )
        print("✅ Ensemble retriever initialized and cached")

    ensemble_retriever = _cached_ensemble_retriever

    retrieved_docs = ensemble_retriever.invoke(search_query)

    structured_results = []
    seen_urls = set()
    for doc in retrieved_docs:
        source_url = doc.metadata.get('source', '')
        doc_title = doc.metadata.get('title', 'Unknown')

        if source_url and not source_url.startswith('http'):
            if 'runbooks' in source_url.lower() or source_url.startswith('/'):
                source_url = (
                    f"https://runbooks.gitlab.com{source_url}"
                    if source_url.startswith('/')
                    else f"https://runbooks.gitlab.com/{source_url}"
                )
            else:
                source_url = f"https://runbooks.gitlab.com/{source_url}"

        if source_url in seen_urls:
            continue

        structured_results.append({
            'action_title': doc_title,
            'source_document': doc_title,
            'source_url': source_url,
            'relevance_score': doc.metadata.get('score', 0.0),
            'tags': doc.metadata.get('tags', []),
        })

        seen_urls.add(source_url)
        if len(structured_results) >= max_results:
            break

    return structured_results

