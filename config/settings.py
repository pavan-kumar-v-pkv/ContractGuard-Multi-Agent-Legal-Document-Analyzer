"""Application configguration management."""

from pydantic_settings import BaseSettings
from typing import Literal, Optional
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App Info
    APP_NAME: str = "ContractGuard"
    VERSION: str = "0.1.0"
    DEBUG: bool = True

    # LLM Configuration
    LLM_PROVIDER: Literal["openai", "ollama"] = "openai"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    TEMPERATURE: float = 0.1

    # Ollama Configuration(for future use)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3:8b"

    # RAG COnfiguration
    VECTOR_STORE_PATH: str = "./data/vector_store"
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 100
    TOP_K_RETRIEVAL: int = 5

    # Document Processing
    MAX_FILE_SIZE_MB: int = 10
    SUPPORTED_FILE_TYPES: list[str] = ["pdf", "docx"]
    TIMEOUT_SECONDS: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

    @property
    def project_root(self) -> Path:
        """Get project root directory."""
        return Path(__file__).parent.parent

    @property
    def data_dir(self) -> Path:
        """Get data directory path."""
        return self.project_root / "data"

# Global settings instance
settings = Settings()
