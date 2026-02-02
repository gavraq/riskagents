# ITC Template Filler - Complete Reference

**Skill Name**: `itc-template-filler`
**Purpose**: Automate population of ITC (Investment Technology Committee) project governance templates
**Status**: Production Ready (v1.1)
**Last Updated**: 2025-01-08

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Template Structure](#template-structure)
3. [How It Works](#how-it-works)
4. [Bundled Modules](#bundled-modules)
5. [Data Extraction Strategy](#data-extraction-strategy)
6. [Real-World Example](#real-world-example)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Using the Skill

```
Complete the ITC template for the Energy VaR project using the meeting minutes
from meetings/energy_var_meeting.md and the template at templates/ITC_Template.xlsx
```

The skill will:
1. ✅ Extract project information from meeting minutes
2. ✅ Populate the Excel template (handling merged cells safely)
3. ✅ Generate gap analysis report
4. ✅ Provide confidence scores for all extractions

### What You Get

**Output Files**:
- `ITC_ProjectName_Proposal.xlsx` - Populated template
- `ITC_ProjectName_Report.md` - Gap analysis with confidence scores

**Typical Results**:
- 80-95% template completion (depending on source document quality)
- Clear identification of missing fields requiring manual input
- Source attribution for audit trail

---

## Template Structure

The ITC Project Template contains **4 sheets** with **~350 total fields**:

### Sheet 1: ITC Project Proposal (Main)

#### Section 1: Problem Statement
| Cell | Field | Type | Notes |
|------|-------|------|-------|
| D4 | Project Name | Text | |
| E5 | Submission Date | Date | Auto-generated if not provided |
| E7 | Business Sponsor | Text | |
| E8 | IT ExCo Sponsor | Text | Often TBC initially |
| E9 | Functional Area | Text | E.g., "Market Risk / Front Office" |
| E10 | Business Unit | Text | E.g., "Commodities - Energy Trading" |
| E11 | Background & Problem Statement | Multi-line | **MERGED CELL** (E11:E21) |
| E13-E17 | Key Drivers | Checkboxes | System Simplification, Decommissioning, Regulatory |
| E18 | Regulatory Description | Text | If E17 checked |
| E20 | Strategic Importance | Text | |
| E22-E25 | Business Readiness | Checkboxes | Requirements, business case, resources, funding |

#### Section 2: Benefits/Costs/Duration
| Cell | Field | Type | Notes |
|------|-------|------|-------|
| E28-E37 | Benefit Themes | Checkboxes | Revenue, Cost, Regulatory, Capital, Control, Capability |
| H28-H37 | Benefit Descriptions | Text | Quantified benefits for checked themes |
| E40-E44 | Business Unit Beneficiaries | Checkboxes | Front Office, Middle Office, Risk, Technology, Other |
| G40-G44 | Beneficiary Impact | Text | How each unit benefits |
| E46 | Cost Estimate | Currency | Overall project cost |
| E47 | Cost Breakdown | Multi-line | **MERGED CELL** (E47:G47) |
| E48 | Duration | Text | E.g., "12-18 months" |
| E49 | Timeline | Multi-line | **MERGED CELL** - Phased delivery plan |

### Sheet 2: Scope Elements

Requirements breakdown (starting row 4):

| Column | Field | Notes |
|--------|-------|-------|
| A | Requirement Description | Full text |
| B | Scope Understood | "Yes" / "Partial" / "No" |
| C | Enhancement vs Like-for-like | Classification |
| E | Sponsorship | Business unit/person |
| F | Rationale | Why this requirement |
| H | Resource Requirements | Teams/people needed |

### Sheet 3: Estimates

Task-level breakdown (starting row 4):

| Column | Field | Notes |
|--------|-------|-------|
| B | Task Description | What needs to be done |
| C | Dependencies | What must complete first |
| D | Duration Estimate | E.g., "6 weeks" |
| G | Resource Owner | Team/person responsible |

### Sheet 4: Sheet2

Reference data (typically left unchanged)

### Critical: Merged Cells

**Many cells are merged** - attempting direct assignment causes errors:
```python
# FAILS with MergedCell error:
proposal_sheet['E11'] = "Long text..."

# WORKS - uses bundled helper:
from excel_helpers import set_cell_value
set_cell_value(proposal_sheet, 'E11', "Long text...")
```

The skill handles this automatically.

---

## How It Works

### Workflow

```
1. Read Source Documents
   ├── Meeting minutes
   ├── Project plans
   ├── Business cases
   └── Technical specs
        ↓
2. Classify & Inventory
   ├── Detect document type
   ├── Extract metadata (date, attendees)
   └── Categorize content
        ↓
3. Extract Fields
   ├── Use primary source (highest confidence)
   ├── Fallback to secondary source if needed
   ├── Score confidence (0-1.0)
   └── Track provenance (which source?)
        ↓
4. Resolve Conflicts
   ├── Multiple sources disagree?
   ├── Choose highest confidence
   └── Flag for manual review if close
        ↓
5. Populate Template
   ├── Load Excel template
   ├── Validate structure
   ├── Populate using safe cell manipulation
   └── Preserve formulas and formatting
        ↓
6. Generate Gap Analysis
   ├── Identify missing fields
   ├── Classify by priority (High/Medium/Low)
   ├── Calculate overall confidence
   └── Suggest next actions
```

### Confidence Scoring

| Score | Meaning | Example |
|-------|---------|---------|
| 90-100% | Direct extraction, exact match | "Project: Energy VaR Migration" → project_name |
| 75-89% | Strong inference | Sponsor inferred from meeting chair |
| 60-74% | Moderate confidence | Cost estimated from discussion |
| 40-59% | Weak signal | Timeline inferred from vague "Q1" mention |
| 0-39% | No data / placeholder | Field left blank or "TBC" |

---

## Bundled Modules

The skill includes 3 Python modules located in `.claude/skills/itc-template-filler/`:

### 1. excel_helpers.py

**Purpose**: Safe Excel manipulation with merged cell handling

**Key Functions**:

```python
def set_cell_value(sheet, cell_ref, value):
    """Handles merged cells automatically"""

def get_merged_cell_value(sheet, cell_ref):
    """Read from merged or regular cells"""

def validate_template(template_path):
    """Returns (success, workbook, error)"""

def inspect_template_structure(workbook):
    """Discover merged cells, formulas, validation rules"""
```

**Usage**:
```python
from excel_helpers import set_cell_value, validate_template

# Validate first
success, workbook, error = validate_template(template_path)
if not success:
    print(f"Error: {error}")

# Populate safely
proposal_sheet = workbook['ITC Project Proposal']
set_cell_value(proposal_sheet, 'E11', problem_statement)  # Works for merged cells
set_cell_value(proposal_sheet, 'D4', project_name)        # Works for regular cells
```

### 2. extraction_helpers.py

**Purpose**: Multi-source data extraction with confidence scoring

**Key Functions**:

```python
def inventory_source_documents(doc_paths):
    """Read and categorize source documents"""

def classify_document(content):
    """Returns 'meeting_minutes', 'technical_spec', 'business_case', or 'unknown'"""

def extract_field_with_confidence(field_name, sources, field_map=FIELD_SOURCE_MAP):
    """Returns (value, confidence, source_path)"""

def resolve_conflicts(field_name, extractions):
    """Handle disagreements between sources"""

def generate_extraction_report(extracted_fields):
    """Returns markdown report with confidence scores"""
```

**Usage**:
```python
from extraction_helpers import (
    inventory_source_documents,
    extract_field_with_confidence,
    generate_extraction_report
)

# Read sources
sources = inventory_source_documents([
    'meetings/kickoff.md',
    'specs/project_plan.md',
    'business/business_case.md'
])

# Extract fields
extracted_fields = {}
for field in ['project_name', 'business_sponsor', 'problem_statement']:
    value, confidence, source = extract_field_with_confidence(field, sources)
    if value:
        extracted_fields[field] = (value, confidence, source, None)

# Generate report
report = generate_extraction_report(extracted_fields)
```

### 3. populate_template.py

**Purpose**: Main template population engine

**Key Function**:

```python
def populate_itc_template(template_path, output_path, project_data, verbose=True):
    """
    Returns: {
        'success': bool,
        'message': str,
        'populated_fields': int
    }
    """
```

**Usage as Library**:
```python
from populate_template import populate_itc_template

project_data = {
    'project_name': 'Energy VaR Migration',
    'business_sponsor': 'Philip / Richard',
    'problem_statement': '...',
    'benefits': {
        'cost_reduction': {
            'checkbox': 'E30',
            'description': 'H30',
            'text': 'Vespa decommissioning saves £200-300K annually'
        }
    },
    # ... etc
}

result = populate_itc_template(
    template_path='templates/ITC_Template.xlsx',
    output_path='outputs/Energy_VaR_Proposal.xlsx',
    project_data=project_data
)

if result['success']:
    print(f"✓ Populated {result['populated_fields']} fields")
else:
    print(f"✗ Error: {result['message']}")
```

**Usage as CLI**:
```bash
# Inspect template structure
python populate_template.py --template template.xlsx --inspect

# Populate from JSON file
python populate_template.py \
  --template templates/ITC_Template.xlsx \
  --output outputs/MyProject_ITC.xlsx \
  --data project_data.json
```

---

## Data Extraction Strategy

### From Meeting Minutes

**Extract**:
- Project name (from title or "Project:" lines)
- Problem statement (from "Background", "Problem", "Current State" sections)
- Sponsors (from attendees with "Sponsor" in title or role)
- Decisions → Map to scope elements
- Action items → Map to tasks
- Timeline discussions → Business readiness assessment
- Benefit mentions → Benefit themes

**Patterns**:
```python
# Project name
r'(?:Project|Initiative):\s*(.+?)(?:\n|$)'

# Business sponsor
r'(?:Business Sponsor|Sponsor):\s*(.+?)(?:\n|$)'

# Costs
r'[£$€][\d,]+[KMkm]?'
```

### From Project Plan / Scope

**Extract**:
- Requirements (R01, R02, etc.)
- Work breakdown structure
- Dependencies between tasks
- Resource allocation
- Timeline / milestones

### From Business Case

**Extract**:
- Quantified benefits (revenue, cost savings)
- FTE impacts
- Regulatory / compliance drivers
- Capital / liquidity impacts
- Strategic rationale

### Source Priority

Default field-to-source mapping (configurable in `extraction_helpers.py`):

| Field | Primary Source | Fallback Source | Confidence Threshold |
|-------|----------------|-----------------|----------------------|
| project_name | meeting_minutes | - | 0.8 |
| business_sponsor | meeting_minutes | business_case | 0.9 |
| problem_statement | business_case | meeting_minutes | 0.7 |
| technical_requirements | technical_spec | meeting_minutes | 0.85 |
| costs | business_case | meeting_minutes | 0.6 |

---

## Real-World Example

### Energy VaR Migration Project

**Context**: Migrate Energy VaR calculations from Vespa to Murex/FMDM platform

**Inputs**:
- Meeting minutes (Oct 20, 2025) - Strategic planning
- Meeting minutes (Nov 3, 2025) - Technical details
- ITC Project Template.xlsx (with merged cells, formulas, validation)

**Process**:
```
User: "Complete the ITC template for Energy VaR using the meeting minutes"

Agent: Invokes itc-template-filler skill
  ↓
Skill: Reads 2 meeting minutes files
  ↓
Skill: Extracts project data:
  - Project name: "Energy VaR Migration to Murex/FMDM" (95% confidence)
  - Sponsors: "Philip (Front Office) / Richard (Risk)" (95% confidence)
  - Problem statement: Synthesized from both meetings (90% confidence)
  - 4 project components identified
  - 10 requirements extracted
  - 17 tasks mapped
  ↓
Skill: Populates template using excel_helpers
  - 143 cells populated across 4 sections
  - All merged cells handled correctly
  ↓
Skill: Generates gap analysis report
  - 90% complete
  - 10% needs sponsor validation (IT ExCo Sponsor, detailed costs)
  - Recommendations for next steps
```

**Results**:
- ✅ **143 cells populated** across 4 sections
- ✅ **90% template completion**
- ✅ **85% average confidence score**
- ✅ **Gap analysis report** (22KB, detailed)
- ✅ **First-run success** (no manual debugging)

**Time Savings**:
- Before: 4+ hours (manual entry + debugging merged cell errors)
- After: 30 minutes (skill execution + review)
- **8x faster**

### Gap Analysis Report Sample

```markdown
# ITC Template Population Report
## Project: Energy VaR Migration to Murex/FMDM
## Generated: 2025-11-03

### Population Summary
- Total Fields: 143
- Populated: 128 (90%)
- Missing: 15 (10%)
- Overall Confidence: 85%

### Section 1: Problem Statement - ✓ COMPLETE (95% confidence)
✅ Project Name (D4): "Energy VaR Migration to Murex/FMDM" (95%)
  Source: Meeting minutes (Oct 20)

✅ Business Sponsor (E7): "Philip (FO) / Richard (Risk)" (95%)
  Source: Meeting attendees + discussion

⚠️  IT ExCo Sponsor (E8): "TBC" - Manual input required
  Reason: Mentioned but not specified in minutes

✅ Problem Statement (E11): Comprehensive background extracted (90%)
  Sources: Both meetings synthesized

### Section 2: Benefits - ✓ MOSTLY COMPLETE (85% confidence)
✅ Cost Reduction (E30): Checked
✅ Cost Description (H30): "Vespa decommissioning, £200-300K annual savings" (80%)
  Source: Oct 20 meeting discussion

✅ Regulatory (E31): Checked
✅ Regulatory Description (H31): "PRA methodology validation consistency" (90%)
  Source: Nov 3 meeting technical details

### Fields Requiring Manual Input
HIGH PRIORITY:
1. IT ExCo Sponsor (E8) - Governance requirement
2. Detailed vendor quotes (H46) - Cost validation
3. Specific go-live dates (Estimates sheet) - Timeline confirmation

MEDIUM PRIORITY:
4. Quantified revenue benefits (if applicable)
5. Resource names (currently team names)
6. Risk register details

### Recommendations
1. ✓ Review with sponsors (Philip/Richard) for accuracy
2. ✓ Confirm IT ExCo sponsor with governance team
3. ✓ Validate cost estimates with IT portfolio office
4. ✓ Add specific dates to task timeline
5. → Ready for ITC submission after review
```

---

## Troubleshooting

### Common Issues

#### 1. MergedCell Error

**Symptom**:
```
AttributeError: 'MergedCell' object attribute 'value' is read-only
```

**Cause**: Direct assignment to merged cell

**Solution**: The skill handles this automatically. If you're writing custom code, use:
```python
from excel_helpers import set_cell_value
set_cell_value(sheet, 'E11', value)
```

#### 2. Low Confidence Scores

**Symptom**: Gap analysis shows many fields <60% confidence

**Causes**:
- Insufficient source documentation
- Ambiguous or missing section headers
- Information scattered across too many documents

**Solutions**:
1. Provide multiple document types (meeting + spec + business case)
2. Ensure source docs have clear headers ("Background", "Problem Statement", "Business Sponsor:")
3. Use explicit labels in source documents
4. Review gap analysis to see what's missing, then add to source docs

#### 3. Template Not Found

**Symptom**: `Error: Template not found at [path]`

**Cause**: Incorrect path or file moved

**Solution**:
```bash
# Verify path
ls -la "path/to/template.xlsx"

# Use absolute path
python populate_template.py --template /absolute/path/to/template.xlsx
```

#### 4. Missing Fields

**Symptom**: Many "NOT FOUND" in gap analysis

**Causes**:
- Field not mentioned in source documents
- Different terminology used
- Information implied but not stated explicitly

**Solutions**:
1. Check if information exists under different wording
2. Add missing information to source documents
3. Review extraction patterns in `extraction_helpers.py` (may need customization)
4. Mark truly missing fields for manual entry

#### 5. Sheet Not Found

**Symptom**: `Error: Sheet 'ITC Project Proposal' not found`

**Cause**: Template has different sheet names or is wrong version

**Solution**:
```bash
# Inspect template
python populate_template.py --template template.xlsx --inspect

# This will show:
# Available sheets: ['Different Name', 'Scope Elements', ...]
```

Update code or ensure correct template version.

---

## Advanced Usage

### Custom Field Mappings

Edit `extraction_helpers.py` to add custom field mappings:

```python
FIELD_SOURCE_MAP = {
    'your_custom_field': {
        'primary': 'meeting_minutes',
        'pattern': r'Your Pattern:\s*(.+?)(?:\n|$)',
        'confidence_threshold': 0.8
    }
}
```

### Template Variations

For different template versions, you can:

1. Create template-specific population scripts
2. Use configuration files for field mappings
3. Extend `populate_template.py` with template auto-detection

### Integration

**With Other Skills**:
```
# First structure meeting notes
Create meeting minutes from transcript.txt

# Then populate template using structured output
Complete ITC template using the meeting minutes you just created
```

**With External Systems**:
The bundled modules can be imported into your own scripts:
```python
from populate_template import populate_itc_template
# Your custom integration code
```

---

## Additional Resources

### Documentation
- [Skills Guide](skills-guide.md) - Complete skills framework documentation
- [itc-template-filler README](.claude/skills/itc-template-filler/README.md) - Quick reference
- [Enhancements History](10-itc-template-filler-enhancements.md) - v1.0 → v1.1 changes

### Source Code
- Skill definition: `.claude/skills/itc-template-filler/SKILL.md`
- Excel helpers: `.claude/skills/itc-template-filler/excel_helpers.py`
- Extraction helpers: `.claude/skills/itc-template-filler/extraction_helpers.py`
- Population engine: `.claude/skills/itc-template-filler/populate_template.py`

### External Links
- [Anthropic: Agent Skills Best Practices](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)

---

**Document Version**: 1.0
**Consolidated From**: 07-itc-template-analysis.md, 08-itc-template-filler-skill.md, 10-itc-template-filler-enhancements.md
**Status**: Active Reference
