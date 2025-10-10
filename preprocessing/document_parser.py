"""
Document Parser - This extracts text from PDF and Word documents.
Preserves structure such as headings, headers, page numbers etc.
"""
import os
from typing import Dict, List, Optional
import pdfplumber
from docx import Document
import re

class DocumentParser:
    """
    Main class for parsing legal documents
    """

    def __init__(self, file_path: str):
        """
        Initialize parser with file path
        Args:
            file_path: Path to PDF or DOCX file
        """

        self.file_path = file_path
        self.file_type = self._detect_file_type()

    def _detect_file_type(self) -> str:
        """Detect if file is PDF or DOCX"""
        extension = os.path.splitext(self.file_path)[1].lower()

        if extension == ".pdf":
            return "pdf"
        elif extension in [".docx", ".doc"]:
            return "docx"
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        
    def parse(self) -> Dict:
        """
        Main parsing method - routes to appropriate parser
        Returns:
            Dictionary with extracted content
        """
        if self.file_type == "pdf":
            return self._parse_pdf()
        else:
            return self._parse_docx()
        
    def _parse_pdf(self) -> Dict:
        """
        Parse PDF file and extract structured content
        """
        result = {
            'file_name': os.path.basename(self.file_path),
            'file_type': 'pdf',
            'pages': [],
            'full_text': '',
            'total_pages': 0
        }

        try:
            with pdfplumber.open(self.file_path) as pdf:
                result['total_pages'] = len(pdf.pages)

                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extract text from page
                    text = page.extract_text()
                    
                    if text:
                        # Store page info
                        page_data = {
                            'page_number': page_num,
                            'text': text,
                            'char_count': len(text)
                        }
                        result['pages'].append(page_data)
                        result['full_text'] += f"\n\n--- Page {page_num} ---\n\n{text}"

                    print(f"Successfully parsed  {result['total_pages']} pages from PDF.")
                    return result
        except Exception as e:
            print(f"Error parsing PDF: {str(e)}")
            raise

    def _parse_docx(self) -> Dict:
        """
        Parse DOCX file and extract structured content
        """
        result = {
            'file_name': os.path.basename(self.file_path),
            'file_type': 'docx',
            'paragraphs': [],
            'full_text': '',
            'total_paragraphs': 0
        }

        try:
            doc = Document(self.file_path)

            for para_num, paragraph in enumerate(doc.paragraphs, start=1):
                text = paragraph.text.strip()

                if text:
                    # Skip empty paragpraphs
                    para_data = {
                        'paragraph_number': para_num,
                        'text': text,
                        'style': paragraph.style.name # Header, normal, etc.
                    }
                    result['paragraphs'].append(para_data)
                    result['full_text'] += f"{text}\n\n"

                result['total_paragraphs'] = len(result['paragraphs'])
                print(f'Successfully parsed {result['total_paragraphs']} paragraphs from DOCX')
                return result

        except Exception as e:
            print(f"Error parsing DOCX: {str(e)}")
            raise

    def extract_sections(self, parsed_content: Dict) -> List[Dict]:
        """
        Split document into logical sections based on headers/numbering
        Args:
            parsed_content: Output from parse() method
        Returns:
            List of sections with headers and content
        """
        sections = []
        current_section = None

        # Pattern to dectect section headers (e.g., "1.", "Article 3", "Section A")
        header_pattern = re.compile(r'^(\d+\.|Article\s+\d+|Section\s+[A-Z]|[A-Z]\.|[IVX]+\.)', re.IGNORECASE)

        text = parsed_content['full_text']
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this line is a header
            if header_pattern.match(line) or line.isupper() and len(line) < 100:
                # Save previous section
                if current_section:
                    sections.append(current_section)

                # Start new section
                current_section = {
                    'header': line,
                    'content': ''
                }
            else:
                # Add to current section
                if current_section:
                    current_section['content'] += f"{line}\n"
                else:
                    # Content before first header
                    if not sections:
                        current_section = {
                            'header': 'Preamble',
                            'content': f"{line}\n"
                        }

        # last section
        if current_section:
            sections.append(current_section)

        print(f"Extracted {len(sections)} sections from document")
        return sections
    
    # Helper function for easy use
    def parse_document(file_path: str) -> Dict:
        """
        Quick function to parse a document
        Args:
            file_path: Path to PDF or DOCX
        Returns:
            Parsed document dictionary
        """
        parser = DocumentParser(file_path=file_path)
        return parser.parse()
