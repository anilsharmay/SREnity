"""
Naive retrieval implementation - Vector similarity search
For SREnity RAG Pipeline Evaluation
"""
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from operator import itemgetter
from src.utils.prompts import get_rag_prompt

def create_naive_retriever(vector_store, k=3):
    """Create a proper LangChain retriever from vector store"""
    return vector_store.as_retriever(search_kwargs={"k": k})

def create_naive_retrieval_chain(vector_store, model_factory, k=3):
    """Create a Runnable chain for naive retrieval"""
    
    # Create retriever and model
    naive_retriever = create_naive_retriever(vector_store, k)
    chat_model = model_factory.get_llm()
    
    # Use centralized RAG prompt template
    rag_prompt = get_rag_prompt()
    
    # Create the chain - functional composition
    naive_retrieval_chain = (
        # Input: {"question": "user question"}
        # Output: {"docs": [Document], "question": "user question"}
        {"docs": itemgetter("question") | naive_retriever, "question": itemgetter("question")}
        # Generate response and extract contexts in one pass
        | RunnablePassthrough.assign(
            response=lambda x: chat_model.invoke(
                rag_prompt.format(
                    question=x["question"],
                    context="\n\n".join([doc.page_content for doc in x["docs"]])
                )
            ).content,
            contexts=lambda x: [doc.page_content for doc in x["docs"]]  # Extract contexts as strings
        )
    )
    
    return naive_retrieval_chain
