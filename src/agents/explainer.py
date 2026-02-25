"""Plain-language clause explanation agent."""

from typing import Any, Dict

from config.prompts import EXPLAINER_PROMPT
from src.agents.llm_client import get_llm
from src.utils.json_utils import safe_json_loads


def explain_clause(clause_text: str, llm=None) -> Dict[str, Any]:
    """Explain a clause in plain English using the LLM."""
    llm = llm or get_llm()
    prompt = EXPLAINER_PROMPT.format(clause_text=clause_text)
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)
    return safe_json_loads(content)
