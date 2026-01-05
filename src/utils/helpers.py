"""Utility helper functions."""

import re
from pathlib import Path
from typing import List
import hashlib

def clean_text(text: str) -> str:
    """CLean and normalize text."""
    # Remove multiple space
    text = re.sub(r'\s+', ' ', text)
    # Remove multiple new lines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    # Strip
    text = text.strip()
    return text

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks

def generate_id(text: str) -> str:
    """Generate unique ID for text."""
    return hashlib.md5(text.encode()).hexdigest()

def validate_file(file_path: Path) -> bool:
    """Validate uploaded file."""
    from config.settings import settings
    
    # Check extension
    if file_path.suffix.lower() not in settings.SUPPORTED_FILE_TYPES:
        return False

    # Check size
    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_path.stat().st_size > max_size:
        return False

    return True