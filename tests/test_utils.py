"""Basic unit tests for ContractGuard."""

import pytest
from pathlib import Path

from src.utils.helpers import clean_text, chunk_text, generate_id, validate_file
from src.utils.json_utils import safe_json_loads, _extract_json_block


class TestHelpers:
    def test_clean_text(self):
        text = "Hello    world\n\n\n\nNew paragraph"
        cleaned = clean_text(text)
        assert "  " not in cleaned
        assert "\n\n\n" not in cleaned
        
    def test_chunk_text(self):
        text = " ".join([f"word{i}" for i in range(100)])
        chunks = chunk_text(text, chunk_size=20, overlap=5)
        assert len(chunks) > 1
        assert all(len(chunk.split()) <= 20 for chunk in chunks)
        
    def test_generate_id(self):
        text = "test"
        id1 = generate_id(text)
        id2 = generate_id(text)
        assert id1 == id2  # Same text should give same ID
        assert generate_id("other") != id1


class TestJsonUtils:
    def test_safe_json_loads_valid(self):
        result = safe_json_loads('{"key": "value"}')
        assert result == {"key": "value"}
        
    def test_safe_json_loads_with_code_block(self):
        text = '```json\n{"key": "value"}\n```'
        result = safe_json_loads(text)
        assert result == {"key": "value"}
        
    def test_safe_json_loads_embedded(self):
        text = 'Here is some JSON: {"key": "value"} and more text'
        result = safe_json_loads(text)
        assert result == {"key": "value"}
        
    def test_safe_json_loads_invalid(self):
        with pytest.raises(ValueError):
            safe_json_loads("not json at all")
            
    def test_safe_json_loads_empty(self):
        with pytest.raises(ValueError):
            safe_json_loads("")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
