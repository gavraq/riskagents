---
name: markdown-to-word
description: Convert markdown documents to professional Word (.docx) format. Use when user asks to convert markdown to Word, export a document to Word, create a Word version of a report, or generate a .docx file from markdown content. Keywords - markdown to word, convert to docx, export word, markdown word, document conversion, word document.
---

# Markdown to Word Converter

Convert markdown documents (.md) to professionally formatted Word (.docx) documents using the `DocxBuilder` utility class.

## When to Use

- User asks to convert a markdown file to Word format
- User asks to export a stress scenario, report, or any document to .docx
- User asks for a Word version of a generated document
- User asks to "create a Word document from..." any markdown content

## How to Convert

Use the `docx_builder.py` module located at `.claude/skills/markdown-to-word/docx_builder.py`.

### Step-by-step process:

1. **Read** the source markdown file
2. **Write and run** a Python conversion script that:
   - Imports `DocxBuilder` from the skill directory
   - Creates a document with `create_document()`
   - Optionally adds a branded cover page with `add_cover_page()`
   - Converts the markdown content with `add_markdown_content()`
   - Adds a footer with `add_footer()`
   - Saves the output with `save()`
3. **Report** the output file path to the user

### Template conversion script:

```python
import sys
sys.path.insert(0, "/Volumes/DockSSD/projects/riskagents/.claude/skills/markdown-to-word")
from docx_builder import DocxBuilder

# Read the source markdown
with open("INPUT_PATH_HERE", "r") as f:
    markdown_content = f.read()

# Extract title from first heading if present
lines = markdown_content.strip().split('\n')
title = "Document"
subtitle = ""
for line in lines:
    if line.startswith('# '):
        title = line[2:].strip()
        break

# Build the Word document
builder = DocxBuilder()
builder.create_document()
builder.add_cover_page(
    title=title,
    subtitle=subtitle,
    prepared_by="Market Risk",
    date=None,  # Uses today's date
)
builder.add_markdown_content(markdown_content)
builder.add_footer()
output_path = builder.save("OUTPUT_PATH_HERE")
print(f"Word document saved to: {output_path}")
```

### Important notes:

- Always use `sys.path.insert` to add the skill directory before importing
- Run with `uv run python script.py` to use the project's virtual environment (python-docx is installed)
- Save output to the `output/` directory by default
- Use the same filename as the input but with `.docx` extension
- The markdown file path will typically be in `output/stress tests/` for stress scenario documents

## DocxBuilder Key Methods

| Method | Purpose |
|--------|---------|
| `create_document()` | Initialize a new Word document |
| `add_cover_page(title, subtitle, ...)` | Add branded cover page |
| `add_markdown_content(text)` | Convert and add markdown text |
| `add_section_heading(title)` | Add H1 heading |
| `add_subsection_heading(title)` | Add H2 heading |
| `add_paragraph(text)` | Add plain paragraph |
| `add_bullet_list(items)` | Add bulleted list |
| `add_key_value_table(data)` | Add two-column table |
| `add_data_table(headers, rows)` | Add multi-column table |
| `add_footer()` | Add branded footer |
| `save(path)` | Save to .docx file |

## Integration

This skill also provides the shared `DocxBuilder` base class used by:
- `pillar-stress-generator` (MLRCDocumentBuilder)
- `climate-scorecard-filler` (ClimateScorecardDocumentBuilder)

## Allowed Tools
- Read (to read input markdown files)
- Bash (to run the Python conversion script)
- Write (to create the conversion script)
