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
    max_results: int = 3
) -> List[Dict]:
    """
    Search runbooks using RCA recommendations and return structured results with metadata
    
    Args:
        rca_recommendations: List of resolution recommendations from RCA
        root_cause: Root cause description
        max_results: Maximum number of runbook results to return
    
    Returns:
        List of dicts with:
        - action_title: Extracted action title
        - steps: List of actionable steps
        - source_document: Document name/title
        - source_url: URL to runbook document
        - relevance_score: Relevance score (if available)
        - raw_content: Original retrieved content (truncated)
    """
    # Build search query from RCA
    recommendations_text = ", ".join(rca_recommendations)
    search_query = f"{root_cause}. Recommended actions: {recommendations_text}"
    
    # Get cached database components (singleton - only initialized once)
    vector_store, chunked_docs = _get_or_create_database_components()
    
    # Get or create ensemble retriever (cache it too)
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
    
    # Retrieve documents
    retrieved_docs = ensemble_retriever.invoke(search_query)
    
    # Process each document to extract structured information
    structured_results = []
    for doc in retrieved_docs[:max_results]:
        # Extract metadata
        source_url = doc.metadata.get('source', '')
        doc_title = doc.metadata.get('title', 'Unknown')
        
        # Construct full URL if source is a path
        if source_url and not source_url.startswith('http'):
            # Try to construct GitLab runbook URL
            # If source is like "runbooks/cloud-sql/..." convert to full URL
            if 'runbooks' in source_url.lower() or source_url.startswith('/'):
                source_url = f"https://runbooks.gitlab.com{source_url}" if source_url.startswith('/') else f"https://runbooks.gitlab.com/{source_url}"
            else:
                # Fallback: try to construct from title/path
                source_url = f"https://runbooks.gitlab.com/{source_url}"
        
        # Extract action title and steps from content
        action_data = extract_action_from_runbook(doc.page_content, search_query)
        
        structured_results.append({
            'action_title': action_data.get('title', doc_title),
            'steps': action_data.get('steps', []),
            'source_document': doc_title,
            'source_url': source_url,
            'relevance_score': doc.metadata.get('score', 0.0),  # If available from retriever
            'raw_content': doc.page_content[:500]  # Truncate for reference
        })
    
    return structured_results


def extract_action_from_runbook(content: str, context: str) -> Dict:
    """
    Use LLM to extract actionable title and steps from runbook content
    
    Args:
        content: Runbook content (truncated to avoid token limits)
        context: Search context/query
    
    Returns:
        {
            'title': 'Action title',
            'steps': ['Step 1', 'Step 2', ...]
        }
    """
    try:
        get_model_factory = _get_model_factory()
        ChatPromptTemplate = _get_chat_prompt_template()
        
        model_factory = get_model_factory()
        model = model_factory.get_llm()
        
        # Truncate content to avoid token limits (keep first 2000 chars)
        truncated_content = content[:2000]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are extracting actionable information from SRE runbook content.
            
Based on the context query and runbook content, extract:
1. A clear, concise action title (what needs to be done)
2. A list of specific numbered steps or key actions from the runbook

Return ONLY valid JSON in this format:
{
    "title": "Action title",
    "steps": ["Step 1 description", "Step 2 description", ...]
}

If steps are not clearly numbered, extract the main actions as a list.
Limit steps to 5-7 most important ones."""),
            ("user", f"Context: {context}\n\nRunbook content:\n{truncated_content}")
        ])
        
        response = model.invoke(prompt.format_messages(context=context, content=truncated_content))
        
        # Parse JSON response
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        # Try to extract JSON from response (might be wrapped in markdown code blocks)
        if '```json' in response_text:
            json_start = response_text.find('```json') + 7
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        elif '```' in response_text:
            json_start = response_text.find('```') + 3
            json_end = response_text.find('```', json_start)
            response_text = response_text[json_start:json_end].strip()
        
        result = json.loads(response_text)
        return {
            'title': result.get('title', 'Runbook Procedure'),
            'steps': result.get('steps', [])
        }
        
    except Exception as e:
        # Fallback: extract basic steps from content
        print(f"Error extracting action from runbook: {e}")
        steps = []
        lines = content.split('\n')
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            # Look for numbered steps or bullet points
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                # Clean up the step text
                step = line.lstrip('0123456789.-* ').strip()
                if step and len(step) > 10:  # Only include substantial steps
                    steps.append(step)
                    if len(steps) >= 7:
                        break
        
        return {
            'title': 'Runbook Procedure',
            'steps': steps if steps else ['Review runbook content for detailed steps']
        }

