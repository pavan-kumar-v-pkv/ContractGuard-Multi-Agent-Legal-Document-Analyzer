"""Orchestration pipeline for ContractGuard."""

from pathlib import Path
from typing import Any, Dict, List

from config.settings import settings
from src.agents.clause_extractor import extract_clauses
from src.agents.comparison_agent import compare_clause
from src.agents.explainer import explain_clause
from src.agents.llm_client import get_llm
from src.agents.negotiation_advisor import negotiation_advice
from src.agents.risk_assessor import assess_risk
from src.parsers.chunker import chunk_document
from src.parsers.docx_parser import DOCXParser
from src.parsers.pdf_parser import PDFParser
from src.rag.vector_store import VectorStoreManager
from src.utils.helpers import clean_text, validate_file


class ContractGuardPipeline:
    """End-to-end contract processing pipeline."""

    def __init__(self):
        self.llm = get_llm()
        self.vector_store = VectorStoreManager()
        self.pdf_parser = PDFParser()
        self.docx_parser = DOCXParser()

    def parse_document(self, file_path: Path) -> Dict[str, Any]:
        """Parse a document and return structured content.
        
        Args:
            file_path: Path to document file
            
        Returns:
            Dictionary with parsed content including text, sections, metadata
            
        Raises:
            ValueError: If file type is unsupported or file is invalid
            FileNotFoundError: If file doesn't exist
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not validate_file(file_path):
            raise ValueError(
                f"Invalid file: {file_path.name}. Must be PDF or DOCX under {settings.MAX_FILE_SIZE_MB}MB"
            )

        suffix = file_path.suffix.lower()
        try:
            if suffix == ".pdf":
                parsed = self.pdf_parser.parse(file_path)
            elif suffix == ".docx":
                parsed = self.docx_parser.parse(file_path)
            else:
                raise ValueError(f"Unsupported file type: {suffix}")
        except Exception as e:
            raise RuntimeError(f"Failed to parse {file_path.name}: {e}") from e

        parsed["text"] = clean_text(parsed.get("text", ""))
        return parsed

    def ingest_document(self, file_path: Path) -> Dict[str, Any]:
        """Parse, chunk, and store a document in the vector database."""
        parsed = self.parse_document(file_path)
        text = parsed.get("text", "")
        chunks = chunk_document(text)

        metadatas = [
            {
                "source": str(file_path),
                "chunk_index": idx,
            }
            for idx in range(len(chunks))
        ]

        if chunks:
            self.vector_store.add_texts(chunks, metadatas=metadatas)

        return {
            "parsed": parsed,
            "chunks": chunks,
        }

    def answer_question(self, question: str) -> str:
        """Answer a question using retrieved context.
        
        Args:
            question: User's question about the contract
            
        Returns:
            Answer string from the LLM
        """
        if not question or not question.strip():
            return "Please provide a valid question."
            
        docs = self.vector_store.similarity_search(question)
        if not docs:
            return "No relevant information found in the knowledge base. Please upload a contract first."
            
        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = (
            "You are a contract analysis assistant. Use the context to answer. "
            "If the answer is not in the context, say you don't know.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}"
        )
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    def extract_clauses(self, contract_text: str) -> List[Dict[str, Any]]:
        """Extract clauses from contract text."""
        return extract_clauses(contract_text, llm=self.llm)

    def assess_clause_risk(self, clause_type: str, clause_text: str) -> Dict[str, Any]:
        """Assess risk for a clause."""
        return assess_risk(clause_type, clause_text, llm=self.llm)

    def compare_clause(self, clause_text: str) -> Dict[str, Any]:
        """Compare a clause to similar clauses from the vector store."""
        docs = self.vector_store.similarity_search(clause_text)
        retrieved = [doc.page_content for doc in docs]
        return compare_clause(clause_text, retrieved, llm=self.llm)

    def negotiate_clause(self, clause_text: str, risk_level: int | str, concerns: List[str]) -> Dict[str, Any]:
        """Provide negotiation advice for a clause."""
        return negotiation_advice(clause_text, risk_level, concerns, llm=self.llm)

    def explain_clause(self, clause_text: str) -> Dict[str, Any]:
        """Explain a clause in plain English."""
        return explain_clause(clause_text, llm=self.llm)
