"""
Ensemble retrieval implementation - Combines existing chains
For SREnity RAG Pipeline Evaluation
"""
from langchain_core.runnables import RunnableLambda
from src.utils.prompts import get_rag_prompt

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
        
        combination_prompt = ChatPromptTemplate.from_template("""
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
        """)
        
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
