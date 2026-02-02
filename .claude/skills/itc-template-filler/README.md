# ITC Template Filler Skill

Automates population of ITC (Investment Technology Committee) Project Templates for banking governance processes.

**Governance Context**: ITC is the first governance gate in the project approval process. After ITC approval, projects proceed to ICC (Investment & Change Committee) for detailed business case approval using the `icc-business-case-filler` skill.

## Quick Start

This skill is automatically invoked when you ask to "complete ITC template", "fill template", or "populate project template".

### Example Usage

```
Complete the ITC template for the Energy VaR project using the meeting minutes
from meetings/energy_var_meeting.md and the template at templates/ITC_Template.xlsx
```

The skill will:
1. Extract project information from meeting minutes
2. Populate the multi-sheet Excel template (handling merged cells safely)
3. Generate a gap analysis report showing what was populated and what's missing
4. Provide confidence scores for extracted data

## Bundled Modules

This skill includes three Python modules that handle the technical complexity:

### 1. excel_helpers.py

Safe Excel manipulation with merged cell handling:

```python
from excel_helpers import set_cell_value, validate_template

# Handles merged cells automatically
set_cell_value(proposal_sheet, 'E11', problem_statement)

# Validate template before processing
success, workbook, error = validate_template(template_path)
```

**Why this matters:** ITC templates use merged cells extensively (e.g., E11:E21 for problem statement). Direct assignment to merged cells fails with `AttributeError`. This module handles that complexity.

### 2. extraction_helpers.py

Multi-source data extraction with confidence scoring:

```python
from extraction_helpers import inventory_source_documents, extract_field_with_confidence

# Read and categorize multiple sources
sources = inventory_source_documents([
    'meeting_minutes.md',
    'project_plan.md',
    'business_case.md'
])

# Extract with confidence score and source attribution
value, confidence, source = extract_field_with_confidence('project_name', sources)
```

**Features:**
- Automatic document classification (meeting minutes vs technical spec vs business case)
- Primary/fallback source strategy
- Confidence scoring (0-1.0)
- Conflict detection when multiple sources disagree
- Extraction provenance reporting

### 3. populate_template.py

Main template population engine:

```python
from populate_template import populate_itc_template

result = populate_itc_template(
    template_path='templates/ITC_Template.xlsx',
    output_path='outputs/Energy_VaR_ITC_Proposal.xlsx',
    project_data={
        'project_name': 'Energy VaR Migration to Murex/FMDM',
        'business_sponsor': 'Philip (Front Office) / Richard (Risk)',
        'problem_statement': '...',
        'benefits': {...},
        # ... etc
    }
)

print(f"Populated {result['populated_fields']} fields")
```

**Can also run standalone:**

```bash
# Inspect template structure
python populate_template.py --template template.xlsx --inspect

# Populate from JSON data
python populate_template.py --template template.xlsx --output output.xlsx --data data.json
```

## Template Structure

The ITC Project Template contains 4 sheets with ~350 total fields:

### ITC Project Proposal (Main Sheet)

**Section 1: Problem Statement**
- Project name (D4)
- Submission date (E5)
- Sponsors (E7, E8)
- Functional area & business unit (E9, E10)
- Background & problem statement (E11) - **merged cell**
- Key drivers (E13-E17)
- Business readiness (E22-E25)

**Section 2: Benefits/Costs/Duration**
- Benefit themes (E28-E37)
- Business unit beneficiaries (E40-E44)
- Cost estimate (E46)
- Cost breakdown (E47) - **merged cell**
- Duration (E48)
- Timeline (E49) - **merged cell**

### Scope Elements Sheet

Requirements breakdown with:
- Description (A column)
- BRD status (B column)
- Enhancement vs like-for-like (C column)
- Sponsorship (E column)
- Rationale (F column)
- Resource requirements (H column)

### Estimates Sheet

Task-level breakdown with:
- Task description (B column)
- Dependencies (C column)
- Duration estimates (D column)
- Resource owners (G column)

### Sheet2

Reference data (typically left unchanged)

## Data Extraction Strategy

### From Meeting Minutes

Extract:
- Project name (from title or "Project:" lines)
- Problem statement (from "Background", "Problem", "Current State" sections)
- Sponsors (from attendees with "Sponsor" in title)
- Decisions → Scope elements
- Action items → Tasks
- Timeline discussions → Readiness assessment
- Benefit mentions → Benefit themes

### From Project Plan/Scope

Extract:
- Requirements list (R01, R02, etc.)
- Work breakdown structure
- Dependencies
- Resource allocation
- Timeline/milestones

### From Business Case

Extract:
- Quantified benefits (revenue, cost savings)
- FTE impacts
- Regulatory/compliance drivers
- Capital/liquidity impacts

## Confidence Scoring

All extracted fields receive confidence scores:

- **High (85-100%)**: Direct extraction, exact matches (e.g., "Project: Energy VaR Migration")
- **Medium (60-84%)**: Inferred from context (e.g., sponsor inferred from meeting attendees)
- **Low (40-59%)**: Weak signals, ambiguous sources
- **None (<40%)**: No data found, field left blank

## Gap Analysis Report

The skill generates a detailed report showing:

```markdown
# Template Population Report
## Project: Energy VaR Migration
## Generated: 2025-01-08

### Population Summary
- Total Fields: 143
- Populated: 128 (90%)
- Missing: 15 (10%)
- Overall Confidence: 85%

### Section 1: Problem Statement - ✓ COMPLETE
✅ Project Name (D4): Energy VaR Migration to Murex/FMDM (Confidence: 95%)
✅ Business Sponsor (E7): Philip / Richard (Confidence: 95%)
⚠️  IT ExCo Sponsor (E8): TBC - Manual input required

### Fields Requiring Manual Input
1. IT ExCo Sponsor (E8) - HIGH PRIORITY
2. Detailed cost breakdown vendor quotes - MEDIUM PRIORITY
...
```

## Real-World Example

From the Energy VaR project (actual implementation):

**Input:**
- 2 meeting minutes files (strategic meeting + technical meeting)
- ITC template with merged cells, formulas, data validation

**Output:**
- 143 cells populated across 4 sections
- 90% complete (10% needs sponsor validation)
- Gap analysis report (22KB)
- Success on first run

**Key learnings:**
- Merged cells ARE the norm in governance templates
- Multi-source synthesis is essential (strategic + technical meetings)
- Confidence scoring helps prioritize manual review
- Gap analysis critical for governance sign-off

## Common Issues & Solutions

### Issue 1: "MergedCell object attribute 'value' is read-only"

**Cause:** Direct assignment to merged cell
```python
proposal_sheet['E11'] = value  # FAILS if E11 is merged
```

**Solution:** Use bundled helper
```python
set_cell_value(proposal_sheet, 'E11', value)  # Works for merged or regular cells
```

### Issue 2: Low extraction confidence

**Cause:** Insufficient source documentation

**Solution:**
1. Provide multiple source types (meeting + spec + business case)
2. Review gap analysis to see what's missing
3. Manually add missing fields to sources before re-running

### Issue 3: Template not found or corrupted

**Cause:** Path incorrect or file locked

**Solution:**
```python
from excel_helpers import validate_template
success, workbook, error = validate_template(template_path)
if not success:
    print(f"Error: {error}")
```

## Integration with Other Skills

Works well with:
- **meeting-minutes**: Structure meeting notes first, then populate template
- **project-planner**: Generate project plan, then populate template
- **status-reporter**: Update templates periodically as project progresses

## Development Notes

### Based on Anthropic Best Practices

This skill follows ["Equipping Agents for the Real World with Agent Skills"](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) principles:

1. **Progressive Disclosure**: Metadata in SKILL.md, detailed implementation in bundled scripts
2. **Dual-Purpose Scripts**: Modules serve as both executables and reference documentation
3. **Clear Execution Intent**: Skill description makes it clear when to invoke vs when to read reference code
4. **Modular Design**: Separate concerns (Excel manipulation, extraction, population) into reusable modules

### Enhancement History

**Version 1.0 → 1.1 (Current)**
- Added merged cell handling (critical blocker resolved)
- Bundled executable Python modules
- Multi-source extraction with confidence scoring
- Gap analysis reporting
- Real-world validation with Energy VaR project

**Based on recommendations from:**
`/Users/gavinslater/projects/riskagent/data/icbc_standard_bank/Projects/Energy/Project_Template_Filler_Skill_Improvements.md`

### Future Enhancements

Potential improvements (not yet implemented):

- Historical project data learning
- Integration with JIRA/MS Project
- Real-time collaboration tracking
- Multi-template support (different governance bodies)
- Approval workflow integration

## License & Attribution

Created for Risk Agent framework.
Tested on real banking governance templates (ICBC Standard Bank).

---

**Last Updated**: 2025-01-08
**Version**: 1.1
**Supports**: ITC Project Template 2025
