"""
Chain-of-Thought Contract Analyzer
Uses 7-step reasoning process to analyze contract clauses.
"""

import json
from typing import Dict, Optional, List
from .llm_client import LLMClient, LLMConfig
from .prompts.cot_prompts import COT_SYSTEM_PROMPT, COT_ANALYSIS_PROMPT, FEW_SHOT_EXAMPLES

class CoTAnalyzer:
    """
    Analyzes contract clauses using Chain-of-Thought reasoning.
    Integrates with RAG system to compare against standard clauses.
    """

    def __init__(self, llm_client: Optional[LLMClient] = None, retriever=None):
        """
        Args:
            llm_client: LLM client for generation (uses default if None)
            retriever: ContractRetriever instance for RAG (optional)
        """
        self.llm = llm_client or LLMClient()
        self.retriever = retriever

    async def analyze_clause(
            self,
            clause_text: str,
            clause_type: str = "unknown",
            use_rag: bool = True
    ) -> Dict:
        """
        Analyze a contract clause using 7-step CoT reasoning.

        Args:
            clause_text: The clause text to analyze
            clause_type: Type of clause (e.g. "termination", "payment", "liability")
            user_rag: Whether to retrieve similar clauses for context

        Returns:
            Structured analysis with risk scores and recommendations
        """
        # 1. Retrieve similar clauses from standard contracts (if RAG enabled)
        similar_clauses_text = ""
        if use_rag and self.retriever:
            try:
                similar = self.retriever.search_similar_clauses(
                    query_clause=clause_text,
                    clause_type=clause_type,
                    top_k=3
                )

                if similar:
                    similar_clauses_text = "\n\n".join([
                        f"**Standard Clause {i+1}** (Fairness: {s.get('fairness_score', 'N/A')}/10):\n{s['text']}"
                        for i, s in enumerate(similar)
                    ])
                else:
                    similar_clauses_text = "No similar standard clauses found in database."
            except Exception as e:
                print(f"Warning: RAG retrieval failed: {e}")
                similar_clauses_text = "RAG retrieval unavailable."
        else:
            similar_clauses_text = "RAG comparison disabled."

        # 2. Build the analysis prompt
        prompt = COT_ANALYSIS_PROMPT.format(
            clause_text=clause_text,
            clause_type=clause_type,
            similar_clauses=similar_clauses_text
        )
        # Add few-shot examples to system prompt
        full_system_prompt = f"{COT_SYSTEM_PROMPT}\n\n**EXAMPLES OF GOOD ANALYSIS:**{FEW_SHOT_EXAMPLES}"

        # Step 3: Generate analysis
        try:
            response = await self.llm.generate_json(
                prompt=prompt,
                system_prompt=full_system_prompt
            )

            # Validate and return
            if isinstance(response, dict):
                response['analyzed_clause'] = clause_text
                response['rag_context_used'] = use_rag and self.retriever is not None
                return response
            else:
                raise ValueError(f"LLM response is not a valid JSON object. Expected dict, got {type(response)}")
            
        except json.JSONDecodeError as e:
            print(f"Error: LLM returned invalid JSON: {e}")
            return self._error_response(clause_text, "JSON parsing failed")
        except Exception as e:
            print(f"Error during clause analysis: {e}")
            return self._error_response(clause_text, str(e))
        
    def analyze_clause_sync(
        self,
        clause_text: str,
        clause_type: str = "unknown",
        use_rag: bool = True
    ) -> Dict:
        """
        Synchronous version of analyze_clause.
        Useful for non-async code.
        """
        import asyncio
        return asyncio.run(self.analyze_clause(
            clause_text=clause_text,
            clause_type=clause_type,
            use_rag=use_rag
        ))
    
    async def analyze_multiple_clauses(
        self,
        clauses: List[Dict[str, str]],
        use_rag: bool = True
    ) -> List[Dict]:
        """
        Analyze multiple clauses in parallel.
        
        Args:
            clauses: List of {"text": ..., "type": ...} dicts
            use_rag: Whether to use RAG for each clause
        
        Returns:
            List of analysis results
        """
        import asyncio
        tasks = [
            self.analyze_clause(
                clause_text=clause["text"],
                clause_type=clause.get("type", "unknown"),
                use_rag=use_rag
            )
            for clause in clauses
        ]
        return await asyncio.gather(*tasks)
    
    def _error_response(self, clause_text: str, error_msg: str) -> Dict:
        """Return a safe error response."""
        return {
            "clause_type": "error",
            "analyzed_clause": clause_text,
            "error": error_msg,
            "step5_risk_scoring": {
                "risk_level": "unknown",
                "risk_score": 0,
                "justification": "Analysis failed"
            },
            "step6_recommendations": {
                "action": "manual_review",
                "priority": "high",
                "suggested_changes": ["Review this clause manually - automated analysis failed"],
                "alternative_language": ""
            },
            "overall_verdict": f"Automated analysis failed: {error_msg}. Manual review required."
        }
    
    def print_analysis(self, analysis: Dict) -> None:
        """Pretty-print the analysis result."""
        print("\n" + "="*80)
        print(f"CLAUSE ANALYSIS: {analysis.get('clause_type', 'unknown').upper()}")
        print("="*80)
        
        print("\nCLAUSE TEXT:")
        print(f"  {analysis.get('analyzed_clause', 'N/A')[:200]}...")
        
        if 'step5_risk_scoring' in analysis:
            risk = analysis['step5_risk_scoring']
            print("\n RISK ASSESSMENT:")
            print(f"  Level: {risk.get('risk_level', 'unknown').upper()}")
            print(f"  Score: {risk.get('risk_score', 0)}/10")
            print(f"  Why: {risk.get('justification', 'N/A')}")
        
        if 'step6_recommendations' in analysis:
            rec = analysis['step6_recommendations']
            print("\n RECOMMENDATION:")
            print(f"  Action: {rec.get('action', 'unknown').upper()}")
            print(f"  Priority: {rec.get('priority', 'unknown').upper()}")
            if rec.get('suggested_changes'):
                print("  Changes needed:")
                for change in rec['suggested_changes'][:3]:
                    print(f"    - {change}")
        
        print("\n VERDICT:")
        print(f"  {analysis.get('overall_verdict', 'N/A')}")
        print("="*80 + "\n")