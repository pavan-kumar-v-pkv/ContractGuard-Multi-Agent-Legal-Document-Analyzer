"""LLM client factory."""

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama

from config.settings import settings


def get_llm():
    """Return a configured chat model based on settings.
    
    Returns:
        Configured LangChain chat model
        
    Raises:
        ValueError: If LLM provider is unsupported or API key is missing
    """
    if settings.LLM_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not set. Please set it in your .env file or environment."
            )
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.TEMPERATURE,
            api_key=settings.OPENAI_API_KEY,
        )

    if settings.LLM_PROVIDER == "ollama":
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=settings.TEMPERATURE,
        )

    raise ValueError(
        f"Unsupported LLM provider: {settings.LLM_PROVIDER}. Use 'openai' or 'ollama'."
    )
