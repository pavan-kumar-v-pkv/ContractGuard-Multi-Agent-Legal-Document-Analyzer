"""Negotiation advisor agent."""

from typing import Any, Dict, Iterable

from config.prompts import NEGOTIATION_ADVISOR_PROMPT
from src.agents.llm_client import get_llm
from src.utils.json_utils import safe_json_loads


def negotiation_advice(
    clause_text: str,
    risk_level: int | str,
    concerns: Iterable[str],
    llm=None,
) -> Dict[str, Any]:
    """Generate negotiation advice for a clause."""
    llm = llm or get_llm()
    prompt = NEGOTIATION_ADVISOR_PROMPT.format(
        clause_text=clause_text,
        risk_level=risk_level,
        concerns="\n".join(concerns),
    )
    response = llm.invoke(prompt)
    content = response.content if hasattr(response, "content") else str(response)
    return safe_json_loads(content)
