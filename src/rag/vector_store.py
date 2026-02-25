"""Vector store utilities using Chroma."""

from pathlib import Path
from typing import Iterable, List

from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from config.settings import settings
from src.rag.embeddings import get_embeddings


class VectorStoreManager:
    """Manage Chroma vector store operations."""

    def __init__(self, persist_directory: str | None = None):
        self.persist_directory = Path(persist_directory or settings.VECTOR_STORE_PATH)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self._store: Chroma | None = None

    def _get_store(self) -> Chroma:
        if self._store is None:
            self._store = Chroma(
                collection_name="contractguard",
                persist_directory=str(self.persist_directory),
                embedding_function=get_embeddings(),
            )
        return self._store

    def add_texts(self, texts: Iterable[str], metadatas: Iterable[dict] | None = None) -> List[str]:
        """Add texts to the vector store.
        
        Args:
            texts: Texts to add
            metadatas: Optional metadata for each text
            
        Returns:
            List of document IDs
        """
        texts_list = list(texts)
        if not texts_list:
            return []
            
        store = self._get_store()
        ids = store.add_texts(texts_list, metadatas=list(metadatas) if metadatas else None)
        store.persist()
        return ids

    def similarity_search(self, query: str, k: int | None = None) -> List[Document]:
        store = self._get_store()
        return store.similarity_search(query, k=k or settings.TOP_K_RETRIEVAL)

    def as_retriever(self, k: int | None = None):
        store = self._get_store()
        return store.as_retriever(search_kwargs={"k": k or settings.TOP_K_RETRIEVAL})
