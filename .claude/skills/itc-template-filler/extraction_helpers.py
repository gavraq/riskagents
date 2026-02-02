#!/usr/bin/env python3
"""
Multi-Source Data Extraction Helpers
Utilities for extracting and synthesizing project data from multiple sources
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional


# Field-to-source mapping configuration
FIELD_SOURCE_MAP = {
    'project_name': {
        'primary': 'meeting_minutes',
        'pattern': r'(?:Project|Initiative):\s*(.+?)(?:\n|$)',
        'confidence_threshold': 0.8
    },
    'business_sponsor': {
        'primary': 'meeting_minutes',
        'fallback': 'business_case',
        'pattern': r'(?:Business Sponsor|Sponsor):\s*(.+?)(?:\n|$)',
        'confidence_threshold': 0.9
    },
    'problem_statement': {
        'primary': 'business_case',
        'fallback': 'meeting_minutes',
        'sections': ['Background', 'Problem Statement', 'Current State'],
        'confidence_threshold': 0.7
    },
    'technical_requirements': {
        'primary': 'technical_spec',
        'fallback': 'meeting_minutes',
        'pattern': r'R\d+[.:]?\s*(.+?)(?=R\d+|$)',
        'confidence_threshold': 0.85
    },
    'costs': {
        'primary': 'business_case',
        'fallback': 'meeting_minutes',
        'pattern': r'[£$€][\d,]+[KMkm]?',
        'confidence_threshold': 0.6
    }
}


def classify_document(content: str) -> str:
    """
    Classify document type based on content heuristics.

    Args:
        content: Document text content

    Returns:
        str: Document type (meeting_minutes, technical_spec, business_case, unknown)
    """
    first_500 = content[:500]

    if 'Meeting Minutes' in first_500 or 'Attendees:' in first_500:
        return 'meeting_minutes'
    elif 'Technical Specification' in first_500 or 'Requirements:' in first_500:
        return 'technical_spec'
    elif 'Business Case' in first_500 or 'Financial Justification' in first_500:
        return 'business_case'
    else:
        return 'unknown'


def extract_date(content: str) -> Optional[str]:
    """
    Extract date from document content.

    Args:
        content: Document text

    Returns:
        str or None: Extracted date
    """
    # Try various date patterns
    patterns = [
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
        r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',  # DD Month YYYY
    ]

    for pattern in patterns:
        match = re.search(pattern, content[:1000])  # Search first 1000 chars
        if match:
            return match.group(0)

    return None


def extract_attendees(content: str) -> List[str]:
    """
    Extract attendee list from meeting minutes.

    Args:
        content: Document text

    Returns:
        list: Attendee names
    """
    attendees = []

    # Look for attendees section
    attendees_match = re.search(r'Attendees?:(.*?)(?:\n\n|$)', content, re.DOTALL | re.IGNORECASE)
    if attendees_match:
        attendees_text = attendees_match.group(1)
        # Extract names (bullet points or comma-separated)
        if '-' in attendees_text or '*' in attendees_text:
            attendees = re.findall(r'[-*]\s*(.+?)(?:\n|$)', attendees_text)
        else:
            attendees = [name.strip() for name in attendees_text.split(',')]

    return [a.strip() for a in attendees if a.strip()]


def inventory_source_documents(doc_paths: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Read and categorize source documents.

    Args:
        doc_paths: List of paths to source documents

    Returns:
        dict: Document metadata and content
    """
    sources = {}

    for path in doc_paths:
        path_obj = Path(path)
        if not path_obj.exists():
            continue

        # Read document
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Categorize by type
        doc_type = classify_document(content)

        sources[str(path)] = {
            'type': doc_type,
            'content': content,
            'length': len(content),
            'date': extract_date(content),
            'attendees': extract_attendees(content) if doc_type == 'meeting_minutes' else []
        }

    return sources


def extract_section(content: str, section_header: str) -> Optional[str]:
    """
    Extract content under a specific section header.

    Args:
        content: Document text
        section_header: Header to find (e.g., "Background", "Problem Statement")

    Returns:
        str or None: Section content
    """
    # Try to find section with various header formats
    patterns = [
        rf'#{1,3}\s*{re.escape(section_header)}(.*?)(?=#{1,3}\s|\Z)',  # Markdown headers
        rf'{re.escape(section_header)}:?(.*?)(?=\n\n[A-Z]|\Z)',  # Plain text with colon
        rf'\*\*{re.escape(section_header)}\*\*(.*?)(?=\*\*|\Z)',  # Bold markdown
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None


def extract_with_pattern(content: str, pattern: Optional[str] = None, sections: Optional[List[str]] = None) -> Tuple[Optional[str], float]:
    """
    Extract value using regex pattern or section headers.

    Args:
        content: Document text
        pattern: Regex pattern (optional)
        sections: List of section headers to try (optional)

    Returns:
        tuple: (extracted_value or None, confidence_score)
    """
    if pattern:
        # Regex extraction
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            value = match.group(1).strip() if match.lastindex and match.lastindex >= 1 else match.group(0).strip()
            # Confidence based on match quality
            confidence = 0.9 if len(value) > 10 else 0.6
            return value, confidence

    if sections:
        # Section-based extraction
        for section in sections:
            section_content = extract_section(content, section)
            if section_content:
                confidence = 0.8 if len(section_content) > 50 else 0.5
                return section_content, confidence

    return None, 0.0


def find_document_by_type(sources: Dict[str, Dict], doc_type: str) -> Optional[Dict]:
    """
    Find first document matching specified type.

    Args:
        sources: Source documents dict
        doc_type: Type to find

    Returns:
        dict or None: Document info
    """
    for path, doc_info in sources.items():
        if doc_info['type'] == doc_type:
            return {**doc_info, 'path': path}
    return None


def extract_field_with_confidence(field_name: str, sources: Dict, field_map: Dict = FIELD_SOURCE_MAP) -> Tuple[Optional[str], float, Optional[str]]:
    """
    Extract field from best source with confidence score.

    Args:
        field_name: Field to extract
        sources: Source documents
        field_map: Field-to-source mapping configuration

    Returns:
        tuple: (value or None, confidence_score, source_path or None)
    """
    if field_name not in field_map:
        return None, 0.0, None

    field_spec = field_map[field_name]

    # Try primary source first
    primary_doc = find_document_by_type(sources, field_spec['primary'])
    if primary_doc:
        value, confidence = extract_with_pattern(
            primary_doc['content'],
            field_spec.get('pattern'),
            field_spec.get('sections')
        )

        if confidence >= field_spec['confidence_threshold']:
            return value, confidence, primary_doc['path']

    # Try fallback source
    if 'fallback' in field_spec:
        fallback_doc = find_document_by_type(sources, field_spec['fallback'])
        if fallback_doc:
            value, confidence = extract_with_pattern(
                fallback_doc['content'],
                field_spec.get('pattern'),
                field_spec.get('sections')
            )
            # Penalize fallback source
            return value, confidence * 0.8, fallback_doc['path']

    # No good match found
    return None, 0.0, None


def resolve_conflicts(field_name: str, extractions: List[Tuple]) -> Tuple:
    """
    Resolve conflicts when multiple sources provide different values.

    Args:
        field_name: Field name
        extractions: List of (value, confidence, source) tuples

    Returns:
        tuple: Best value with justification (value, confidence, source, notes)
    """
    if len(extractions) == 0:
        return None, 0.0, None, "No data found"

    if len(extractions) == 1:
        return (*extractions[0], None)

    # Sort by confidence
    sorted_extractions = sorted(extractions, key=lambda x: x[1], reverse=True)

    best = sorted_extractions[0]
    second_best = sorted_extractions[1] if len(sorted_extractions) > 1 else None

    # If top two are very close in confidence, flag for manual review
    if second_best and abs(best[1] - second_best[1]) < 0.1:
        notes = f"CONFLICT: {second_best[2]} has similar value '{second_best[0][:50]}...'"
        return (
            best[0],
            best[1] * 0.7,  # Reduce confidence due to conflict
            best[2],
            notes
        )

    return (*best, None)


def generate_extraction_report(extracted_fields: Dict[str, Tuple]) -> str:
    """
    Document what was extracted from where with confidence.

    Args:
        extracted_fields: Dict of field_name -> (value, confidence, source, notes)

    Returns:
        str: Markdown report
    """
    report = "# Data Extraction Report\n\n"
    report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    high_conf = []
    medium_conf = []
    low_conf = []
    missing = []

    for field_name, (value, confidence, source, notes) in extracted_fields.items():
        if confidence >= 0.8:
            high_conf.append((field_name, value, confidence, source, notes))
        elif confidence >= 0.6:
            medium_conf.append((field_name, value, confidence, source, notes))
        elif confidence > 0:
            low_conf.append((field_name, value, confidence, source, notes))
        else:
            missing.append(field_name)

    # High confidence fields
    if high_conf:
        report += "## ✅ High Confidence Fields\n\n"
        for field_name, value, confidence, source, notes in high_conf:
            report += f"### {field_name}\n"
            report += f"- **Value**: {str(value)[:200]}{'...' if len(str(value)) > 200 else ''}\n"
            report += f"- **Confidence**: {confidence:.0%}\n"
            report += f"- **Source**: {source}\n"
            if notes:
                report += f"- **Notes**: {notes}\n"
            report += "\n"

    # Medium confidence fields
    if medium_conf:
        report += "## ⚠️  Medium Confidence Fields (Review Recommended)\n\n"
        for field_name, value, confidence, source, notes in medium_conf:
            report += f"### {field_name}\n"
            report += f"- **Value**: {str(value)[:200]}{'...' if len(str(value)) > 200 else ''}\n"
            report += f"- **Confidence**: {confidence:.0%}\n"
            report += f"- **Source**: {source}\n"
            if notes:
                report += f"- **Notes**: {notes}\n"
            report += "\n"

    # Low confidence fields
    if low_conf:
        report += "## ❌ Low Confidence Fields (Manual Review Required)\n\n"
        for field_name, value, confidence, source, notes in low_conf:
            report += f"### {field_name}\n"
            report += f"- **Value**: {str(value)[:200]}{'...' if len(str(value)) > 200 else ''}\n"
            report += f"- **Confidence**: {confidence:.0%}\n"
            report += f"- **Source**: {source}\n"
            if notes:
                report += f"- **Notes**: {notes}\n"
            report += "\n"

    # Missing fields
    if missing:
        report += "## 🔴 Missing Fields\n\n"
        for field_name in missing:
            report += f"- **{field_name}**: No data found in source documents\n"
        report += "\n"

    return report
