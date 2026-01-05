"""PDF document parser with section detection."""

import pdfplumber
import re
from typing import Dict, List, Tuple
from pathlib import Path

class PDFParser:
    """
    Extract text, metadata, and sections from PDF files.

    This parser:
    1. EXtracts raw text from all PDF pages.
    2. Detects contract sections using regex patterns
    3. Preserves document structure (sections, numbering)
    3. Extracts tables if present
    """

    def __init__(self):
        """Initialize PDF parser."""
        # Regex patterns for detecting section headers
        # Matches: "1.",  "1.1", "Section 1", "Article I", etc.
        self.section_patterns = [
            r'^(\d+)\.\s+([A-Z][^\n]+)',           # "1. DEFINITIONS"
            r'^(\d+\.\d+)\s+([A-Z][^\n]+)',        # "1.1 Services"
            r'^Section\s+(\d+)[:\.]?\s*([^\n]*)',  # "Section 1: Definitions"
            r'^Article\s+(\d+)[:\.]?\s*([^\n]*)',  # "Article 5: Payment"
            r'^Clause\s+([A-Z\d]+)[:\.]?\s*([^\n]*)',  # "Clause A: Terms"
            r'^([A-Z]+)\.\s+([A-Z][^\n]+)',        # "A. DEFINITIONS"
        ]

    def parse(self, file_path: Path) -> Dict:
        """
        Parse PDF file and extract all content.

        Args:
            file_path: Path to PDF file

        Returns:
            Dictionary containing:
                - text:  Full document text
                - pages: List of text per page
                - sections: List of detected sections
                - metadata: PDF metadata (pages, title, author)
                - tables: Extracted tables (if any)
        """
        try:
            # Open PDF file
            with pdfplumber.open(str(file_path)) as pdf:

                # Step 1: Extract Metadata
                metadata = {
                    'num_pages': len(pdf.pages),
                    'title': pdf.metadata.get('Title', 'Unknown'),
                    'author': pdf.metadata.get('Author', 'Unknown'),
                    'creator': pdf.metadata.get('Creator', 'Unknown'),
                }

                # Step 2: Extract text from all pages
                pages = []
                full_text = ""

                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extrarct text from current page
                    page_text = page.extract_text()

                    if page_text:
                        # Store individual page text
                        pages.append(page_text)

                        # Add to full document text with page marker
                        full_text += f"\n--- PAGE {page_num} ---\n"
                        full_text += page_text + "\n"

                # Step 3: Extract tables if present
                tables = []
                for page in pdf.pages:
                    # EXtract tables from current page
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)

                # Step 4: Detect sections
                sections = self._detect_sections(full_text)

                # Step 5: Return everything
                return {
                    'text': full_text.strip(),
                    'pages': pages,
                    'sections': sections,
                    'metadata': metadata,
                    'tables': tables
                }
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {str(e)}")

    def _detect_sections(self, text: str) -> List[Dict[str, str]]:
        """
        Detect sections in the document text using regex patterns.

        This methid finds sections headers like
        "1. DEFINITIONS", "Section 2: Payment Terms", etc.

        Args:
            text: Full document text

        Returns:
            List of sections with:
                - number: Section number or identifier (e.g., "1.1", "A")
                - title: Section title
                - content: Section text content
                - start_pos: Start position in the full text
        """
        sections = []
        lines = text.split('\n')

        # Track positions for content extraction
        current_position = 0

        # Step 1: Final all sections headers
        section_matches = []

        for line_idx, line in enumerate(lines):
            line_stripped = line.strip()

            # Skip empty lines
            if not line_stripped:
                current_position += len(line) + 1 # +1 for newline
                continue

            # Try each regex pattern
            for pattern in self.section_patterns:
                match = re.match(pattern, line_stripped)

                if match:
                    # Extract section number and title
                    section_num = match.group(1)
                    section_title = match.group(2).strip() if len(match.groups()) > 1 else ""

                    section_matches.append({
                        'number': section_num,
                        'title': section_title,
                        'line_idx': line_idx,
                        'start_post': current_position
                    })
                    break # found a match, stop trying other patterns
            current_position += len(line) + 1 # +1 for newline

        # Step 2: Extract Content Between Sections
        for i, section_match in enumerate(section_matches):
            start_line = section_match['line_idx']

            # Determine where this section ends (start of next section or end of document)
            if i < len(section_matches) - 1:
                end_line = section_matches[i+1]['line_idx']
            else:
                end_line = len(lines)

            # Extract content between section header and next section
            content_lines = lines[start_line + 1:end_line]
            content = '\n'.join(content_lines).strip()

            # Only add if there's actual content
            if content:
                sections.append({
                    'number': section_match['number'],
                    'title': section_match['title'],
                    'content': content,
                    'start_pos': section_match['start_pos']
                })

        return sections5