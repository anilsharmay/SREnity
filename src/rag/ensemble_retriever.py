"""
Ensemble retrieval implementation - Combines existing chains
For SREnity RAG Pipeline Evaluation
"""
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from operator import itemgetter
from src.utils.prompts import get_rag_prompt, get_ensemble_combination_prompt

def create_ensemble_chain(naive_chain, bm25_reranker_chain, weights=[0.5, 0.5]):
    """
    Create ensemble chain that combines results from existing chains
    
    Args:
        naive_chain: Vector similarity chain
        bm25_reranker_chain: BM25 + Reranker chain  
        weights: [naive_weight, bm25_weight] - default [0.5, 0.5]
    
    Returns:
        Runnable chain that combines both approaches
    """
    
    def ensemble_invoke(inputs):
        """Run both chains and combine their results"""
        question = inputs["question"]
        
        # Run both chains in parallel
        naive_result = naive_chain.invoke({"question": question})
        bm25_result = bm25_reranker_chain.invoke({"question": question})
        
        # Combine contexts based on weights
        naive_contexts = naive_result.get('contexts', [])
        bm25_contexts = bm25_result.get('contexts', [])
        
        # Weight the number of contexts from each chain
        naive_count = int(len(naive_contexts) * weights[0])
        bm25_count = int(len(bm25_contexts) * weights[1])
        
        # Combine contexts (naive first, then BM25)
        combined_contexts = []
        combined_contexts.extend(naive_contexts[:naive_count])
        combined_contexts.extend(bm25_contexts[:bm25_count])
        
        # For response, we could:
        # 1. Use the better response (based on some criteria)
        # 2. Combine both responses
        # 3. Use naive as primary (since it has better precision)
        
        # Strategy: Use naive response as primary (better precision)
        # but include BM25 contexts for better recall
        ensemble_response = naive_result.get('response', '')
        
        return {
            'response': ensemble_response,
            'contexts': combined_contexts,
            'naive_response': naive_result.get('response', ''),
            'bm25_response': bm25_result.get('response', ''),
            'naive_contexts': naive_contexts,
            'bm25_contexts': bm25_contexts
        }
    
    # Create a RunnableLambda that can be invoked like other chains
    return RunnableLambda(ensemble_invoke)

def create_ensemble_chain_with_llm_combination(naive_chain, bm25_reranker_chain, model_factory, weights=[0.5, 0.5]):
    """
    Create ensemble chain that uses LLM to combine responses from both chains
    
    This is more sophisticated - it runs both chains and uses an LLM to synthesize
    the best answer from both responses and contexts.
    """
    from langchain_core.prompts import ChatPromptTemplate
    
    def ensemble_invoke_with_llm(inputs):
        """Run both chains and use LLM to combine responses"""
        question = inputs["question"]
        
        # Run both chains
        naive_result = naive_chain.invoke({"question": question})
        bm25_result = bm25_reranker_chain.invoke({"question": question})
        
        # Get LLM to combine the responses
        chat_model = model_factory.get_llm()
        
        # Use centralized ensemble combination prompt
        combination_prompt = get_ensemble_combination_prompt()
        
        # Combine contexts for the LLM
        all_contexts = naive_result.get('contexts', []) + bm25_result.get('contexts', [])
        
        combined_response = chat_model.invoke(
            combination_prompt.format(
                question=question,
                naive_response=naive_result.get('response', ''),
                bm25_response=bm25_result.get('response', ''),
                naive_contexts='\n\n'.join(naive_result.get('contexts', [])),
                bm25_contexts='\n\n'.join(bm25_result.get('contexts', []))
            )
        ).content
        
        return {
            'response': combined_response,
            'contexts': all_contexts,
            'naive_response': naive_result.get('response', ''),
            'bm25_response': bm25_result.get('response', ''),
            'naive_contexts': naive_result.get('contexts', []),
            'bm25_contexts': bm25_result.get('contexts', [])
        }
    
    return RunnableLambda(ensemble_invoke_with_llm)

def create_ensemble_retriever(vector_store, chunked_docs, model_factory, naive_k=3, bm25_k=12, rerank_k=4):
    """
    Create ensemble retriever that combines naive vector and BM25+reranker
    
    Args:
        vector_store: Qdrant vector store
        chunked_docs: List of chunked documents
        model_factory: Model factory instance
        naive_k: Number of docs for naive retriever
        bm25_k: Number of docs for BM25 retriever
        rerank_k: Number of docs after reranking
    
    Returns:
        EnsembleRetriever instance
    """
    from langchain.retrievers import EnsembleRetriever
    from src.rag.naive_retriever import create_naive_retriever
    from src.rag.bm25_reranker_retriever import create_bm25_reranker_retriever
    
    # Create individual retrievers
    naive_retriever = create_naive_retriever(vector_store, k=naive_k)
    bm25_reranker_retriever = create_bm25_reranker_retriever(chunked_docs, bm25_k, rerank_k)
    
    # Create ensemble retriever
    ensemble_retriever = EnsembleRetriever(
        retrievers=[naive_retriever, bm25_reranker_retriever],
        weights=[0.5, 0.5]  # Equal weights
    )
    
    return ensemble_retriever

def create_ensemble_retrieval_chain(ensemble_retriever, model_factory):
    """
    Create full RAG chain with ensemble retriever
    
    Args:
        ensemble_retriever: EnsembleRetriever instance
        model_factory: Model factory instance
    
    Returns:
        Runnable chain for ensemble retrieval
    """
    from langchain_core.runnables import RunnablePassthrough
    from operator import itemgetter
    
    # Get the RAG prompt (same as other retrievers)
    rag_prompt = get_rag_prompt()
    
    # Get the chat model
    chat_model = model_factory.get_llm()
    
    # Create the ensemble retrieval chain
    def extract_content(message):
        """Extract content from AIMessage"""
        if hasattr(message, 'content'):
            return message.content
        return str(message)
    
    ensemble_chain = (
        {"context": itemgetter("question") | ensemble_retriever, "question": itemgetter("question")}
        | RunnablePassthrough.assign(
            response=lambda x: chat_model.invoke(
                rag_prompt.format(
                    question=x["question"],
                    context="\n\n".join([doc.page_content for doc in x["context"]])
                )
            ).content,
            contexts=lambda x: [doc.page_content for doc in x["context"]]
        )
    )
    
    return ensemble_chain
