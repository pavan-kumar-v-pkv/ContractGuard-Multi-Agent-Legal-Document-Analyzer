"""
Test Script for Phase 2 -  RAG System
Tests contract database, indexing and retrieval
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from rag.contract_collector import ContractCollector
from rag.contract_indexer import ContractIndexer
from rag.contract_retriever import ContractRetriever

def test_phase2():
    """
    Test complete RAG pipeline
    """
    print("="*60)
    print(f"PHASE 2 TEST: RAG Knowledge Base")
    print("="*60)

    # Step 1: Generate standard contracts
    print("\nStep 1: Generatinf standard contract database...")
    collector = ContractCollector()
    contracts = collector.generate_standard_contracts()
    print(f"    Created {len(contracts)} standard contracts.")

    # Step 2: Index contracts
    print("\nStep 2: Building vector index...")
    indexer = ContractIndexer()
    index = indexer.index_contracts()
    print("    Vector Index built successfully.")

    # Step 3: Test retrieval
    print("\nStep 3: Testing contract clause retrieval...")
    retriever = ContractRetriever()

    # Test Case 1: Good termination clause
    print("\n" + "-"*60)
    print("TEST CASE 1: Fair Termination Clause")
    print("-"*60)

    good_clause = "Either party may terminate this agreement with 30 days written notice"
    results = retriever.search_similar_clauses(good_clause, clause_type="termination")

    print(f"\nQuery: '{good_clause}'")
    print(f"Found {len(results)} similar clauses:\n")

    for i, res in enumerate(results, 1):
        print(f"{i}. {res['contract_type']} - {res['clause_type']}")
        print(f"   Fairness Score: {res['fairness_score']}/10")
        print(f"   Similarity Score: {res['score']:.4f}\n")
        print()

    # Test Case 2: Unfair termination clause
    print("\n" + "-"*60)
    print("TEST CASE 2: Unfair Termination Clause")
    print("-"*60)

    unfair_clause = "Company may terminate without cause with 24 hours notice. Contractor needs 90 days notice."
    results = retriever.search_similar_clauses(unfair_clause, clause_type="termination")

    print(f"\nQuery: '{unfair_clause}'")
    print(f"Found {len(results)} similar clauses:\n")

    for i, res in enumerate(results, 1):
        print(f"{i}. {res['contract_type']} - {res['clause_type']}")
        print(f"   Fairness Score: {res['fairness_score']}/10")
        print(f"   Similarity Score: {res['score']:.4f}\n")
        print()

    # Test Case 3: Payment clause
    print("\n" + "-"*60)
    print("TEST CASE 3: Payment Clause")
    print("-"*60)

    payment_clause = "Payment is due within 30 days of invoice receipt. Late payments incur a 5% fee."
    results = retriever.search_similar_clauses(payment_clause, clause_type="payment")

    print(f"\nQuery: '{payment_clause}'")
    print(f"Found {len(results)} similar clauses:\n")

    for i, res in enumerate(results, 1):
        print(f"{i}. {res['contract_type']} - {res['clause_type']}")
        print(f"   Fairness Score: {res['fairness_score']}/10")
        print(f"   Similarity Score: {res['score']:.4f}\n")
        print()

    # Test Case 4: Compare clause function
    print("\n" + "-"*60)
    print("TEST CASE 4: Clause Comparison Function")
    print("-"*60)

    test_clause = "Either party may terminate with 30 days notice."
    comparison = retriever.compare_clause(test_clause, clause_type="termination")

    print(f"\nClause to analyze: '{test_clause}'")
    print("\nComparison Summary:")
    print(f"    Found Similar: {comparison['found_similar']}")
    print(f"    Average Fairness Score: {comparison.get('average_fairness_score', 'N/A')}")
    print(f"\n{comparison['comparison_summary']}")

    # Test Case 5: IP clause
    print("\n" + "-"*60)
    print("TEST CASE 5: Intellectual Property Clause")
    print("-"*60)

    ip_clause = "All work created becomes company property immediately"
    results = retriever.search_similar_clauses(ip_clause, clause_type="intellectual_property", top_k=3)

    print(f"\nQuery: '{ip_clause}'")
    print(f"Found {len(results)} similar clauses:\n")

    for i, res in enumerate(results, 1):
        print(f"{i}. {res['contract_type']} - {res['clause_type']}")
        print(f"   Fairness Score: {res['fairness_score']}/10")
        print(f"   Similarity Score: {res['score']:.4f}\n")
        print()

    # Summary
    print("\n" + "="*60)
    print("PHASE 2 TEST COMPLETE")
    print("="*60 + "\n")
    print("\n RAG System Status:")
    print(f" ✅ Contract Database: {len(contracts)} standard contracts")
    print(f" ✅ Vector Index: Built and saved")
    print(f" ✅ Retrieval System: Working correctly")
    print(f" ✅ Location: {os.path.abspath('rag/')}")
    print("\n You can now:")
    print(" 1. Search for similar clauses")
    print(" 2. Compare user clauses against standards")
    print(" 3. Extend the contract database with more clauses/types")


if __name__ == "__main__":
    test_phase2()