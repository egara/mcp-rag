import logging
from typing import Dict, Any, List

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

from src.config import settings

logger = logging.getLogger(__name__)

def get_embedding_function():
    """Returns the embedding function based on configuration."""
    model_name = settings.embedding_model
    if "sentence-transformers" in model_name:
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return OllamaEmbeddings(
        model=model_name,
        # Note: If you use Ollama for embeddings, you'll need to add OLLAMA_BASE_URL to config
        # base_url="http://host.docker.internal:11434",
    )

def get_vector_store() -> PGVector:
    """Returns the pgvector store instance."""
    embeddings = get_embedding_function()
    return PGVector(
        embeddings=embeddings,
        connection=settings.postgres_connection_string,
        collection_name=settings.pgvector_collection,
        use_jsonb=True,
    )

def query_documents(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Searches the RAG system and returns the most relevant document chunks.
    Does NOT use an LLM to synthesize an answer.
    """
    try:
        vector_store = get_vector_store()
        docs = vector_store.similarity_search(query, k=top_k)
        
        sources = []
        for doc in docs:
            sources.append({
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", "?"),
                "content": doc.page_content.strip()
            })

        return sources
    except Exception as e:
        logger.error(f"Error querying RAG: {e}")
        return []
