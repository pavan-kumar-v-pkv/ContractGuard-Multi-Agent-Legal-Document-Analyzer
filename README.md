# ContractGuard 🛡️

AI-powered contract analysis and risk assessment tool using LangChain, RAG, and multi-agent architecture.

## Features

- **Document Parsing**: Extract text from PDF and DOCX contracts
- **Clause Extraction**: Automatically identify and categorize contract clauses
- **Risk Assessment**: Analyze clauses for potential risks and concerns
- **Comparison**: Compare clauses against industry standards using RAG
- **Plain-English Explanation**: Translate legal jargon into simple language
- **Negotiation Advice**: Get actionable suggestions for contract negotiation
- **Interactive UI**: Streamlit-based interface for easy interaction

## Architecture

```
ContractGuard/
├── app.py                  # Main Streamlit entry point
├── config/                 # Configuration and prompts
├── src/
│   ├── agents/            # LLM-powered agents (clause extraction, risk, etc.)
│   ├── orchestration/     # Main pipeline orchestration
│   ├── parsers/           # PDF and DOCX parsers
│   ├── rag/              # Vector store and embeddings
│   ├── ui/               # Streamlit UI
│   └── utils/            # Helper utilities
└── data/
    ├── contracts/        # Uploaded contracts
    ├── knowledge_base/   # Reference contracts
    └── vector_store/     # Chroma vector database
```

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key (or Ollama for local LLM)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd ContractGuard
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   Create a `.env` file in the root directory:
   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=sk-your-api-key-here
   
   # LLM Settings
   LLM_PROVIDER=openai
   OPENAI_MODEL=gpt-4o-mini
   EMBEDDING_MODEL=text-embedding-3-small
   TEMPERATURE=0.1
   
   # RAG Settings
   VECTOR_STORE_PATH=./data/vector_store
   CHUNK_SIZE=512
   CHUNK_OVERLAP=100
   TOP_K_RETRIEVAL=5
   
   # App Settings
   DEBUG=True
   MAX_FILE_SIZE_MB=10
   TIMEOUT_SECONDS=60
   ```

### Using Ollama (Optional)

To use local LLMs with Ollama:

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama3:8b`
3. Update `.env`:
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3:8b
   ```

## Usage

### Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### Workflow

1. **Upload a Contract**: 
   - Click "Upload a contract" in the sidebar
   - Select a PDF or DOCX file
   - Click "Ingest Document" to parse and index it

2. **Ask Questions**:
   - Use the "Ask" tab to query the contract
   - Example: "What are the payment terms?"

3. **Analyze Clauses**:
   - Use the "Clauses & Analysis" tab
   - Click "Extract Clauses" to identify all clauses
   - Select a clause to analyze
   - Use action buttons:
     - **Assess Risk**: Identify potential risks
     - **Compare**: Compare to industry standards
     - **Explain**: Get plain-English explanation
     - **Negotiate**: Get negotiation advice

### Programmatic Usage

```python
from pathlib import Path
from src.orchestration.pipeline import ContractGuardPipeline

# Initialize pipeline
pipeline = ContractGuardPipeline()

# Parse a contract
contract_path = Path("data/contracts/sample.pdf")
result = pipeline.ingest_document(contract_path)

# Extract clauses
clauses = pipeline.extract_clauses(result["parsed"]["text"])

# Assess risk for a clause
risk = pipeline.assess_clause_risk(
    clause_type="Payment Terms",
    clause_text="Payment is due within 30 days..."
)

# Answer questions
answer = pipeline.answer_question("What are the termination conditions?")
```

## Project Structure

### Key Components

- **Parsers** ([src/parsers](src/parsers)):
  - `pdf_parser.py`: Extract text and sections from PDFs
  - `docx_parser.py`: Parse Word documents
  - `chunker.py`: Text chunking for RAG

- **Agents** ([src/agents](src/agents)):
  - `clause_extractor.py`: Extract and categorize clauses
  - `risk_assessor.py`: Assess clause risks
  - `comparison_agent.py`: Compare to standards
  - `negotiation_advisor.py`: Generate negotiation advice
  - `explainer.py`: Plain-language explanations

- **RAG** ([src/rag](src/rag)):
  - `vector_store.py`: Chroma vector store manager
  - `embeddings.py`: Embedding model factory

- **Pipeline** ([src/orchestration/pipeline.py](src/orchestration/pipeline.py)):
  - Orchestrates all components
  - Main interface for contract processing

## Configuration

All settings are in [config/settings.py](config/settings.py) and can be overridden via environment variables.

Key settings:
- `LLM_PROVIDER`: "openai" or "ollama"
- `OPENAI_MODEL`: GPT model to use (e.g., "gpt-4o-mini")
- `CHUNK_SIZE`: Text chunk size for RAG
- `TOP_K_RETRIEVAL`: Number of similar chunks to retrieve

## Development

### Run Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 src/
```

### Add New Agents

1. Create a new agent file in `src/agents/`
2. Add a prompt template in `config/prompts.py`
3. Import and use in `src/orchestration/pipeline.py`

## Troubleshooting

**Issue**: `OPENAI_API_KEY is not set`
- **Solution**: Add your API key to `.env` file

**Issue**: Empty vector store results
- **Solution**: Upload and ingest at least one contract first

**Issue**: Module import errors
- **Solution**: Ensure virtual environment is activated and dependencies installed

**Issue**: Ollama connection refused
- **Solution**: Start Ollama service: `ollama serve`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built with [LangChain](https://langchain.com)
- UI powered by [Streamlit](https://streamlit.io)
- Vector store using [Chroma](https://www.trychroma.com)
