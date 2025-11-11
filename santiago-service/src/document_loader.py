#!/usr/bin/env python3
"""
Santiago Layer 0: Document Loading and Deep Asset Linking

Implements document loading capabilities for clinical guidelines and knowledge sources.
Creates Layer 0 representations in the knowledge graph with deep linking capabilities
for traceability from all higher layers back to source content.

Based on lessons learned: "We learned that we need to load the original knowledge
document and create a layer 0 in the graph to support deep asset linking from all
of the other layers. We should be able to trace back any asset, logic, decision table,
workflow back to the text."

Author: GitHub Copilot
Date: November 10, 2025
"""

import json
import os
import re
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Document processing libraries
try:
    import PyPDF2
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DocumentMetadata:
    """Metadata for a loaded document"""
    id: str
    title: str
    source: str
    version: str
    publication_date: Optional[str]
    authors: List[str]
    organization: Optional[str]
    document_type: str  # guideline, study, protocol, etc.
    format: str  # pdf, html, text, xml
    file_path: Optional[str]
    url: Optional[str]
    checksum: str
    loaded_at: str
    sections: List[Dict[str, Any]]
    toc: List[Dict[str, Any]]  # Table of contents

@dataclass
class DocumentSection:
    """Represents a section within a document"""
    id: str
    title: str
    content: str
    level: int  # Heading level (1-6)
    start_position: int  # Character position in full text
    end_position: Optional[int] = None
    parent_id: Optional[str] = None
    subsections: List[str] = None
    anchors: List[Dict[str, Any]] = None  # Reference anchors within section

    def __post_init__(self):
        if self.subsections is None:
            self.subsections = []
        if self.anchors is None:
            self.anchors = []

@dataclass
class DocumentAnchor:
    """Reference anchor within document content"""
    id: str
    text: str
    section_id: str
    position: int
    context: str  # Surrounding text for context
    anchor_type: str  # table, figure, recommendation, etc.
    metadata: Dict[str, Any]

class DocumentLoader:
    """
    Layer 0 Document Loader for Santiago

    Loads clinical documents and creates structured representations with deep linking
    capabilities for traceability throughout the knowledge graph.
    """

    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path) if storage_path else Path("data/documents")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.loaded_documents: Dict[str, DocumentMetadata] = {}

    def load_document(self, source: Union[str, Path],
                     metadata: Dict[str, Any]) -> DocumentMetadata:
        """
        Load a document from various sources and create Layer 0 representation

        Args:
            source: File path, URL, or content string
            metadata: Document metadata

        Returns:
            DocumentMetadata with full document structure
        """
        logger.info(f"Loading document: {metadata.get('title', 'Unknown')}")

        # Determine document type and load content
        if isinstance(source, (str, Path)) and Path(source).exists():
            content, format_type = self._load_from_file(source)
        elif isinstance(source, str) and source.startswith(('http://', 'https://')):
            content, format_type = self._load_from_url(source)
        else:
            content = str(source)
            format_type = 'text'

        # Generate document ID and checksum
        doc_id = self._generate_document_id(metadata, content)
        checksum = self._calculate_checksum(content)

        # Parse document structure
        sections, toc = self._parse_document_structure(content, format_type)

        # Create document metadata
        doc_metadata = DocumentMetadata(
            id=doc_id,
            title=metadata.get('title', 'Unknown'),
            source=metadata.get('source', 'Unknown'),
            version=metadata.get('version', '1.0'),
            publication_date=metadata.get('publication_date'),
            authors=metadata.get('authors', []),
            organization=metadata.get('organization'),
            document_type=metadata.get('document_type', 'guideline'),
            format=format_type,
            file_path=str(source) if isinstance(source, (str, Path)) else None,
            url=str(source) if isinstance(source, str) and source.startswith(('http://', 'https://')) else None,
            checksum=checksum,
            loaded_at=datetime.now().isoformat(),
            sections=[asdict(section) for section in sections],
            toc=toc
        )

        # Store document content and metadata
        self._store_document(doc_id, content, doc_metadata)

        # Cache in memory
        self.loaded_documents[doc_id] = doc_metadata

        logger.info(f"Successfully loaded document {doc_id} with {len(sections)} sections")
        return doc_metadata

    def get_document_content(self, doc_id: str, section_id: Optional[str] = None) -> str:
        """
        Retrieve document content, optionally for a specific section

        Args:
            doc_id: Document identifier
            section_id: Optional section identifier

        Returns:
            Document content or section content
        """
        if doc_id not in self.loaded_documents:
            self._load_document_from_storage(doc_id)

        doc_metadata = self.loaded_documents[doc_id]
        content_path = self.storage_path / doc_id / "content.txt"

        if not content_path.exists():
            raise FileNotFoundError(f"Document content not found: {content_path}")

        with open(content_path, 'r', encoding='utf-8') as f:
            full_content = f.read()

        if section_id:
            # Find section boundaries
            section_data = next((s for s in doc_metadata.sections if s['id'] == section_id), None)
            if section_data:
                start_pos = section_data['start_position']
                end_pos = section_data['end_position']
                return full_content[start_pos:end_pos]
            else:
                raise ValueError(f"Section {section_id} not found in document {doc_id}")

        return full_content

    def create_anchor_reference(self, doc_id: str, section_id: str,
                              anchor_text: str, anchor_type: str,
                              position: int, context: str) -> str:
        """
        Create a deep link reference to specific content within a document

        Args:
            doc_id: Document identifier
            section_id: Section identifier
            anchor_text: Text being referenced
            anchor_type: Type of anchor (recommendation, table, figure, etc.)
            position: Character position in document
            context: Surrounding context text

        Returns:
            Anchor reference ID
        """
        anchor_id = f"{doc_id}_{section_id}_anchor_{hashlib.md5(anchor_text.encode()).hexdigest()[:8]}"

        anchor = DocumentAnchor(
            id=anchor_id,
            text=anchor_text,
            section_id=section_id,
            position=position,
            context=context,
            anchor_type=anchor_type,
            metadata={
                'doc_id': doc_id,
                'created_at': datetime.now().isoformat(),
                'anchor_type': anchor_type
            }
        )

        # Store anchor reference
        self._store_anchor(anchor)

        return anchor_id

    def resolve_anchor_reference(self, anchor_id: str) -> Dict[str, Any]:
        """
        Resolve an anchor reference to get full context and content

        Args:
            anchor_id: Anchor reference identifier

        Returns:
            Anchor details with content and context
        """
        # Extract doc_id from anchor_id (everything before '_section_')
        if '_section_' not in anchor_id:
            raise ValueError(f"Invalid anchor ID format: {anchor_id}")

        doc_id = anchor_id.split('_section_')[0]

        # Load anchor from storage
        anchor_path = self.storage_path / doc_id / "anchors" / f"{anchor_id}.json"

        if not anchor_path.exists():
            raise FileNotFoundError(f"Anchor not found: {anchor_id}")

        with open(anchor_path, 'r', encoding='utf-8') as f:
            anchor_data = json.load(f)

        # Get document and section content
        section_id = anchor_data['section_id']

        doc_content = self.get_document_content(doc_id)
        section_content = self.get_document_content(doc_id, section_id)

        return {
            'anchor': anchor_data,
            'document_content': doc_content,
            'section_content': section_content,
            'full_context': self._get_anchor_context(doc_content, anchor_data['position'], 500)
        }

    def _load_from_file(self, file_path: Union[str, Path]) -> Tuple[str, str]:
        """Load content from a file"""
        file_path = Path(file_path)

        if file_path.suffix.lower() == '.pdf':
            if not HAS_PDF:
                raise ImportError("PyPDF2 required for PDF processing")
            return self._load_pdf(file_path), 'pdf'
        elif file_path.suffix.lower() in ['.html', '.htm']:
            if not HAS_BS4:
                raise ImportError("BeautifulSoup required for HTML processing")
            return self._load_html(file_path), 'html'
        elif file_path.suffix.lower() == '.xml':
            return self._load_xml(file_path), 'xml'
        else:
            # Assume plain text
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read(), 'text'

    def _load_from_url(self, url: str) -> Tuple[str, str]:
        """Load content from a URL"""
        # Placeholder - would implement HTTP requests
        raise NotImplementedError("URL loading not yet implemented")

    def _load_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _load_html(self, file_path: Path) -> str:
        """Extract text from HTML file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            return soup.get_text()

    def _load_xml(self, file_path: Path) -> str:
        """Load XML content"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _parse_document_structure(self, content: str, format_type: str) -> Tuple[List[DocumentSection], List[Dict[str, Any]]]:
        """Parse document structure and create sections with TOC"""
        sections = []
        toc = []

        if format_type == 'pdf':
            sections, toc = self._parse_pdf_structure(content)
        elif format_type == 'html':
            sections, toc = self._parse_html_structure(content)
        elif format_type == 'xml':
            sections, toc = self._parse_xml_structure(content)
        else:
            sections, toc = self._parse_text_structure(content)

        return sections, toc

    def _parse_text_structure(self, content: str) -> Tuple[List[DocumentSection], List[Dict[str, Any]]]:
        """Parse plain text structure using heading patterns"""
        sections = []
        toc = []
        current_pos = 0

        # Split into lines and identify headings
        lines = content.split('\n')
        current_section = None
        section_stack = []

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Check for heading patterns
            heading_match = re.match(r'^(#+\s+)(.+)$', line)
            if heading_match:
                # Save previous section if exists
                if current_section:
                    current_section.end_position = current_pos
                    sections.append(current_section)

                # Create new section
                level = len(heading_match.group(1).strip())
                title = heading_match.group(2).strip()

                # Determine parent
                parent_id = None
                if section_stack and level > section_stack[-1][1]:
                    parent_id = section_stack[-1][0]
                elif section_stack and level <= section_stack[-1][1]:
                    # Pop stack until we find the right parent level
                    while section_stack and section_stack[-1][1] >= level:
                        section_stack.pop()
                    if section_stack:
                        parent_id = section_stack[-1][0]

                section_id = f"section_{len(sections) + 1}"
                current_section = DocumentSection(
                    id=section_id,
                    title=title,
                    content="",
                    level=level,
                    start_position=current_pos,
                    parent_id=parent_id
                )

                # Update parent subsections
                if parent_id:
                    parent_section = next((s for s in sections if s.id == parent_id), None)
                    if parent_section:
                        parent_section.subsections.append(section_id)

                section_stack.append((section_id, level))

                # Add to TOC
                toc.append({
                    'id': section_id,
                    'title': title,
                    'level': level,
                    'parent_id': parent_id
                })
            else:
                # Add content to current section
                if current_section:
                    current_section.content += line + "\n"

            current_pos += len(line) + 1

        # Save final section
        if current_section:
            current_section.end_position = current_pos
            sections.append(current_section)

        return sections, toc

    def _parse_html_structure(self, content: str) -> Tuple[List[DocumentSection], List[Dict[str, Any]]]:
        """Parse HTML structure using heading tags"""
        # Placeholder - would implement HTML parsing
        return self._parse_text_structure(content)  # Fallback to text parsing

    def _parse_pdf_structure(self, content: str) -> Tuple[List[DocumentSection], List[Dict[str, Any]]]:
        """Parse PDF structure using clinical document patterns"""
        sections = []
        toc = []

        # For PDFs, we'll create sections based on numbered recommendations and major headers
        lines = content.split('\n')
        current_section = None
        section_start_pos = 0
        current_pos = 0

        for line in lines:
            line = line.strip()
            if not line:
                current_pos += 1
                continue

            # Look for numbered recommendations (e.g., "9.1", "9.2")
            rec_match = re.match(r'^(\d+\.\d+)\s*(.*)', line)
            if rec_match:
                # Save previous section if exists
                if current_section:
                    current_section.end_position = current_pos
                    sections.append(current_section)

                # Create new recommendation section
                rec_num = rec_match.group(1)
                rec_title = rec_match.group(2).strip() if rec_match.group(2).strip() else f"Recommendation {rec_num}"

                section_id = f"recommendation_{rec_num.replace('.', '_')}"
                current_section = DocumentSection(
                    id=section_id,
                    title=rec_title,
                    content="",
                    level=3,  # Recommendation level
                    start_position=current_pos,
                    parent_id="main_content"
                )

                toc.append({
                    'id': section_id,
                    'title': rec_title,
                    'level': 3,
                    'parent_id': "main_content"
                })

            # Look for major section headers (ALL CAPS, typically clinical sections)
            elif line.isupper() and len(line) > 10 and not line.startswith('http'):
                # Save previous section if exists
                if current_section:
                    current_section.end_position = current_pos
                    sections.append(current_section)

                # Create new major section
                section_id = f"section_{len(sections) + 1}"
                current_section = DocumentSection(
                    id=section_id,
                    title=line,
                    content="",
                    level=2,  # Major section level
                    start_position=current_pos,
                    parent_id="main_content"
                )

                toc.append({
                    'id': section_id,
                    'title': line,
                    'level': 2,
                    'parent_id': "main_content"
                })

            else:
                # Add content to current section
                if current_section:
                    current_section.content += line + "\n"

            current_pos += len(line) + 1

        # Save final section
        if current_section:
            current_section.end_position = current_pos
            sections.append(current_section)

        # If no sections were found, create a single main section
        if not sections:
            sections.append(DocumentSection(
                id="main_content",
                title="Main Content",
                content=content,
                level=1,
                start_position=0,
                end_position=len(content)
            ))
            toc.append({
                'id': "main_content",
                'title': "Main Content",
                'level': 1,
                'parent_id': None
            })

        return sections, toc

    def _parse_xml_structure(self, content: str) -> Tuple[List[DocumentSection], List[Dict[str, Any]]]:
        """Parse XML structure"""
        # Placeholder - would implement XML parsing
        return self._parse_text_structure(content)  # Fallback to text parsing

    def _generate_document_id(self, metadata: Dict[str, Any], content: str) -> str:
        """Generate unique document identifier"""
        # Use title, source, and version to create ID
        id_components = [
            metadata.get('title', 'unknown').lower().replace(' ', '_').replace('/', '_'),
            metadata.get('source', 'unknown').lower().replace('/', '_'),
            metadata.get('version', '1.0').replace('/', '_')
        ]
        base_id = '_'.join(id_components)
        # Add hash of content for uniqueness
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"{base_id}_{content_hash}"

    def _calculate_checksum(self, content: str) -> str:
        """Calculate SHA256 checksum of content"""
        return hashlib.sha256(content.encode()).hexdigest()

    def _store_document(self, doc_id: str, content: str, metadata: DocumentMetadata):
        """Store document content and metadata"""
        doc_dir = self.storage_path / doc_id
        doc_dir.mkdir(exist_ok=True)

        # Store content
        content_path = doc_dir / "content.txt"
        with open(content_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Store metadata
        metadata_path = doc_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(metadata), f, indent=2, ensure_ascii=False)

        # Create anchors directory
        (doc_dir / "anchors").mkdir(exist_ok=True)

        logger.info(f"Stored document {doc_id} in {doc_dir}")

    def _store_anchor(self, anchor: DocumentAnchor):
        """Store anchor reference"""
        doc_id = anchor.metadata['doc_id']
        anchor_dir = self.storage_path / doc_id / "anchors"
        anchor_dir.mkdir(exist_ok=True)

        anchor_path = anchor_dir / f"{anchor.id}.json"
        with open(anchor_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(anchor), f, indent=2, ensure_ascii=False)

    def _load_document_from_storage(self, doc_id: str):
        """Load document metadata from storage"""
        metadata_path = self.storage_path / doc_id / "metadata.json"
        if not metadata_path.exists():
            raise FileNotFoundError(f"Document metadata not found: {metadata_path}")

        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata_dict = json.load(f)

        # Convert back to DocumentMetadata
        metadata = DocumentMetadata(**metadata_dict)
        self.loaded_documents[doc_id] = metadata

    def _get_anchor_context(self, content: str, position: int, context_size: int = 200) -> str:
        """Get context around a position in the content"""
        start = max(0, position - context_size // 2)
        end = min(len(content), position + context_size // 2)
        return content[start:end]

    def list_documents(self) -> List[Dict[str, Any]]:
        """List all loaded documents"""
        documents = []
        for doc_id in self.loaded_documents:
            doc = self.loaded_documents[doc_id]
            documents.append({
                'id': doc.id,
                'title': doc.title,
                'source': doc.source,
                'version': doc.version,
                'sections_count': len(doc.sections),
                'loaded_at': doc.loaded_at
            })
        return documents