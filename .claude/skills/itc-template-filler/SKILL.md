---
name: itc-template-filler
description: Automatically fills out ITC (Investment Technology Committee) Project Template Excel files. Use this skill when user asks to "complete ITC template", "fill ITC template", "populate ITC project template", or "prepare ITC proposal". Extracts project information from meeting minutes and documents to populate ITC-specific fields.
---

# ITC Template Filler Skill

## Purpose

Automates the population of **ITC (Investment Technology Committee) Project Proposal templates** for the initial project governance gate. This is the first approval step where projects are evaluated for strategic alignment and prioritization. Extracts relevant information from various project documentation sources and maps them to the appropriate ITC template fields across multiple Excel sheets.

**Governance Context**: ITC is the first gate in the project approval process. After ITC approval, projects proceed to ICC (Investment & Change Committee) for detailed business case approval.

## When to Use

**ALWAYS USE THIS SKILL** (do not write custom Python scripts) when:
- User asks to "complete ITC template" or "fill ITC template"
- User mentions "ITC Project Template" or "ITC Project Proposal"
- User wants to prepare an ITC proposal or Investment Technology Committee documentation
- User needs initial project approval documentation
- User asks to "complete the ITC" or "prepare for ITC"

**Keywords that trigger this skill:**
"ITC template", "ITC project template", "ITC proposal", "Investment Technology Committee", "fill ITC", "complete ITC", "prepare ITC"

**Note**: For ICC (Investment & Change Committee) business cases, use the `icc-business-case-filler` skill instead.

## Critical Feature: Merged Cell Handling

**⚠️ IMPORTANT:** ITC templates extensively use merged cells. This skill includes specialized handling to avoid the common `AttributeError: 'MergedCell' object attribute 'value' is read-only` error.

The bundled `excel_helpers.py` module provides `set_cell_value()` which automatically:
- Detects if a cell is part of a merged range
- Finds the top-left "real" cell of the merge
- Sets the value correctly

**Always use the bundled scripts** - they handle this complexity for you.

## What This Skill Provides

### 1. Template Population
Populates the multi-sheet ITC Project Template with:
- **Section 1: Problem Statement**
  - Project name and submission details
  - Business sponsors and functions
  - Background and problem statement
  - Business readiness assessment

- **Section 2: Benefits/Costs/Duration**
  - Benefit theme selection and quantification
  - Business unit beneficiary mapping
  - Cost and duration estimates

- **Scope Elements Sheet**
  - Detailed requirements with BRD status
  - Enhancement vs like-for-like identification
  - Sponsorship and rationale
  - Resource requirements

- **Estimates Sheet**
  - Task breakdown with dependencies
  - Duration and resource estimates
  - Critical path identification

### 2. Intelligent Extraction
- Parses meeting minutes for project context
- Identifies key stakeholders and sponsors
- Extracts decisions, action items, and requirements
- Recognizes benefit themes from discussions
- Maps resources and timeline information

### 3. Gap Analysis
- Identifies fields that couldn't be populated
- Provides confidence scores for extracted data
- Highlights required vs optional missing fields
- Suggests where manual input is needed

## Input Parameters

### Required
- `template_path`: Path to the ITC Project Template Excel file
- `output_path`: Where to save the populated template

### At Least One Source Document Required
- `meeting_minutes`: Text content or path to meeting minutes
- `project_plan`: Text content or path to project plan/scope document
- `business_case`: Text content or path to business case
- `additional_context`: Any other relevant project documentation

### Optional
- `project_name`: Explicitly specify project name (otherwise extracted)
- `submission_date`: Date for template submission
- `preserve_formatting`: Boolean (default: true) - maintain original template formatting

## Field Mapping Strategy

### From Meeting Minutes
**Extract:**
- Project title/name
- Problem statement and background
- Key decisions → Scope elements
- Attendees → Stakeholders and sponsors
- Action items → Tasks and dependencies
- Timeline discussions → Readiness assessment
- Benefit discussions → Benefit themes
- Resource mentions → Resource requirements

**Map to:**
- D4: Project Name
- E11: Background & Problem Statement
- E7: Business Sponsor (from attendees)
- E22-E25: Readiness checkboxes
- Section 2: Benefit themes (E28-E37)
- Business Unit Beneficiary (E40-E44)

### From Project Plan/Scope
**Extract:**
- Requirements list
- Scope items
- Work breakdown structure
- Dependencies
- Resource allocation
- Timeline/milestones

**Map to:**
- Scope Elements sheet (all columns)
- Estimates sheet (tasks B column)
- Dependencies (C column)
- Duration estimates (D column)
- Resource owners (G column)

### From Business Case
**Extract:**
- Quantifiable benefits (revenue, cost savings)
- FTE impacts
- Regulatory/compliance drivers
- Capital/liquidity impacts
- Capability improvements

**Map to:**
- Benefit theme values (H28-H37)
- Business unit impact descriptions (G40-G44)
- Cost justifications

## Output Format

### Populated Excel Template
```
ITC_Project_Template_[ProjectName]_[Date].xlsx

Sheets:
1. ITC Project Proposal (all sections populated)
2. Scope Elements (requirements mapped)
3. Estimates (tasks and timeline)
4. Sheet2 (reference data preserved)
```

### Gap Analysis Report
```markdown
# Template Population Report
## Project: [Name]
## Generated: [Date/Time]

### Population Summary
- Total Fields: X
- Populated: Y (Z%)
- Missing: N (M%)
- Confidence: [Overall score]

### Section 1: Problem Statement
✅ Project Name: [Extracted value] (Confidence: 95%)
✅ Business Sponsor: [Extracted value] (Confidence: 85%)
❌ IT ExCo Sponsor: NOT FOUND - Manual input required
...

### Section 2: Benefits
✅ Regulatory (E31): Marked
⚠️  Regulatory Benefit (H31): Partial - "Compliance improvement" (Low confidence)
❌ Revenue Protection (E36): Not mentioned in source documents
...

### Scope Elements
✅ R01: Full revaluation - Mapped from meeting minutes decision
✅ R02: Decommissioning - Mapped from action items
⚠️  R03: Partial information - Resources unclear
...

### Estimates
✅ 15 tasks extracted from project plan
⚠️  5 tasks missing duration estimates
❌ Critical path dependencies need validation
...

### Recommendations
1. **High Priority - Manual Review Required:**
   - IT ExCo Sponsor (E8)
   - Quantified revenue benefits (H28, H36)
   - Start/finish dates for 12 tasks

2. **Medium Priority - Validate Extracted Data:**
   - Business unit beneficiary descriptions
   - Resource allocation names
   - Dependency relationships

3. **Low Priority - Optional Fields:**
   - Additional benefit themes
   - Detailed task notes
```

## Processing Logic

This skill includes executable Python modules that handle the technical complexity of Excel manipulation and multi-source extraction.

### Available Scripts

This skill bundles three Python modules you should reference when implementing template population:

#### 1. excel_helpers.py
Provides safe Excel manipulation functions that handle merged cells (a critical requirement for ITC templates):

```python
from excel_helpers import set_cell_value, validate_template, inspect_template_structure

# Always use set_cell_value() instead of direct assignment
# This handles merged cells automatically
set_cell_value(proposal_sheet, 'E11', problem_statement)  # Works even if E11 is merged

# Inspect template before populating
success, workbook, error = validate_template(template_path)
structure = inspect_template_structure(workbook)
```

**Key functions:**
- `set_cell_value(sheet, cell_ref, value)` - Handles merged cells
- `validate_template(path)` - Check template is loadable
- `inspect_template_structure(workbook)` - Discover merged cells, formulas

#### 2. extraction_helpers.py
Multi-source data extraction with confidence scoring:

```python
from extraction_helpers import (
    inventory_source_documents,
    extract_field_with_confidence,
    generate_extraction_report
)

# Read and categorize sources
sources = inventory_source_documents([
    'meeting_minutes.md',
    'project_plan.md',
    'business_case.md'
])

# Extract fields with confidence
value, confidence, source = extract_field_with_confidence('project_name', sources)

# Generate extraction provenance report
report = generate_extraction_report(extracted_fields)
```

**Key functions:**
- `inventory_source_documents(paths)` - Read and classify documents
- `extract_field_with_confidence(field, sources)` - Extract with confidence score
- `generate_extraction_report(fields)` - Document provenance

#### 3. populate_template.py
Main template population engine with command-line interface:

```python
from populate_template import populate_itc_template

result = populate_itc_template(
    template_path='template.xlsx',
    output_path='output.xlsx',
    project_data={
        'project_name': 'Energy VaR Migration',
        'business_sponsor': 'Philip / Richard',
        'problem_statement': '...',
        'benefits': {...},
        # ... etc
    }
)

print(f"Success: {result['success']}")
print(f"Populated {result['populated_fields']} fields")
```

### Implementation Workflow

When you need to populate a template, follow this workflow:

**Step 1: Read Source Documents**
```python
# Use Read tool to get content
meeting_content = Read('path/to/meeting_minutes.md')
project_content = Read('path/to/project_plan.md')

# Or use extraction_helpers
from extraction_helpers import inventory_source_documents
sources = inventory_source_documents([meeting_path, project_path])
```

**Step 2: Extract Project Data**

Use extraction helpers or manual parsing to build the `project_data` dictionary:

```python
project_data = {
    # Section 1 fields
    'project_name': '...',
    'business_sponsor': '...',
    'it_exco_sponsor': '...',
    'functional_area': '...',
    'business_unit': '...',
    'problem_statement': '...',

    # Key drivers
    'key_drivers': ['system_simplification', 'regulatory'],

    # Business readiness
    'business_readiness': {
        'requirements_understood': True,
        'business_case_developed': True
    },

    # Benefits
    'benefits': {
        'cost_reduction': {
            'checkbox': 'E30',
            'description': 'H30',
            'text': '...'
        },
        'regulatory': {
            'checkbox': 'E31',
            'description': 'H31',
            'text': '...'
        }
    },

    # Costs and timeline
    'cost_estimate': '£1M - £5M',
    'cost_breakdown': '...',
    'duration': '12-18 months',
    'timeline': '...',

    # Scope elements (optional)
    'scope_elements': [
        {
            'description': '...',
            'understood': 'Yes',
            'enhancement': 'Like-for-like',
            'sponsorship': '...',
            'rationale': '...',
            'resources': '...'
        }
    ],

    # Tasks (optional)
    'tasks': [
        {
            'task': '...',
            'dependency': '...',
            'duration': '...',
            'owner': '...'
        }
    ]
}
```

**Step 3: Populate Template**

Use the populate_template module to safely populate the template:

```python
from populate_template import populate_itc_template

result = populate_itc_template(
    template_path=template_path,
    output_path=output_path,
    project_data=project_data,
    verbose=True  # Show progress
)

if result['success']:
    print(f"✓ Populated {result['populated_fields']} fields")
else:
    print(f"✗ Error: {result['message']}")
```

**Step 4: Generate Gap Analysis**

Document what was populated and what's missing:

```python
# If using extraction_helpers
from extraction_helpers import generate_extraction_report
report = generate_extraction_report(extracted_fields)

# Write gap analysis
Write(report_path, report)
```

### Command-Line Usage (Alternative)

The populate_template.py script can also run standalone:

```bash
# Inspect template structure
python populate_template.py --template template.xlsx --inspect

# Populate from JSON data file
python populate_template.py \
  --template template.xlsx \
  --output output.xlsx \
  --data project_data.json
```

## Extraction Patterns

### Project Name
- Look for: "Project:", "Initiative:", meeting title with "Project"
- Pattern: `r"(?:Project|Initiative):\s*(.+?)(?:\n|$)"`
- Confidence: High if in meeting title, Medium if in content

### Business Sponsor
- Look for: "Sponsor:", "Business Sponsor:", attendee list with "Sponsor" title
- Pattern: Check attendees for role indicators
- Confidence: High if explicit, Low if inferred from seniority

### Problem Statement
- Look for: "Background", "Problem", "Challenge", "Current State"
- Extract: Full paragraph/section under these headings
- Confidence: Medium - always needs review for completeness

### Requirements
- Look for: "R##", "Requirement", numbered lists in decisions
- Pattern: `r"R\d+[.:]?\s*(.+?)(?=R\d+|$)"`
- Map to scope elements

### Benefits
- Look for: Keywords like "saves", "reduces", "improves", "generates"
- Quantifiable: Extract numbers with currency/FTE mentions
- Qualitative: Extract benefit descriptions

### Timeline
- Look for: "immediately", "6 months", "Q1", date patterns
- Map to readiness checkboxes (E22-E25)
- Extract milestone dates for estimates sheet

## Error Handling

### Missing Template
```
Error: Template file not found at [path]
Solution: Verify template_path parameter is correct
```

### No Source Documents
```
Error: At least one source document required
Solution: Provide meeting_minutes, project_plan, or business_case
```

### Extraction Failures
```
Warning: Could not extract [field_name]
Action: Mark as gap in report, continue processing
```

### Excel Corruption
```
Error: Could not modify template - file may be corrupted
Solution: Validate template integrity, use backup
```

## Examples

### Example 1: From Meeting Minutes Only
```python
Input:
- meeting_minutes: "Energy VaR Project meeting transcript..."
- template_path: "templates/ITC_Template.xlsx"
- output_path: "outputs/Energy_VaR_ITC_Proposal.xlsx"

Output:
- Populated template with Section 1 complete
- Partial Section 2 (benefit themes identified but not quantified)
- Gap analysis showing missing cost estimates
- Confidence: 65% (good problem statement, missing detailed scope)
```

### Example 2: Full Documentation Set
```python
Input:
- meeting_minutes: "Project kickoff notes..."
- project_plan: "Detailed scope and work breakdown..."
- business_case: "Financial justification document..."
- template_path: "templates/ITC_Template.xlsx"
- output_path: "outputs/Full_Project_ITC_Proposal.xlsx"

Output:
- Fully populated template across all sheets
- High confidence scores (85%+) for most sections
- Minimal gaps (only optional fields)
- Ready for governance review with minor manual validation
```

### Example 3: Gap Analysis Focus
```python
Input:
- meeting_minutes: "Brief discussion notes..."
- template_path: "templates/ITC_Template.xlsx"
- output_path: "outputs/Draft_ITC_Proposal.xlsx"

Output:
- Partially populated template
- Extensive gap analysis with 45% missing fields
- Clear prioritization of what needs manual completion
- Template serves as starting point for further data gathering
```

## Banking Domain Intelligence

### Regulatory Benefits Recognition
- IFRS 9, Basel III/IV compliance
- SR 11-7 (Model Risk Management)
- CRR/CRD requirements
- PRA/FCA regulatory changes

### Risk Management Context
- VaR (Value at Risk) calculations
- Model validation requirements
- Three lines of defense
- ICAAP/ILAAP processes

### Technology Systems
- Murex, QP, Vespa, FMDM, RightAngle
- Front office vs middle office vs back office
- Data platforms and time series management

### Benefit Themes Mapping
- **Revenue generation**: New product capabilities, faster time-to-market
- **Cost reduction**: Decommissioning, efficiency, automation
- **Regulatory**: Compliance, audit readiness, regulatory reporting
- **Capital**: RWA reduction, capital efficiency
- **Control**: Operational risk, data quality, reconciliation
- **Capability**: Platform modernization, scalability

## Quality Assurance

### Pre-Population Checks
- ✅ Template file exists and is readable
- ✅ Template structure matches expected format
- ✅ At least one source document provided
- ✅ Output path is writable

### Post-Population Validation
- ✅ No formulas corrupted
- ✅ Data validation rules preserved
- ✅ Formatting maintained
- ✅ No cells overwritten with invalid data
- ✅ All sheets present and intact

### Confidence Scoring
- **High (85-100%)**: Direct extraction, exact matches
- **Medium (60-84%)**: Inferred, contextual matches
- **Low (40-59%)**: Weak signals, ambiguous
- **None (<40%)**: No data found, field left blank

## Integration with Other Skills

This skill works well with:
- **meeting-minutes**: First structure the meeting notes, then use output for template population
- **project-planner**: Generate project plan first, then populate template
- **status-reporter**: Ongoing projects can have templates updated periodically

## Limitations

1. **Complex Benefit Quantification**: Financial calculations may need manual validation
2. **Multi-Project Dependencies**: Dependencies across projects not automatically identified
3. **Resource Allocation**: People assignment needs HR system integration (future)
4. **Template Versioning**: Assumes current template structure, needs update if template changes
5. **Language**: Currently optimized for English documentation

## Future Enhancements

- Historical project data learning (improve extraction patterns)
- Integration with project management tools (JIRA, MS Project)
- Automated benefit tracking and validation
- Multi-template support (different governance bodies)
- Real-time collaboration (track who populated which fields)
- Approval workflow integration

---

**Last Updated**: 2025-01-05
**Version**: 1.0
**Supports Template**: ITC Project Proposal Template (2025 version)
