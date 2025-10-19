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

def get_rag_prompt():
    """Get the RAG prompt template as a ChatPromptTemplate"""
    return ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
