"""Risk assessment agent."""

from typing import Any, Dict

from config.prompts import RISK_ASSESSOR_PROMPT
from src.agents.llm_client import get_llm
from src.utils.json_utils import safe_json_loads


def assess_risk(clause_type: str, clause_text: str, llm=None) -> Dict[str, Any]:
    """Assess risk for a clause using the LLM."""
    llm = llm or get_llm()
    prompt = RISK_ASSESSOR_PROMPT.format(
        clause_type=clause_type,
        clause_text=clause_text,
    )
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)
    return safe_json_loads(content)
