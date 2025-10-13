"""
Metadata Extractor - Finds key entities in contracts
Using NLP techniques to extract metadata such as parties, dates, and contract types.
"""

import re
from typing import Dict, List
import spacy
from datetime import datetime

class MetadataExtractor:
    """
    Extracts structured metadata from contract text
    """

    def __init__(self):
        """Load spacy model for NER"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("Loaded spacy model 'en_core_web_sm'")
        except:
            print("Spacy model 'en_core_web_sm' not found. Please install it using 'python -m spacy download en_core_web_sm'")
            raise

    def extract(self, text: str) -> Dict:
        """
        Extract all metadata from contract
        Args:
            text: Cleaned contract text
        Returns:
            Dictionary with extracted metadata
        """
        metadata = {
            'parties': self._extract_parties(text),
            'dates': self._extract_dates(text),
            'amounts': self._extract_amounts(text),
            'locations': self._extract_locations(text),
            'contract_type': self._guess_contract_type(text),
            'key_terms': self._extract_key_terms(text)
        }

        return metadata
    
    def _extract_parties(self, text: str) -> List[str]:
        """
        Find party names (people/organizations) using NER
        """
        # Parties are usually mentioned at the start of the contract
        doc = self.nlp(text[:5000])  # Analyze first 2000 characters

        parties = []
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG']:
                parties.append(ent.text)

        # Remove duplicates while preserving order
        unique_parties = []
        seen = set()
        for party in parties:
            if party.lower() not in seen:
                seen.add(party.lower())
                unique_parties.append(party)

        return unique_parties[:5]
    
    def _extract_dates(self, text: str) -> List[str]:
        """Find dates in contract using regex and NER"""
        # Pattern for common date formats
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',  # MM/DD/YYYY -> 01/15/2021
            r'\d{1,2}-\d{1,2}-\d{2,4}',  # MM-DD-YYYY -> 01-15-2021
            r'[A-Z][a-z]+ \d{1,2},? \d{4}',  # Month DD, YYYY -> January 15, 2021
            r'\d{1,2} [A-Z][a-z]+ \d{4}',  # DD Month YYYY -> 15 January 2021
        ]

        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)

        return dates[:10]
    
    def _extract_amounts(self, text: str) -> List[str]:
        """Find monetary amounts in contract using regex and NER"""
        # Pattern for currency amounts
        money_pattern = r'(?:₹|Rs\.?)\s?[\d,]+(?:\.\d{1,2})?'

        amounts = re.findall(money_pattern, text, re.IGNORECASE)
        # Clean up the tuples returned by findall
        amounts = [match[0] if isinstance(match, tuple) else match for match in amounts]

        return amounts[:10]
    
    def _extract_locations(self, text: str) -> List[str]:
        """Find locations (cities, states, countries) using NER"""
        doc = self.nlp(text)

        locations = []
        for ent in doc.ents:
            # GPE = Geopolitical Entity (countries, cities, states)
            if ent.label_ == 'GPE':
                locations.append(ent.text)

        # Remove duplicates while preserving order
        return list(set(locations))[:5]
    
    def _guess_contract_type(self, text: str) -> str:
        """Guess what type of contract this is based on keywords"""
        text_lower = text.lower()

        # keywords for different contract types
        if 'non-disclosure' in text_lower or 'nda' in text_lower or 'confidential' in text_lower:
            return 'Non-Disclosure Agreement (NDA)'
        elif 'employment' in text_lower or 'employee' in text_lower:
            return 'Employment Agreement'
        elif 'freelance' in text_lower or 'independent contractor' in text_lower:
            return 'Freelance/Independent Contractor Agreement'
        elif 'service' in text_lower or 'software' in text_lower:
            return 'Software as a Service (SaaS) Agreement'
        elif 'lease' in text_lower or 'tenant' in text_lower or 'landlord' in text_lower or 'rental' in text_lower:
            return 'Lease Agreement'
        elif 'partnership' in text_lower or 'partner' in text_lower:
            return 'Partnership Agreement'
        elif 'sales' in text_lower or 'purchase' in text_lower or 'buyer' in text_lower or 'seller' in text_lower:
            return 'Sales/Purchase Agreement'
        elif 'loan' in text_lower or 'borrower' in text_lower or 'lender' in text_lower:
            return 'Loan Agreement'
        else:
            return 'General Contract'
        
    def _extract_key_terms(self, text: str) -> Dict:
        """
        Find important terms mentioned in the contract
        e.g., termination notice period, governing law, renewal terms
        """
        text_lower = text.lower()

        terms = {
            'has_termination_clause': 'termination' in text_lower or 'terminate' in text_lower,
            'has_governing_law': 'governing law' in text_lower,
            'has_renewal_terms': 'renewal' in text_lower,
            'has_confidentiality': 'confidentiality' in text_lower or 'non-disclosure' in text_lower or 'nda' in text_lower or 'confidential' in text_lower,
            'has_ip_clause': 'intellectual property' in text_lower or 'ip rights' in text_lower,
            'has_liability_clause': 'liability' in text_lower or 'indemnity' in text_lower,
            'has_dispute_resolution': 'dispute resolution' in text_lower or 'arbitration' in text_lower or 'mediation' in text_lower,
            'has_non_compete': 'non-compete' in text_lower or 'non competition' in text_lower,
        }

        return terms
    
    # Helper function
    def extract_metadata(text: str) -> Dict:
        """Quick metadata extraction function"""
        extractor = MetadataExtractor()
        return extractor.extract(text)
