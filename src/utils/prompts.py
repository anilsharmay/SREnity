"""
Centralized prompt templates for SREnity RAG system
"""
from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT_TEMPLATE = """
You are a Redis expert helping SREs find the right procedures. Based on the question and relevant runbook documentation, provide a clear, step-by-step answer.

**Question:**
{question}

**Relevant Runbook Documentation:**
{context}

**Please provide:**
1. **Direct Answer** - Clear response to the question
2. **Step-by-Step Instructions** - Detailed procedure from the runbooks
3. **Key Commands** - Specific commands or configurations needed
4. **Important Notes** - Warnings, prerequisites, or additional context

Format your response clearly with headers and numbered steps.
"""

ENSEMBLE_COMBINATION_PROMPT_TEMPLATE = """
You are an expert SRE helping to resolve production incidents. You have two different responses to the same question:

**Question:** {question}

**Response 1 (Vector Similarity):**
{naive_response}

**Response 2 (BM25 + Reranker):**
{bm25_response}

**Context from Vector Similarity:**
{naive_contexts}

**Context from BM25 + Reranker:**
{bm25_contexts}

Please provide the best possible answer by combining insights from both responses. 
Prioritize accuracy and completeness. If one response is clearly better, use that as primary.
If both have valuable information, synthesize them into a comprehensive answer.

Provide:
1. **Direct Answer** - Clear response to the question
2. **Step-by-Step Instructions** - Detailed procedure
3. **Key Commands** - Specific commands or configurations
4. **Important Notes** - Warnings, prerequisites, or additional context

Format your response clearly with headers and numbered steps.
"""

def get_rag_prompt():
    """Get the RAG prompt template as a ChatPromptTemplate"""
    return ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

def get_ensemble_combination_prompt():
    """Get the ensemble combination prompt template as a ChatPromptTemplate"""
    return ChatPromptTemplate.from_template(ENSEMBLE_COMBINATION_PROMPT_TEMPLATE)
