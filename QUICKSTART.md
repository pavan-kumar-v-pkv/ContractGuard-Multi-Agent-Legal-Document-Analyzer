# Quick Start Guide

## 1. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## 2. Configure API Key

Edit `.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## 3. Run the App

```bash
streamlit run app.py
```

## 4. Upload a Contract

1. Click "Upload a contract" in the sidebar
2. Select a PDF or DOCX file
3. Click "Ingest Document"

## 5. Analyze Clauses

1. Go to "Clauses & Analysis" tab
2. Click "Extract Clauses"
3. Select a clause
4. Use buttons to:
   - **Assess Risk**: Identify potential issues
   - **Compare**: Compare to standards
   - **Explain**: Get plain-English translation
   - **Negotiate**: Get negotiation tips

## Using Ollama (Local LLMs)

For privacy or cost savings:

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama3:8b`
3. Update `.env`:
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_MODEL=llama3:8b
   ```

## Troubleshooting

**"API key not set" error**: 
- Check your `.env` file has `OPENAI_API_KEY=sk-...`

**"No results found"**:
- Make sure you ingested a document first

**Import errors**:
- Activate virtual environment: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

## Example Workflow

```python
from pathlib import Path
from src.orchestration.pipeline import ContractGuardPipeline

# Initialize
pipeline = ContractGuardPipeline()

# Ingest contract
result = pipeline.ingest_document(Path("contract.pdf"))

# Extract clauses
clauses = pipeline.extract_clauses(result["parsed"]["text"])

# Assess first clause
risk = pipeline.assess_clause_risk(
    clauses[0]["type"], 
    clauses[0]["text"]
)
print(f"Risk Level: {risk['risk_level']}/10")
```

## Next Steps

- Read the full [README.md](README.md)
- Add reference contracts to `data/knowledge_base/`
- Check out example contracts in `data/sample_contracts/`
