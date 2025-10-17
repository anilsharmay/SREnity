"""
Advanced Retrieval Implementation - BM25 + Reranker
For SREnity RAG Pipeline Evaluation
"""

from langchain.retrievers import BM25Retriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.config import get_config, get_model_factory

print("Advanced retrieval module loaded with rerank-v3.5")


def create_bm25_reranker_chain(chunked_docs, model_factory, bm25_k=12, rerank_k=3):
    """Create BM25 + Reranker chain with optimal parameters"""
    config = get_config()
    
    if not config.cohere_api_key:
        print("COHERE_API_KEY not found in environment variables")
        print("Please add COHERE_API_KEY to your .env file")
        return None
    
    print("Creating BM25 + Reranker chain...")
    
    # Step 1: Create BM25 retriever
    print(f"Creating BM25 retriever from {len(chunked_docs)} documents...")
    bm25_retriever = BM25Retriever.from_documents(
        documents=chunked_docs,
        k=bm25_k  # Retrieve 12 candidates with BM25
    )
    print(f"BM25 retriever created (k={bm25_k})")
    
    # Step 2: Create Cohere reranker
    compressor = CohereRerank(
        cohere_api_key=config.cohere_api_key,
        model="rerank-v3.5",  # Use the correct model name
        top_n=rerank_k  # Return top 3 after reranking
    )
    
    # Step 3: Combine BM25 + Reranker
    reranked_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=bm25_retriever
    )
    
    # Step 4: Create the chain that returns both response AND contexts
    chat_model = model_factory.get_llm()
    
    # Same prompt as naive retrieval for fair comparison
    prompt = ChatPromptTemplate.from_template("""
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
""")
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # Create chain that returns both response and contexts (same format as naive chain)
    def run_chain(inputs):
        # Get contexts
        contexts = reranked_retriever.invoke(inputs["question"])
        
        # Format contexts for prompt
        formatted_context = format_docs(contexts)
        
        # Generate response
        response = chat_model.invoke(prompt.format_messages(
            context=formatted_context,
            question=inputs["question"]
        )).content
        
        # Extract context strings
        context_strings = [doc.page_content for doc in contexts]
        
        return {
            "response": response,
            "contexts": context_strings
        }
    
    # Create Runnable that matches naive chain format
    from langchain_core.runnables import RunnableLambda
    bm25_reranker_chain = RunnableLambda(run_chain)
    
    print(f"BM25 + Reranker chain created (BM25 k={bm25_k}, Rerank k={rerank_k})")
    return bm25_reranker_chain


def create_advanced_retrieval_chain(chunked_docs, model_factory):
    """Create BM25 + Reranker chain"""
    print("Creating BM25 + Reranker chain...")
    
    bm25_reranker_chain = create_bm25_reranker_chain(
        chunked_docs, 
        model_factory, 
        bm25_k=12,  # Retrieve 12 candidates
        rerank_k=3   # Return top 3 after reranking
    )
    
    return bm25_reranker_chain