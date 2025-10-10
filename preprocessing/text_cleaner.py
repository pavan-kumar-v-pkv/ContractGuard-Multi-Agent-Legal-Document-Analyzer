"""
Text Cleaner - Normalizes and cleans extracted text.
Removes artifacts from PDF extraction.
"""

import re
from typing import List

class TextCleaner:
    """
    Cleans and normalizes contract text
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Main cleaning pipeline
        Args:
            text: Raw text from parser
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Step 1: Remove extra whitespaces
        text = TextCleaner._remove_extra_whitespace(text)
        # Step 2: Fix common PDF artifacts
        text = TextCleaner._fix_pdf_artifacts(text)
        # Step 3: Normalize quotes and dashes
        text = TextCleaner._normalize_punctuation(text)
        # Step 4: Remove page markers
        text = TextCleaner._remove_page_markers(text)

        return text
    
    @staticmethod
    def _remove_extra_whitespace(text: str) -> str:
        """
        Remove multiple spaces and blank lines
        """
        # replace multiple space with single space
        text = re.sub(r' +', ' ', text)

        # replace multiple newlines with double newline
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

        return text.strip()
    
    @staticmethod
    def _fix_pdf_artifacts(text: str) -> str:
        """
        Fix common PDF extraction issues
        """
        # remove weird characters that appear in PDFs
        text = text.replace('\x00', '')
        text = text.replace('\uf0b7', '•') # Bullet point
        text = text.replace('\u2022', '•')

        # Fix broken words (e.g., "con-tract" -> "contract")
        text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)

        return text
    
    @staticmethod
    def _normalize_punctuation(text: str) -> str:
        """
        Standardize quotes, dashes, etc.
        """
        # Replace smart quotes with regualr quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")

        # Standardize dashes
        text = text.replace('–', '-').replace('—', '-')

        return text

    @staticmethod
    def _remove_page_markers(text: str) -> str:
        """
        Remove 'Page X of Y' type markers
        """
        # Remove page numbers
        text = re.sub(r'--- Page \d+ ---', '', text)
        text = re.sub(r'Page \d+ of \d+', '', text)
        
        return text
    
    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """
        Split text into sentences (useful for later analysis)
        Args:
            text: Cleaned text
        Returns:
            List of sentences
        """
        # Simple sentence splitter (spaCy will do better job)
        sentences = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in sentences if s.strip()]
    

# Helper function
def clean_text(text: str) -> str:
    """Quick cleaning function"""
    return TextCleaner.clean(text)