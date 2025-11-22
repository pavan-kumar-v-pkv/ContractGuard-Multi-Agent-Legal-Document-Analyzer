"""
Test script for Phase 1: Document Parsing
Run this script to test your document parser
"""

import os
from preprocessing.document_parser import DocumentParser
from preprocessing.text_cleaner import TextCleaner
from preprocessing.metadata_extractor import MetadataExtractor
import json

def test_phase1(file_path: str):
    """
    Test all Phase 1 components
    Args:
        file_path: Path to a sample contract file (PDF or DOCX)
    """
    print("="*60)
    print('Phase 1 TEST: Document Preprocessing')
    print("="*60)

    # Step 1: Parse Document
    print("\n Step 1: Parsing document...")
    parser = DocumentParser(file_path)
    parsed_data = parser.parse()

    print(f"    File: {parsed_data['file_name']}")
    print(f"    Type: {parsed_data['file_type']}")
    if 'total_pages' in parsed_data:
        print(f"    Pages: {parsed_data['total_pages']}")
    print(f"    Text length: {len(parsed_data['full_text'])} characters")

    # Step 2: Extract sections
    print("\n Step 2: Extracting Sections...")
    sections = parser.extract_sections(parsed_data)
    print(f"    Found{len(sections)} sections")
    for i, section in enumerate(sections[:3], 1):
        print(f"    {i}. {section['header'][:50]}...")

    # Step 3: Clean text
    print("\n Step 3: Cleaning text...")
    cleaner = TextCleaner()
    cleaned_text = cleaner.clean(parsed_data['full_text'])
    print(f'    Cleaned text length: {len(cleaned_text)} characters')
    print(f'    First 200 chars: {cleaned_text[:200]}...')

    # Step 4: Extract Metadata
    print("\n Step 4: Extracting metadata...")
    extractor = MetadataExtractor()
    metadata = extractor.extract(cleaned_text)

    print(f'    Contract Type: {metadata.get("contract_type", "N/A")}')
    print(f'    Parties: {metadata.get("parties", [])}')
    print(f'    Dates: {metadata.get("dates", [])}')
    print(f'    Amounts: {metadata.get("amounts", [])}')
    print(f'    Locations: {metadata.get("locations", "N/A")}')
    print(f'    Key Terms: {list(metadata.get("key_terms", []))[:5]}...')

    # Step 5: Save processed data
    print("\n Step 5: Saving processed data to JSON...")
    output_data = {
        "original_file": parsed_data['file_name'],
        "parsed_at": str(parsed_data),
        "sections": sections,
        "cleaned_text": cleaned_text,
        "metadata": metadata
    }
    output_file = f"data/processed/{os.path.splitext(parsed_data['file_name'])[0]}_processed.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"   Saved to: {output_file}")
    
    print("\n" + "=" * 60)
    print(" PHASE 1 COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    # Test with your sample contract
    import sys
    contracts  = [
        "/Users/pavankumarv/dev/ml/Projects/ContractGuard/data/sample_contracts/bad_freelance_contract.pdf",
        "/Users/pavankumarv/dev/ml/Projects/ContractGuard/data/sample_contracts/fair_freelance_contract.pdf",
        "/Users/pavankumarv/dev/ml/Projects/ContractGuard/data/sample_contracts/standard_nda.pdf"
    ]
    for contract in contracts:
        if os.path.exists(contract):
            print(f"\n\n{'='*60}")
            print(f"Testing: {contract}")
            print(f"{'='*60}\n")
            test_phase1(contract)
        else:
            print(f"File not found: {contract}")