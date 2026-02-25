"""JSON parsing helpers for LLM responses."""

import json
import re
from typing import Any


def _extract_json_block(text: str) -> str | None:
    """Extract the first JSON object or array from text."""
    if not text:
        return None

    # Try to find JSON code blocks first (markdown style)
    code_block_match = re.search(r"```(?:json)?\s*([\{\[].*?[\}\]])\s*```", text, re.DOTALL)
    if code_block_match:
        return code_block_match.group(1)

    # Fall back to finding any JSON-like structure
    match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if match:
        return match.group(1)
    return None


def safe_json_loads(text: str) -> Any:
    """Parse JSON from a string, falling back to extracting a JSON block.
    
    Args:
        text: Input string that may contain JSON
        
    Returns:
        Parsed JSON object (dict, list, etc.)
        
    Raises:
        json.JSONDecodeError: If no valid JSON can be extracted
    """
    if not text or not text.strip():
        raise ValueError("Empty input text")
        
    # Try direct parsing first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try extracting JSON from text
        extracted = _extract_json_block(text)
        if not extracted:
            raise ValueError(f"No valid JSON found in text: {text[:200]}...")
        try:
            return json.loads(extracted)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse extracted JSON: {e}")
