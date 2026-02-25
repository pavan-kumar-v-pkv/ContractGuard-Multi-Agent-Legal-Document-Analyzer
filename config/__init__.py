"""Configuration package exports."""

from config.prompts import (
    CLAUSE_EXTRACTOR_PROMPT,
    COMPARISON_PROMPT,
    EXPLAINER_PROMPT,
    NEGOTIATION_ADVISOR_PROMPT,
    RISK_ASSESSOR_PROMPT,
)
from config.settings import settings

__all__ = [
    "settings",
    "CLAUSE_EXTRACTOR_PROMPT",
    "RISK_ASSESSOR_PROMPT",
    "COMPARISON_PROMPT",
    "NEGOTIATION_ADVISOR_PROMPT",
    "EXPLAINER_PROMPT",
]
