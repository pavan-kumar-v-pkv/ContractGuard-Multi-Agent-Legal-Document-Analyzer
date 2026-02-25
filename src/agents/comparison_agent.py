"""Clause comparison agent."""

from typing import Any, Dict, Iterable

from config.prompts import COMPARISON_PROMPT
from src.agents.llm_client import get_llm
from src.utils.json_utils import safe_json_loads


def compare_clause(clause_text: str, retrieved_clauses: Iterable[str], llm=None) -> Dict[str, Any]:
    """Compare a clause against retrieved standard clauses."""
    llm = llm or get_llm()
    retrieved_text = "\n\n".join(retrieved_clauses)
    prompt = COMPARISON_PROMPT.format(
        clause_text=clause_text,
        retrieved_clauses=retrieved_text,
    )
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)
    return safe_json_loads(content)
