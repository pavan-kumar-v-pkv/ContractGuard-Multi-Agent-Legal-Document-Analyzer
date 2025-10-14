"""
Contract Retriever - Searches vector database for similar clauses
"""

import os
from typing import List, Dict
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

class ContractRetriever:
    """
    Retrieves similar clauses from contract database
    """

    def __init__(self, vector_db_path: str="rag/embeddings"):
        self.vector_db_path = vector_db_path


        # Setup embeddings model
        print("Loading embedding model...")
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        print("Embedding model loaded.")

        # Load existing index
        self.index = self._load_index()
        print("Contract retriever initialized and ready.")

    def _load_index(self) -> VectorStoreIndex:
        """Load the pre-built vector index from ChromaDB."""
        if not os.path.exists(self.vector_db_path):
            raise ValueError(f"Vector database not found at {self.vector_db_path}. Run indexer first!")
        
        # Connect to ChromaDB
        db = chromadb.PersistentClient(path=self.vector_db_path)
        chroma_collection = db.get_or_create_collection("contract_clauses")
        
        vector_store = ChromaVectorStore(chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store)

        return index
    
    def search_similar_clauses(self, query_clause: str, clause_type: str = None, top_k: int = 3) -> List[Dict]:
        """
        Search for similar clauses in standard contracts
        Args:
            query_clause: The clause text to compare
            clause_type: Optional filter (e.g., "NDA", "Service Agreement")
            top_k: Number of similar clauses to return
        Returns:
            List of similar clause with metadata
        """
        # Build query with context
        query = f"Clause Type: {clause_type}\n{query_clause}" if clause_type else query_clause

        # Create query engine
        query_engine = self.index.as_query_engine(
            similarity_top_k=top_k,
            response_mode="no_text" # we just want the source nodes
        )

        # execute search
        response = query_engine.query(query)

        # Format results
        results = []
        for node in response.source_nodes:
            results.append({
                'text': node.node.text,
                'score': node.score,
                'metadata': node.node.metadata,
                'contract_type': node.node.metadata.get('contract_type'),
                'clause_type': node.node.metadata.get('clause_type'),
                'fairness_score': node.node.metadata.get('fairness_score')
            })

        return results
    
    def compare_clause(self, user_clause: str, clause_type: str) -> Dict:
        """
        Compare user's clause against standard clauses
        Returns comparison analysis
        """
        # Search for similar standard clauses
        similar = self.search_similar_clauses(user_clause, clause_type, top_k=5)

        if not similar:
            return {
                'found_similar': False,
                'message': 'No similar clauses found in the database.'
            }
        
        # Calculate statistics
        fairness_scores = [s['fairness_score'] for s in similar if s['fairness_score'] is not None]
        avg_fairness = sum(fairness_scores) / len(fairness_scores) if fairness_scores else 5.0

        return {
            'found_similar': True,
            'similar_clauses': similar,
            'average_fairness_score': avg_fairness,
            'best_match': similar[0] if similar else None,  # highest score
            'comparison_summary': self._generate_comparison_summary(similar)
        }

    def _generate_comparison_summary(self, similar_clauses: List[Dict]) -> str:
        """
        Generate a human-readable summary of the comparison between the user's clause and similar clauses.
        """
        if not similar_clauses:
            return "No similar clauses found for comparison."

        best_match = similar_clauses[0]
        summary = f"""
Found {len(similar_clauses)} similar clauses in the standard contracts.

Best Match:
-   Contract Type: {best_match['contract_type']}
-   Clause Type: {best_match['clause_type']}
-   Fairness Score: {best_match['fairness_score']}/10
-   Similarity Score: {best_match['score']:.4f}

This clause appears in standard {best_match['contract_type']} agreements.
        """.strip()

        return summary
    
# helper function
def search_contracts(query: str, clause_type: str = None, top_k: int = 3):
    """Quick search function"""
    retriever = ContractRetriever()
    
    # Test query
    test_clause = "Either party may terminate with 30 days notice."
    results = retriever.search_similar_clauses(test_clause, "termination")

    print("\n Search results:")
    print("="*60)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['contract_type']} - {result['clause_type']}")
        print(f"   Fairness Score: {result['fairness_score']}/10")
        print(f"   Similarity Score: {result['score']:.4f}")
        print(f"   Text: {result['text'][:200]}...")  # truncate for display
