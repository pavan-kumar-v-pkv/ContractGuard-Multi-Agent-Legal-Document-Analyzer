"""Streamlit UI for ContractGuard."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import streamlit as st
from dotenv import load_dotenv

from config.settings import settings
from src.orchestration.pipeline import ContractGuardPipeline


DATA_DIR = Path(settings.data_dir)
CONTRACTS_DIR = DATA_DIR / "contracts"
CONTRACTS_DIR.mkdir(parents=True, exist_ok=True)


def _ensure_pipeline() -> ContractGuardPipeline | None:
    if "pipeline" not in st.session_state:
        try:
            st.session_state["pipeline"] = ContractGuardPipeline()
        except Exception as exc:  # noqa: BLE001
            st.error(f"Failed to initialize pipeline: {exc}")
            return None
    return st.session_state["pipeline"]


def _save_upload(uploaded_file) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{timestamp}_{uploaded_file.name}"
    file_path = CONTRACTS_DIR / safe_name
    file_path.write_bytes(uploaded_file.getbuffer())
    return file_path


def _display_json(data: Any) -> None:
    if isinstance(data, (dict, list)):
        st.json(data)
    else:
        st.write(data)


def run_app() -> None:
    load_dotenv()
    st.set_page_config(page_title=settings.APP_NAME, layout="wide")
    st.title("ContractGuard")
    st.caption("AI-assisted contract analysis and risk assessment")

    pipeline = _ensure_pipeline()
    if not pipeline:
        return

    with st.sidebar:
        st.subheader("Upload & Ingest")
        uploaded_file = st.file_uploader(
            "Upload a contract (PDF/DOCX)",
            type=["pdf", "docx"],
            accept_multiple_files=False,
        )
        if uploaded_file:
            st.info(f"Selected: {uploaded_file.name}")
            if st.button("Ingest Document", type="primary"):
                try:
                    file_path = _save_upload(uploaded_file)
                    result = pipeline.ingest_document(file_path)
                    st.session_state["last_parsed"] = result["parsed"]
                    st.session_state["last_file"] = str(file_path)
                    st.success("Document ingested and indexed.")
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Ingestion failed: {exc}")

        st.divider()
        st.subheader("Settings")
        st.write(f"Provider: {settings.LLM_PROVIDER}")
        st.write(f"Model: {settings.OPENAI_MODEL if settings.LLM_PROVIDER == 'openai' else settings.OLLAMA_MODEL}")
        st.write(f"Top-K: {settings.TOP_K_RETRIEVAL}")

    tab_ask, tab_clauses = st.tabs(["Ask", "Clauses & Analysis"])

    with tab_ask:
        st.subheader("Ask a question")
        question = st.text_area("Question", height=100, placeholder="What are the payment terms?")
        if st.button("Get Answer"):
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                try:
                    answer = pipeline.answer_question(question)
                    st.markdown("**Answer**")
                    st.write(answer)
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Failed to answer: {exc}")

    with tab_clauses:
        st.subheader("Extract and analyze clauses")
        parsed = st.session_state.get("last_parsed")
        if not parsed:
            st.info("Upload and ingest a contract to extract clauses.")
            return

        if st.button("Extract Clauses"):
            try:
                clauses = pipeline.extract_clauses(parsed.get("text", ""))
                st.session_state["clauses"] = clauses
            except Exception as exc:  # noqa: BLE001
                st.error(f"Clause extraction failed: {exc}")

        clauses: List[Dict[str, Any]] | None = st.session_state.get("clauses")
        if not clauses:
            st.info("No clauses extracted yet.")
            return

        clause_labels = [
            f"{idx + 1}. {c.get('type', 'Clause')} - {c.get('title', 'Untitled')}"
            for idx, c in enumerate(clauses)
        ]
        selected_idx = st.selectbox("Select a clause", list(range(len(clauses))), format_func=lambda i: clause_labels[i])
        selected_clause = clauses[selected_idx]

        st.markdown("**Clause Text**")
        st.write(selected_clause.get("text", ""))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Assess Risk"):
                try:
                    risk = pipeline.assess_clause_risk(
                        selected_clause.get("type", "Clause"),
                        selected_clause.get("text", ""),
                    )
                    st.session_state["risk"] = risk
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Risk assessment failed: {exc}")
        with col2:
            if st.button("Compare"):
                try:
                    comparison = pipeline.compare_clause(selected_clause.get("text", ""))
                    st.session_state["comparison"] = comparison
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Comparison failed: {exc}")
        with col3:
            if st.button("Explain"):
                try:
                    explanation = pipeline.explain_clause(selected_clause.get("text", ""))
                    st.session_state["explanation"] = explanation
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Explanation failed: {exc}")
        with col4:
            if st.button("Negotiate"):
                try:
                    risk = st.session_state.get("risk") or {}
                    advice = pipeline.negotiate_clause(
                        selected_clause.get("text", ""),
                        risk.get("risk_level", "N/A"),
                        risk.get("concerns", []),
                    )
                    st.session_state["negotiation"] = advice
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Negotiation advice failed: {exc}")

        st.divider()
        st.subheader("Analysis Outputs")
        if st.session_state.get("risk"):
            st.markdown("**Risk Assessment**")
            _display_json(st.session_state["risk"])
        if st.session_state.get("comparison"):
            st.markdown("**Comparison**")
            _display_json(st.session_state["comparison"])
        if st.session_state.get("explanation"):
            st.markdown("**Plain-English Explanation**")
            _display_json(st.session_state["explanation"])
        if st.session_state.get("negotiation"):
            st.markdown("**Negotiation Advice**")
            _display_json(st.session_state["negotiation"])
