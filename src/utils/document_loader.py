"""
Document loading and analysis utilities for SREnity
"""
import json
from pathlib import Path
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_community.document_loaders import RecursiveUrlLoader
from markdownify import markdownify as md


def load_saved_documents(filename: str = "gitlab_runbooks.json") -> List[Document]:
    """Load documents from saved JSON file"""
    filepath = Path("../data/runbooks") / filename
    
    if not filepath.exists():
        raise FileNotFoundError(f"Document file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        docs_data = json.load(f)
    
    # Convert back to Document objects
    documents = []
    for doc_data in docs_data:
        doc = Document(
            page_content=doc_data['page_content'],
            metadata=doc_data['metadata']
        )
        documents.append(doc)
    
    return documents


def analyze_document_sizes(documents: List[Document]) -> Tuple[List[Tuple[int, str, str]], dict]:
    """Analyze document sizes and return statistics"""
    
    # Create list of (size, source, title) tuples
    sizes = [(len(doc.page_content), doc.metadata.get('source', 'Unknown'), doc.metadata.get('title', 'No title')) 
             for doc in documents]
    sizes.sort(reverse=True)
    
    # Calculate statistics
    sizes_only = [size for size, _, _ in sizes]
    stats = {
        'total_documents': len(documents),
        'largest': max(sizes_only),
        'smallest': min(sizes_only),
        'average': sum(sizes_only) / len(sizes_only),
        'over_100k': sum(1 for s in sizes_only if s > 100000),
        'over_200k': sum(1 for s in sizes_only if s > 200000),
        'over_300k': sum(1 for s in sizes_only if s > 300000)
    }
    
    return sizes, stats


def print_document_analysis(documents: List[Document], top_n: int = 10):
    """Print document size analysis"""
    sizes, stats = analyze_document_sizes(documents)
    
    print(f"Loaded {stats['total_documents']} documents")
    print("\n=== Document Size Analysis ===")
    
    print(f"Largest documents:")
    for i, (size, source, title) in enumerate(sizes[:top_n]):
        print(f"{i+1:2d}. {size:6d} chars - {source}")
        print(f"    Title: {title}")
    
    print(f"\nSize statistics:")
    print(f"  Largest: {stats['largest']:,} characters")
    print(f"  Smallest: {stats['smallest']:,} characters") 
    print(f"  Average: {stats['average']:,.0f} characters")
    print(f"  Documents > 100K chars: {stats['over_100k']}")
    print(f"  Documents > 200K chars: {stats['over_200k']}")
    print(f"  Documents > 300K chars: {stats['over_300k']}")
    
    # Show sample of largest document
    print(f"\nSample from largest document:")
    largest_doc = next(doc for doc in documents if len(doc.page_content) == stats['largest'])
    print(f"Source: {largest_doc.metadata.get('source', 'Unknown')}")
    print(f"Title: {largest_doc.metadata.get('title', 'No title')}")
    print(f"Content preview: {largest_doc.page_content[:300]}...")


def get_largest_documents(documents: List[Document], min_size: int = 300000) -> List[Document]:
    """Get documents larger than specified size"""
    return [doc for doc in documents if len(doc.page_content) > min_size]


def get_documents_by_service(documents: List[Document], service_name: str) -> List[Document]:
    """Get documents related to a specific service"""
    service_docs = []
    for doc in documents:
        source = doc.metadata.get('source', '').lower()
        title = doc.metadata.get('title', '').lower()
        if service_name.lower() in source or service_name.lower() in title:
            service_docs.append(doc)
    return service_docs


def download_gitlab_runbooks() -> List[Document]:
    """Download GitLab runbooks using RecursiveUrlLoader"""
    loader = RecursiveUrlLoader(
        url="https://runbooks.gitlab.com/",
        max_depth=2,
        timeout=30
    )
    
    documents = loader.load()
    return documents


def save_documents(documents: List[Document], filename: str = "gitlab_runbooks.json") -> Path:
    """Save documents to file"""
    data_dir = Path("../data/runbooks")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    docs_data = []
    for doc in documents:
        docs_data.append({
            'page_content': doc.page_content,
            'metadata': doc.metadata
        })
    
    filepath = data_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(docs_data, f, indent=2, ensure_ascii=False)
    
    return filepath


def preprocess_html_documents(documents: List[Document]) -> List[Document]:
    """Convert HTML documents to markdown using markdownify"""
    processed_docs = []
    
    for doc in documents:
        # Convert HTML to markdown
        markdown_content = md(
            doc.page_content,
            heading_style="ATX",  # Use # for headings
            bullets="-",          # Use - for lists
            convert=['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                    'ul', 'ol', 'li', 'strong', 'em', 'code', 'pre', 'a', 'br']
        )
        
        # Clean up extra whitespace
        markdown_content = '\n'.join(line.strip() for line in markdown_content.split('\n') if line.strip())
        
        # Create new document with markdown content
        processed_doc = Document(
            page_content=markdown_content,
            metadata=doc.metadata
        )
        processed_docs.append(processed_doc)
    
    # Show before/after comparison
    original_sizes = [len(doc.page_content) for doc in documents]
    processed_sizes = [len(doc.page_content) for doc in processed_docs]
    
    print(f"HTML to Markdown conversion results:")
    print(f"  Original: {min(original_sizes):,} - {max(original_sizes):,} chars")
    print(f"  Markdown: {min(processed_sizes):,} - {max(processed_sizes):,} chars")
    print(f"  Reduction: {((sum(original_sizes) - sum(processed_sizes)) / sum(original_sizes) * 100):.1f}%")
    
    return processed_docs
