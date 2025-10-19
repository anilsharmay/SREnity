"""
Advanced Retrieval Implementation - BM25 + Reranker
For SREnity RAG Pipeline Evaluation
"""

from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.config import get_config, get_model_factory
from src.utils.prompts import get_rag_prompt

print("Advanced retrieval module loaded with rerank-v3.5")


def create_bm25_reranker_retriever(chunked_docs, bm25_k=12, rerank_k=3):
    """Create BM25 + Reranker retriever"""
    config = get_config()
    
    if not config.cohere_api_key:
        print("COHERE_API_KEY not found in environment variables")
        print("Please add COHERE_API_KEY to your .env file")
        return None
    
    print("Creating BM25 + Reranker retriever...")
    
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
    
    print(f"BM25 + Reranker retriever created (BM25 k={bm25_k}, Rerank k={rerank_k})")
    return reranked_retriever


def create_bm25_reranker_chain(chunked_docs, model_factory, bm25_k=12, rerank_k=3):
    """Create BM25 + Reranker chain using the retriever"""
    
    # Create retriever using the new function
    reranked_retriever = create_bm25_reranker_retriever(chunked_docs, bm25_k, rerank_k)
    
    if reranked_retriever is None:
        return None
    
    print("Creating BM25 + Reranker chain...")
    
    # Create the chain using functional composition (same pattern as naive chain)
    from langchain_core.runnables import RunnablePassthrough
    from operator import itemgetter
    
    chat_model = model_factory.get_llm()
    rag_prompt = get_rag_prompt()
    
    # Create chain using functional composition pattern
    bm25_reranker_chain = (
        {"context": itemgetter("question") | reranked_retriever, "question": itemgetter("question")}
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