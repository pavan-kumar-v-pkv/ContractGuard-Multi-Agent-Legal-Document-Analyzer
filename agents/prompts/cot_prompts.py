"""
Chain-of-Thought (CoT) prompts for contract analysis
7-step reasoning: Identification -> Legal -> Financial -> Business -> Risk -> Recommendations
"""

COT_SYSTEM_PROMPT = """You are an expert contract analyst with 20+ years of legal and business experience.
You analyze contract clauses systematically using a 7-step Chain-of-Thought reasoning process.

Your analysis must be:
- Thorough and methodical
- Legally accurate
- Practically actionable
- Balanced (not overly cautious or dismissive)
- Focused on protecting the weaker part's interests

Always return structured JSON output following the exact schema provided.
"""

COT_ANALYSIS_PROMPT = """Analyze the following contract clause using 7-step Chain-of-Thought reasoning:

**CLAUSE TO ANALYZE:**
{clause_text}

**CLAUSE TYPE:** {clause_type}

**CONTEXT FROM SIMILAR STANDARD CLAUSES:**
{similar_clauses}

---

**ANALYZE STEP-BY-STEP:**

**Step 1- Clause Identification:**
- What is this clause really saying?
- What are the key obligations, rights, and conditions?
- Identify any ambiguous or vague language.

**Step 2 - Legal Analysis:**
- What are the legal implications?
- Does it comply with standard legal practices?
- Are there any red flags (unlimited liability, one-sided terms, unfair termination)?
- How does it compare to industry-standard clauses?

**Step 3 - Financial Impact:**
- What are the potential financial costs or risks?
- Are there hidden fees, penalties, or liabilities?
- What's the worst-case financial scenario?

**Step 4 - Business Implications:**
- How does this affect day-to-day operations?
- Does it limit business flexibility?
- What happens if circumstances change (e.g., need to terminate early)?

**Step 5 - Risk Scoring:**
- Overall risk level: LOW (1-3), MEDIUM (4-6), HIGH (7-8), CRITICAL (9-10)
- Justify the score based on legal, financial, and business factors.

**Step 6 - Recommendations:**
- Should this clause be accepted, modified, or rejected?
- What specific changes would make it fairer?
- What alternative language would you suggest?

**Step 7 - Negotiation Strategy:**
- What's the best approach to negotiate this clause?
- What leverage points exist?
- What's a realistic compromise?

---

**OUTPUT FORMAT (JSON):**
Return ONLY valid JSON, no markdown:
{{
    "clause_type": "string",
    "clause_summary": "string (1-2 sentences)",
    "step1_identification": {{
        "key_obligations": ["list"],
        "key_rights": ["list"],
        "ambiguous_terms": ["list"]
    }},
    "step2_legal_analysis": {{
        "legal_issues": ["list of concerns"],
        "compliance_status": "compliant/concerning/non-compliant",
        "comparison_to_standard": "better/similar/worse",
        "red_flags": ["list"]
    }},
    "step3_financial_impact": {{
        "potential_costs": ["list"],
        "worst_case_scenario": "string",
        "estimated_risk_amount": "string (e.g., '$10K-50K' or 'unlimited')"
    }},
    "step4_business_implications": {{
        "operational_impact": "string",
        "flexibility_constraints": ["list"],
        "exit_difficulty": "easy/moderate/difficult/trapped"
    }},
    "step5_risk_scoring": {{
        "risk_level": "low/medium/high/critical",
        "risk_score": 1-10,
        "justification": "string (2-3 sentences)"
    }},
    "step6_recommendations": {{
        "action": "accept/modify/reject",
        "priority": "low/medium/high/urgent",
        "suggested_changes": ["list of specific edits"],
        "alternative_language": "string (your proposed clause text)"
    }},
    "step7_negotiation": {{
        "strategy": "string (approach to take)",
        "leverage_points": ["list"],
        "realistic_compromise": "string",
        "dealbreaker": true/false
    }},
    "overall_verdict": "string (final 2-3 sentence summary)"
}}
"""

FEW_SHOT_EXAMPLES = """
**EXAMPLE 1 - UNFAIR TERMINATION CLAUSE:**

Clause: "Company may terminate this agreement at any time without cause or notice. Contractor must provide 90 days written notice and may only terminate for material breach."

Analysis:
{{
    "clause_type": "termination",
    "risk_level": "critical",
    "risk_score": 9,
    "legal_issues": [
        "Grossly one-sided termination rights",
        "No notice requirement for company",
        "Excessive 90-day notice for contractor",
        "Contractor cannot terminate without cause"
    ],
    "action": "reject",
    "suggested_changes": [
        "Add 30-day notice requirement for both parties",
        "Allow both parties to terminate without cause with equal notice",
        "Remove asymmetric termination conditions"
    ]
}}

---

**EXAMPLE 2 - FAIR PAYMENT CLAUSE:**

Clause: "Payment due within 30 days of invoice. Late payments incur 1.5% monthly interest. Either party may dispute charges within 15 days with written explanation."

Analysis:
{{
    "clause_type": "payment",
    "risk_level": "low",
    "risk_score": 2,
    "legal_issues": [],
    "action": "accept",
    "suggested_changes": [],
    "justification": "Standard payment terms, reasonable interest rate, fair dispute process for both parties"
}}

---

**EXAMPLE 3 - CONCERNING LIABILITY CLAUSE:**

Clause: "Contractor shall indemnify and hold Company harmless from any and all claims, damages, or expenses arising from this agreement, including Company's own negligence."

Analysis:
{{
    "clause_type": "liability",
    "risk_level": "high",
    "risk_score": 8,
    "legal_issues": [
        "Unlimited liability exposure",
        "Covers company's own negligence (highly unusual)",
        "No cap on indemnification amount",
        "One-sided (no mutual indemnification)"
    ],
    "action": "modify",
    "suggested_changes": [
        "Add liability cap (e.g., '...up to the amount paid under this agreement')",
        "Remove indemnification for Company's own negligence",
        "Make indemnification mutual",
        "Exclude indirect/consequential damages"
    ],
    "alternative_language": "Each party shall indemnify the other for direct damages caused by their own negligence or breach, up to the total amount paid under this agreement, excluding indirect or consequential damages."
}}
"""