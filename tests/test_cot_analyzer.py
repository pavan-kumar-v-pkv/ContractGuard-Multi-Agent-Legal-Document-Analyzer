# File: tests/test_cot_analyzer.py
"""
Tests for Chain-of-Thought Contract Analyzer
"""

import pytest
from agents.cot_analyzer import CoTAnalyzer
from agents.llm_client import LLMClient

# Sample clauses for testing
UNFAIR_TERMINATION = """
Company may terminate this agreement at any time, for any reason or no reason, 
without notice. Contractor must provide 90 days written notice and may only 
terminate for material breach that remains uncured for 30 days.
"""

FAIR_PAYMENT = """
Payment is due within 30 days of invoice receipt. Late payments will incur 
interest at 1.5% per month. Either party may dispute charges within 15 days 
by providing written explanation.
"""

CONCERNING_LIABILITY = """
Contractor shall indemnify, defend, and hold harmless Company from any and all 
claims, damages, losses, and expenses, including attorney fees, arising from 
this agreement or Contractor's work, including claims arising from Company's 
own negligence or willful misconduct.
"""

VAGUE_CONFIDENTIALITY = """
Contractor agrees to keep all information confidential forever and will not 
disclose anything learned during the engagement to anyone for any purpose.
"""

@pytest.mark.asyncio
async def test_analyze_termination_clause():
    """Test analysis of unfair termination clause."""
    analyzer = CoTAnalyzer()
    
    result = await analyzer.analyze_clause(
        clause_text=UNFAIR_TERMINATION,
        clause_type="termination",
        use_rag=False  # Disable RAG for unit test
    )
    
    # Validate structure
    assert 'clause_type' in result
    assert 'step5_risk_scoring' in result
    assert 'step6_recommendations' in result
    
    # Should detect high risk
    risk_score = result['step5_risk_scoring']['risk_score']
    assert risk_score >= 7, f"Expected high risk (7+), got {risk_score}"
    
    # Should recommend changes
    action = result['step6_recommendations']['action']
    assert action in ['modify', 'reject'], f"Expected modify/reject, got {action}"
    
    print("\nTermination clause analysis:")
    analyzer.print_analysis(result)

@pytest.mark.asyncio
async def test_analyze_payment_clause():
    """Test analysis of fair payment clause."""
    analyzer = CoTAnalyzer()
    
    result = await analyzer.analyze_clause(
        clause_text=FAIR_PAYMENT,
        clause_type="payment",
        use_rag=False
    )
    
    # Should be low-medium risk (3b model can be conservative)
    risk_score = result['step5_risk_scoring']['risk_score']
    assert risk_score <= 7, f"Expected low-medium risk (≤7), got {risk_score}"
    
    # Should recommend accept or minor modify
    action = result['step6_recommendations']['action']
    assert action in ['accept', 'modify'], f"Expected accept/modify, got {action}"
    
    print("\nPayment clause analysis:")
    analyzer.print_analysis(result)

@pytest.mark.asyncio
async def test_analyze_liability_clause():
    """Test analysis of concerning liability clause."""
    analyzer = CoTAnalyzer()
    
    result = await analyzer.analyze_clause(
        clause_text=CONCERNING_LIABILITY,
        clause_type="liability",
        use_rag=False
    )
    
    # Validate legal issues detected
    if 'step2_legal_analysis' in result:
        legal_issues = result['step2_legal_analysis'].get('legal_issues', [])
        red_flags = result['step2_legal_analysis'].get('red_flags', [])
        assert len(legal_issues) > 0 or len(red_flags) > 0, "Should detect legal issues"
    
    # Should be high risk
    risk_score = result['step5_risk_scoring']['risk_score']
    assert risk_score >= 6, f"Expected high risk (6+), got {risk_score}"
    
    print("\nLiability clause analysis:")
    analyzer.print_analysis(result)

@pytest.mark.asyncio
async def test_batch_analysis():
    """Test analyzing multiple clauses in parallel."""
    analyzer = CoTAnalyzer()
    
    clauses = [
        {"text": UNFAIR_TERMINATION, "type": "termination"},
        {"text": FAIR_PAYMENT, "type": "payment"},
        {"text": VAGUE_CONFIDENTIALITY, "type": "confidentiality"}
    ]
    
    results = await analyzer.analyze_multiple_clauses(clauses, use_rag=False)
    
    assert len(results) == 3, f"Expected 3 results, got {len(results)}"
    
    for i, result in enumerate(results):
        print(f"\n{'='*80}")
        print(f"BATCH ANALYSIS {i+1}/3")
        analyzer.print_analysis(result)

def test_sync_analyzer():
    """Test synchronous wrapper."""
    analyzer = CoTAnalyzer()
    
    result = analyzer.analyze_clause_sync(
        clause_text=FAIR_PAYMENT,
        clause_type="payment",
        use_rag=False
    )
    
    assert 'clause_type' in result
    assert 'step5_risk_scoring' in result
    
    print("\nSync analysis works!")

if __name__ == "__main__":
    # Run tests manually
    import asyncio
    
    analyzer = CoTAnalyzer()
    
    print("\nTesting Chain-of-Thought Analyzer...\n")
    
    # Test termination clause
    result = asyncio.run(analyzer.analyze_clause(
        UNFAIR_TERMINATION,
        "termination",
        use_rag=False
    ))
    analyzer.print_analysis(result)