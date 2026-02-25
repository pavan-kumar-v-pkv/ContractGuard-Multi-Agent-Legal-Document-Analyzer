"""Embedding model factory."""

from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings, HuggingFaceEmbeddings

from config.settings import settings


def get_embeddings():
    """Return an embeddings model based on settings."""
    if settings.LLM_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")
        return OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, api_key=settings.OPENAI_API_KEY)

    if settings.LLM_PROVIDER == "ollama":
        return OllamaEmbeddings(base_url=settings.OLLAMA_BASE_URL, model=settings.OLLAMA_MODEL)

    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
