"""
Contract Indexer - Creates vector embeddings and searchable index for contracts.
Uses LlamaIndex to build RAG system.
"""

import os
import json
from typing import List, Dict
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from tqdm import tqdm

class ContractIndexer:
    """
    Creates searchable vector index of contract clauses using LlamaIndex and ChromaDB.
    """

    def __init__(self, 
                 contract_db_path: str="rag/contract_database",
                 vector_db_path: str="rag/embeddings"
                ):
        self.contract_db_path = contract_db_path
        self.vector_db_path = vector_db_path

        # Setup embeddings model

        print("Loading embedding model...")
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

        # Setup text splitter
        Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)

        print("Embedding model loaded.")

    def load_contracts(self) -> List[Dict]:
        """Load all contracts from database directory."""
        contracts = []

        if not os.path.exists(self.contract_db_path):
            raise ValueError(f"Contract database not found:  {self.contract_db_path}")

        for filename in os.listdir(self.contract_db_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.contract_db_path, filename)
                with open(filepath, 'r') as f:
                    contract = json.load(f)
                    contracts.append(contract)

        print(f"Loaded {len(contracts)} contracts from database")
        return contracts
    
    def create_documents(self, contracts: List[Dict]) -> List[Document]:
        """
        Convert contracts to LlamaIndex Document objects.
        Each clause becomes a separate document for better retrieval.
        """
        documents = []

        for contract in tqdm(contracts, desc="Creating documents"):
            contract_type = contract['type']

            # Create a document for each clause
            for clause_name, clause_data in contract['clauses'].items():
                # Combine text with metadata for better context
                text = f"""
Contract Type: {contract_type}
Clause Type: {clause_name}
Standard Text: {clause_data['text']}
Benchmark: {clause_data['benchmark']}
Key Terms: {json.dumps(clause_data['key_terms'], indent=2)}
                """.strip()

                # Create Document with metadata
                doc = Document(
                    text=text,
                    metadata={
                        'contract_type': contract_type,
                        'clause_type': clause_name,
                        'risk_level': contract.get('risk_level', 'unknown'),
                        'fairness_score': clause_data['key_terms'].get('fairness_score', 5),
                        'source': 'standard_contract_database'
                    }
                )
                documents.append(doc)

            print(f"Created {len(documents)} searchable document chunks")
            return documents
        
    def build_index(self, documents: List[Document]) -> VectorStoreIndex:
        """
        Build vector index using ChromaDB as the vector store.
        """
        print("Building vector index...")

        # Setup ChromaDB
        os.makedirs(self.vector_db_path, exist_ok=True)

        db = chromadb.PersistentClient(path=self.vector_db_path)
        chroma_collection = db.get_or_create_collection("contract_clauses")

        vector_store = ChromaVectorStore(chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Create index
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )

        print(f"Vector index built with {len(documents)} documents.")
        print(f"Saved to: {self.vector_db_path}")

        return index
    
    def index_contracts(self):
        """
        Main method: Load contracts, create documents, and build vector index.
        """
        print("="*60)
        print("CONTRACT INDEXING PIPELINE")
        print("="*60)

        # Step 1: Load Contracts
        contracts = self.load_contracts()

        # Step 2: Convert to Documents
        documents = self.create_documents(contracts)

        # Step 3: Build Vector index
        index = self.build_index(documents)

        print("\n"+"="*60)
        print("INDEXING COMPLETE")
        print("="*60+"\n")
        return index
    
# Helper function
def index_all_contracts():
    """Quick function to index everything."""
    indexer = ContractIndexer()
    index = indexer.index_contracts()
    return index

if __name__ == "__main__":
    index_all_contracts()
