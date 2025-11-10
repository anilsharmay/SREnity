"""
Database utilities for SREnity
Centralizes vector database creation, loading, and management
"""

from pathlib import Path
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

from src.utils.config import get_config, get_model_factory
from src.utils.document_loader import load_saved_documents, preprocess_html_documents


def filter_by_service(documents, services=['redis']):
    """Filter documents by service type"""
    filtered = []
    for doc in documents:
        source = doc.metadata.get('source', '').lower()
        if any(service in source for service in services):
            filtered.append(doc)
    return filtered


def chunk_documents_with_tiktoken(documents, chunk_size=1000, chunk_overlap=200):
    """Chunk documents using tiktoken encoding"""
    config = get_config()
    encoding = tiktoken.encoding_for_model(config.openai_model)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=lambda text: len(encoding.encode(text)),
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)


def create_vector_store(chunked_docs):
    """Create new vector store"""
    config = get_config()
    model_factory = get_model_factory()
    
    print(f"Creating vector store at: {config.qdrant_url}")
    print(f"Using collection name: {config.qdrant_collection_name}")
    
    embeddings = model_factory.get_embeddings()
    vector_store = Qdrant.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        path=config.qdrant_url,
        collection_name=config.qdrant_collection_name
    )
    
    print(f"Stored {len(chunked_docs)} chunks in Qdrant at {config.qdrant_url}")
    return vector_store


def load_existing_vector_store():
    """Load existing vector store"""
    config = get_config()
    model_factory = get_model_factory()
    
    embeddings = model_factory.get_embeddings()
    vector_store = Qdrant.from_existing_collection(
        embedding=embeddings,
        path=config.qdrant_url,
        collection_name=config.qdrant_collection_name
    )
    
    print(f"Loaded existing vector store from {config.qdrant_url}")
    return vector_store


def get_or_create_vector_store(chunked_docs=None):
    """Smart vector store loading - checks for existing DB first"""
    config = get_config()
    qdrant_path = Path(config.qdrant_url)
    
    if qdrant_path.exists():
        print("Vector database exists. Loading...")
        return load_existing_vector_store()
    else:
        if chunked_docs is None:
            raise ValueError("chunked_docs required when creating new vector store")
        print("Vector database not found. Creating new one...")
        return create_vector_store(chunked_docs)


def create_database_components():
    """Create database components (vector_store, chunked_docs)"""
    config = get_config()
    model_factory = get_model_factory()
    
    # Load documents
    documents = load_saved_documents()
    print(f"📚 Loaded {len(documents)} documents")
    
    ## Filter to Redis services only for focused responses
    #documents = filter_by_service(documents, ['redis'])
    #print(f"🔍 Filtered to {len(documents)} Redis documents")
    
    # Preprocess HTML documents to markdown
    print("🔄 Preprocessing documents...")
    processed_documents = preprocess_html_documents(documents)
    
    # Chunk documents with tiktoken
    print("🔄 Chunking documents...")
    chunked_docs = chunk_documents_with_tiktoken(processed_documents, chunk_size=1000, chunk_overlap=200)
    print(f"📄 Created {len(chunked_docs)} chunks")
    
    # Create or load vector store
    print("🔄 Creating/loading vector store...")
    vector_store = get_or_create_vector_store(chunked_docs)
    
    return vector_store, chunked_docs
