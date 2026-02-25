#!/usr/bin/env python3
"""Setup script to initialize the ContractGuard project."""

import os
import sys
from pathlib import Path


def create_directories():
    """Create necessary project directories."""
    dirs = [
        "data/contracts",
        "data/knowledge_base",
        "data/sample_contracts",
        "data/vector_store",
        "output",
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")


def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("\n⚠️  .env file not found!")
        print("Creating a template .env file...")
        
        template = """# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here

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
"""
        env_path.write_text(template)
        print("✓ Created .env template")
        print("\n⚠️  Please edit .env and add your OPENAI_API_KEY")
        return False
    else:
        # Check if API key is set
        content = env_path.read_text()
        if "your-api-key-here" in content or "OPENAI_API_KEY=sk-" not in content:
            print("\n⚠️  Please set your OPENAI_API_KEY in .env file")
            return False
        print("✓ .env file exists with API key")
        return True


def check_dependencies():
    """Check if all required packages are installed."""
    required_packages = [
        "streamlit",
        "langchain",
        "chromadb",
        "pdfplumber",
        "python-docx",
        "pydantic",
        "python-dotenv",
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("\n⚠️  Missing packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nRun: pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies installed")
    return True


def main():
    """Run setup checks."""
    print("ContractGuard Setup\n" + "=" * 50)
    
    print("\n1. Creating directories...")
    create_directories()
    
    print("\n2. Checking dependencies...")
    deps_ok = check_dependencies()
    
    print("\n3. Checking environment configuration...")
    env_ok = check_env_file()
    
    print("\n" + "=" * 50)
    
    if deps_ok and env_ok:
        print("✅ Setup complete! You're ready to run ContractGuard.")
        print("\nTo start the app, run:")
        print("  streamlit run app.py")
    else:
        print("⚠️  Setup incomplete. Please resolve the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
