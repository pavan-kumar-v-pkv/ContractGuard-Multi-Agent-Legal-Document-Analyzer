"""Text chunking utilities."""

from typing import List

from config.settings import settings
from src.utils.helpers import chunk_text


def chunk_document(text: str, chunk_size: int | None = None, overlap: int | None = None) -> List[str]:
	"""Chunk a document into overlapping segments.

	Args:
		text: Raw document text.
		chunk_size: Number of words per chunk.
		overlap: Number of overlapping words between chunks.

	Returns:
		List of text chunks.
	"""
	if not text:
		return []

	chunk_size = chunk_size or settings.CHUNK_SIZE
	overlap = overlap if overlap is not None else settings.CHUNK_OVERLAP

	return chunk_text(text, chunk_size=chunk_size, overlap=overlap)
