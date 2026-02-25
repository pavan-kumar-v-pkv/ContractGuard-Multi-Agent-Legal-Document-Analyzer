"""Clause extraction agent."""

from typing import Any, List

from config.prompts import CLAUSE_EXTRACTOR_PROMPT
from src.agents.llm_client import get_llm
from src.utils.json_utils import safe_json_loads


def extract_clauses(contract_text: str, llm=None) -> List[dict[str, Any]]:
    """Extract clauses from a contract using the LLM.
    
    Args:
        contract_text: Full text of the contract
        llm: Optional pre-configured LLM instance
        
    Returns:
        List of clause dictionaries with type, title, text, section
        
    Raises:
        ValueError: If contract text is empty or invalid
    """
    if not contract_text or not contract_text.strip():
        raise ValueError("Contract text cannot be empty")
        
    llm = llm or get_llm()
    prompt = CLAUSE_EXTRACTOR_PROMPT.format(contract_text=contract_text)
    
    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        clauses = safe_json_loads(content)
        
        # Ensure we return a list
        if not isinstance(clauses, list):
            raise ValueError("Expected list of clauses from LLM")
        return clauses
    except Exception as e:
        raise RuntimeError(f"Failed to extract clauses: {e}") from e
