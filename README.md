# ContractGuard 🛡️

> AI-powered contract analysis and risk assessment using a multi-agent LangChain pipeline with RAG.

ContractGuard ingests legal contracts (PDF/DOCX), extracts clauses, scores risk against industry standards, and surfaces actionable negotiation advice — all through a conversational Streamlit UI.

## Features

- **Multi-agent orchestration** — dedicated agents for parsing, clause extraction, risk scoring, and explanation
- **RAG pipeline** — clause comparison against a knowledge base of reference contracts via Chroma vector store
- **Risk scoring** — flags high-risk clauses with plain-English explanations
- **Negotiation advice** — actionable suggestions per clause
- **Supports PDF & DOCX** — robust document parsing via PyMuPDF and python-docx

## Architecture

```
ContractGuard/
├── app.py                    # Streamlit entry point
├── config/                   # Prompts and LLM config
├── src/
│   ├── agents/               # Clause extractor, risk scorer, advisor agents
│   ├── orchestration/        # Pipeline coordinator
│   ├── parsers/              # PDF and DOCX parsers
│   ├── rag/                  # Chroma vector store + embeddings
│   ├── ui/                   # Streamlit components
│   └── utils/                # Helpers
├── data/
│   ├── contracts/            # Uploaded contracts
│   ├── knowledge_base/       # Reference contracts for RAG
│   └── vector_store/         # Chroma DB
└── tests/                    # Unit tests
```

## Tech Stack

| Layer | Technology |
|---|---|
| Agent framework | LangChain |
| Vector store | Chroma |
| Embeddings | OpenAI `text-embedding-3-small` |
| LLM | GPT-4o / Ollama (local) |
| UI | Streamlit |
| Parsers | PyMuPDF, python-docx |

## Setup

```bash
git clone https://github.com/pavan-kumar-v-pkv/ContractGuard-Multi-Agent-Legal-Document-Analyzer
cd ContractGuard-Multi-Agent-Legal-Document-Analyzer
pip install -r requirements.txt
cp config/.env.example config/.env  # Add your OPENAI_API_KEY
streamlit run app.py
```

## How It Works

1. Upload a contract (PDF or DOCX)
2. The parser agent extracts raw text and segments it into clauses
3. The RAG agent retrieves similar clauses from the reference knowledge base
4. The risk scorer agent evaluates each clause and assigns a risk tier (Low / Medium / High)
5. The advisor agent generates plain-English explanations and negotiation suggestions
6. Results are displayed interactively in the Streamlit UI

## Example Output

| Clause | Risk | Issue | Suggestion |
|---|---|---|---|
| Limitation of Liability | 🔴 High | Cap too low at 1x fees | Negotiate to 2x or uncapped for IP claims |
| Termination for Convenience | 🟡 Medium | No notice period specified | Request 30-day written notice |
| Governing Law | 🟢 Low | Standard jurisdiction clause | No action needed |

## License

MIT
