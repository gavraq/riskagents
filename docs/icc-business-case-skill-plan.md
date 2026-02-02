# ICC Business Case Template Filler - Implementation Plan

**Date**: 2025-01-08
**Purpose**: Create a new skill for populating ICC (Investment & Change Committee) Business Case templates
**Context**: ICC is the second governance "gate" after ITC approval, requiring detailed business case with resources, budget, and implementation plan

---

## Executive Summary

### The Governance Flow

```
ITC (Investment Technology Committee)
  Purpose: Strategic alignment, project prioritization
  Template: ITC Project Template (4 sheets, ~350 fields)
  Gate: Initial approval to proceed with planning
  ↓
ICC (Investment & Change Committee)
  Purpose: Detailed business case approval
  Template: ICC Business Case Template (17 sheets, ~2000+ fields)
  Gate: Final approval with budget and resources
```

### Current State

**Existing Skill**: `project-template-filler`
- **Problem**: Named generically but specifically designed for ITC template
- **Keywords**: "fill template", "complete template", "governance template" (too broad)
- **Implementation**: Hardcoded for ITC structure (4 sheets)

**New Requirement**: ICC Business Case template filler
- **Complexity**: 17 sheets vs 4 sheets (4x larger)
- **Detail Level**: Full business case vs project proposal
- **Relationship**: Builds on ITC-approved project

### Proposed Solution

**Rename existing skill**: `project-template-filler` → `itc-template-filler`
- More specific naming
- Clear trigger keywords
- No confusion with other templates

**Create new skill**: `icc-business-case-filler`
- Separate skill for ICC template
- Can reference ITC output as input
- Handles 17-sheet complexity

---

## Detailed Analysis

### ICC Template Structure

**17 Sheets** (vs ITC's 4):

| Sheet | Purpose | Complexity | Populated Fields | Merged Cells |
|-------|---------|------------|------------------|--------------|
| **Guidelines** | Instructions | Low | 28 | 16 |
| **Project Summary** | Executive overview | High | 152 | 57 |
| **Sheet2** | Unknown (legacy?) | Low | 71 | 0 |
| **Sheet1** | Unknown (legacy?) | Low | 29 | 0 |
| **Finances** | Budget breakdown | Very High | 1190 | 7 |
| **Milestones & Benefits** | Timeline & benefits | High | 164 | 126 |
| **Business and Asset Class** | Business unit impact | Medium | 63 | 9 |
| **Technology Simplification Objec** | Tech objectives | Low | 27 | 0 |
| **Technology Impact Assessment** | IT impact | Medium | 135 | 37 |
| **OPR Checklist** | Operational risk | Medium | 177 | 25 |
| **OPR IT - Tier 1 & Tier 0** | IT operational risk | Medium | ? | ? |
| **RAIDs** | Risks, Assumptions, Issues, Dependencies | Medium | ? | ? |
| **X Dependencies** | Project dependencies | Medium | ? | ? |
| **PDLC Artefacts** | Project lifecycle artifacts | Low | ? | ? |
| **Project Governance** | Governance structure | Medium | ? | ? |
| *+ 2 more sheets* | | | | |

**Total Estimated Fields**: ~2000+ (vs ITC's 358)

**Key Differences from ITC**:
1. **Financial Detail**: Entire "Finances" sheet with 1190 fields (budgets, costs, FTE, phasing)
2. **Milestones**: Detailed project timeline with benefits tracking
3. **Risk Management**: Dedicated RAIDS and OPR sheets
4. **Dependencies**: Cross-project dependency tracking
5. **Governance**: Formal governance structure definition

### Overlap with ITC

Many ICC fields can be **pre-populated from ITC output**:

| ICC Field | Source | Notes |
|-----------|--------|-------|
| Project Name | ITC D4 | Direct copy |
| Business Sponsor | ITC E7 | Direct copy |
| Problem Statement | ITC E11 | Can expand with more detail |
| Benefits | ITC E28-E37 | Must be **quantified** in ICC |
| High-level Timeline | ITC E48-E49 | Must be **detailed** in ICC |
| Scope Overview | ITC Scope Elements | Must be **expanded** in ICC |

**Reuse Opportunity**: ICC skill can read populated ITC template as input!

---

## Implementation Plan

### Phase 1: Rename Existing Skill (1-2 hours)

#### 1.1 Rename Skill Directory

```bash
mv .claude/skills/project-template-filler .claude/skills/itc-template-filler
```

#### 1.2 Update SKILL.md

**File**: `.claude/skills/itc-template-filler/SKILL.md`

**Changes**:
```yaml
---
name: itc-template-filler  # Changed from project-template-filler
description: Automatically fills out ITC (Investment Technology Committee) Project Template Excel files. Use when user asks to "complete ITC template", "fill ITC template", "populate ITC project template". Extracts information from meeting minutes and documents.
---

# ITC Template Filler Skill  # Changed title

## Purpose
Automates the population of **ITC Project Proposal templates** for initial project approval gate...
```

**Update trigger keywords to be ITC-specific**:
- "ITC template"
- "fill ITC template"
- "complete ITC project template"
- "Investment Technology Committee template"

**Remove generic keywords**:
- ~~"fill template"~~ (too generic)
- ~~"governance template"~~ (too generic)

#### 1.3 Update change-agent.md

**File**: `.claude/agents/change-agent.md`

**Change**:
```markdown
### itc-template-filler  # Changed from project-template-filler
Populates ITC (Investment Technology Committee) project governance templates by extracting information from meeting minutes, project plans, and business cases. Handles multi-sheet Excel templates with field mappings for project details, scope, estimates, and benefit quantification.

**Use when**: User needs to complete an **ITC template**, prepare **ITC** governance documentation, fill out **ITC** project proposal forms, or compile information for **Investment Technology Committee** presentation.
```

#### 1.4 Update Documentation

**Files to update**:
- `docs/skills-guide.md` - Change skill name to `itc-template-filler`
- `docs/itc-template-filler-reference.md` - Update skill name throughout
- `README.md` - Update skill list

**Search and replace**:
- `project-template-filler` → `itc-template-filler` (in context of the skill name)

#### 1.5 Test Renamed Skill

```
Test query: "Complete the ITC template for Energy VaR project"
Expected: itc-template-filler skill invoked
```

---

### Phase 2: Create ICC Business Case Skill (6-8 hours)

#### 2.1 Analyze ICC Template in Detail

**Script to create**: `analyze_icc_template.py`

```python
#!/usr/bin/env python3
"""
Analyze ICC Business Case Template structure
Generate field mapping documentation
"""
import openpyxl
from pathlib import Path

template_path = Path('data/icbc_standard_bank/Processes/Change Mgt/ICC Business Case Template 2025-draft.xlsm')
wb = openpyxl.load_workbook(template_path)

for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]

    # For each sheet, identify:
    # 1. Input fields (cells for user data entry)
    # 2. Formula cells (don't overwrite)
    # 3. Merged cell ranges
    # 4. Data validation rules
    # 5. Conditional formatting

    # Generate field mapping documentation
```

**Output**: `docs/icc-template-analysis.md` (similar to what we did for ITC)

#### 2.2 Create Skill Directory Structure

```bash
mkdir -p .claude/skills/icc-business-case-filler
```

**Structure**:
```
.claude/skills/icc-business-case-filler/
├── SKILL.md                    # Skill definition
├── README.md                   # User documentation
├── excel_helpers.py            # Symlink to itc-template-filler/excel_helpers.py
├── extraction_helpers.py       # Symlink to itc-template-filler/extraction_helpers.py
├── icc_field_mappings.py       # ICC-specific field mappings (NEW)
└── populate_icc_template.py    # ICC population engine (NEW)
```

**Reuse from ITC skill**:
- `excel_helpers.py` - Same merged cell handling
- `extraction_helpers.py` - Same multi-source extraction

**New for ICC**:
- `icc_field_mappings.py` - ICC sheet/field structure
- `populate_icc_template.py` - ICC-specific population logic

#### 2.3 Design Field Mapping Strategy

**ICC-Specific Challenges**:

1. **Finances Sheet** (1190 fields):
   - Budget phasing by quarter/year
   - Cost categories (Capex, Opex, FTE)
   - Multi-year projections
   - Vendor cost breakdowns

2. **Milestones & Benefits** (164 fields with 126 merged cells):
   - Gantt-chart style timeline
   - Benefit quantification with tracking
   - Dependencies between milestones

3. **RAIDS**:
   - Risk register
   - Assumptions log
   - Issues tracker
   - Dependencies map

**Mapping Strategy**:

```python
# icc_field_mappings.py

ICC_FIELD_MAP = {
    # Project Summary sheet
    'project_summary': {
        'project_name': 'B5',
        'business_sponsor': 'B6',
        'it_sponsor': 'B7',
        'project_manager': 'B8',
        'executive_summary': 'B10:M15',  # Merged
        'problem_statement': 'B16:M25',  # Merged
        # ... etc
    },

    # Finances sheet
    'finances': {
        'total_capex': 'E10',
        'total_opex': 'E11',
        'total_fte': 'E12',
        'y1_q1_capex': 'F20',
        'y1_q2_capex': 'G20',
        # ... extensive quarterly breakdown
    },

    # Can be pre-populated from ITC
    'from_itc': {
        'project_name': ('ITC Project Proposal', 'D4'),
        'business_sponsor': ('ITC Project Proposal', 'E7'),
        'problem_statement': ('ITC Project Proposal', 'E11'),
        'scope_elements': ('Scope Elements', 'A4:H*'),
        # ... etc
    }
}
```

#### 2.4 Create SKILL.md

**Key sections**:

```markdown
---
name: icc-business-case-filler
description: Automatically fills out ICC (Investment & Change Committee) Business Case Template Excel files. Use when user asks to "complete ICC template", "fill ICC business case", "populate ICC template". Builds detailed business case with finances, milestones, and risk management.
---

# ICC Business Case Filler Skill

## Purpose
Automates population of ICC Business Case templates for final project approval.
The ICC is the second governance gate after ITC approval, requiring detailed
business case with full budget, resource plan, and implementation timeline.

## When to Use
**ALWAYS USE THIS SKILL** when:
- User asks to "complete ICC template"
- User mentions "ICC business case"
- User needs "Investment & Change Committee" documentation
- User has ITC-approved project and needs detailed business case

**Keywords**:
"ICC template", "ICC business case", "Investment & Change Committee",
"complete ICC", "fill ICC template"

## Input Parameters

### Required
- `template_path`: Path to ICC Business Case Template
- `output_path`: Where to save populated template

### Optional but Recommended
- `itc_template_path`: Path to populated ITC template (for pre-population)
- `meeting_minutes`: Additional meeting notes since ITC approval
- `business_case`: Detailed financial justification
- `resource_plan`: Resource allocation and FTE details
- `risk_register`: Known risks and mitigations

## What This Skill Provides

### 1. Pre-Population from ITC
If ITC template provided, automatically copies:
- Project name, sponsors, problem statement
- High-level scope and timeline
- Benefit themes (to be quantified in ICC)

### 2. Comprehensive Template Population
Populates 17 sheets:
- **Project Summary**: Executive overview
- **Finances**: Multi-year budget with quarterly phasing
- **Milestones & Benefits**: Detailed timeline with benefit tracking
- **Business and Asset Class**: Business unit impact analysis
- **Technology Impact**: IT infrastructure changes
- **OPR Checklist**: Operational risk assessment
- **RAIDs**: Risk, Assumption, Issue, Dependency tracking
- **Dependencies**: Cross-project dependencies
- **Governance**: Project governance structure
- ... and 8 more sheets

### 3. Gap Analysis
Identifies:
- Fields successfully pre-populated from ITC
- Fields extracted from source documents
- **Critical gaps** requiring manual input (especially financial details)
- Confidence scores for all extractions

## Example Usage

### Scenario: ITC-Approved Project Needs ICC Business Case

Input:
- Populated ITC template from previous approval
- Additional financial analysis document
- Resource allocation spreadsheet
- Updated risk register

Output:
- ICC template 60-80% populated (from ITC + documents)
- Gap analysis highlighting required financial details
- Recommendations for completing business case

```

#### 2.5 Implement ICC Population Logic

**File**: `populate_icc_template.py`

```python
#!/usr/bin/env python3
"""
ICC Business Case Template Population
Can pre-populate from ITC template and additional sources
"""

import openpyxl
from pathlib import Path
from excel_helpers import set_cell_value, validate_template
from icc_field_mappings import ICC_FIELD_MAP

def pre_populate_from_itc(icc_workbook, itc_template_path):
    """
    Pre-populate ICC fields from completed ITC template

    Args:
        icc_workbook: ICC template workbook
        itc_template_path: Path to populated ITC template

    Returns:
        dict: Fields pre-populated with source attribution
    """
    success, itc_wb, error = validate_template(itc_template_path)
    if not success:
        return {}

    pre_populated = {}

    # Project Summary sheet in ICC
    icc_summary = icc_workbook['Project Summary']
    itc_proposal = itc_wb['ITC Project Proposal']

    # Copy basic fields
    project_name = itc_proposal['D4'].value
    if project_name:
        set_cell_value(icc_summary, 'B5', project_name)
        pre_populated['project_name'] = ('D4 from ITC', 1.0)

    business_sponsor = itc_proposal['E7'].value
    if business_sponsor:
        set_cell_value(icc_summary, 'B6', business_sponsor)
        pre_populated['business_sponsor'] = ('E7 from ITC', 1.0)

    # ... continue for all mappable fields

    return pre_populated

def populate_icc_template(template_path, output_path,
                         itc_template_path=None,
                         business_case_data=None,
                         verbose=True):
    """
    Main ICC template population function
    """
    # Load ICC template
    success, icc_wb, error = validate_template(template_path)
    if not success:
        return {'success': False, 'message': error}

    populated_count = 0
    sources = {}

    # Step 1: Pre-populate from ITC if provided
    if itc_template_path:
        if verbose:
            print("Pre-populating from ITC template...")
        itc_fields = pre_populate_from_itc(icc_wb, itc_template_path)
        populated_count += len(itc_fields)
        sources['ITC'] = itc_fields

    # Step 2: Populate from business case data
    if business_case_data:
        if verbose:
            print("Populating from business case...")
        # ... implementation

    # Step 3: Save
    icc_wb.save(output_path)

    return {
        'success': True,
        'message': f'Populated {populated_count} fields',
        'populated_fields': populated_count,
        'sources': sources
    }
```

#### 2.6 Update change-agent.md

**Add new skill**:

```markdown
### icc-business-case-filler
Populates ICC (Investment & Change Committee) Business Case templates for final project approval. Handles 17-sheet template with detailed financials, milestones, risk management, and governance structure. Can pre-populate from ITC-approved project template.

**Use when**: User needs to complete **ICC template**, prepare **ICC business case**, fill out **Investment & Change Committee** documentation, or create detailed business case after ITC approval.

**Note**: This is the second governance gate after ITC. Can automatically reuse data from ITC template if provided.
```

#### 2.7 Create Documentation

**File**: `docs/icc-business-case-reference.md`

Similar structure to `itc-template-filler-reference.md`:
- Quick start
- Template structure (17 sheets)
- How it works
- Pre-population from ITC
- Field mapping strategy
- Real-world example
- Troubleshooting

---

### Phase 3: Testing & Refinement (2-3 hours)

#### 3.1 Test Renamed ITC Skill

```
Query: "Complete the ITC template for the Credit Risk project"
Expected: itc-template-filler invoked
Verify: Skill name displays correctly
```

#### 3.2 Test New ICC Skill

**Test Case 1: ICC from Scratch**
```
Query: "Create ICC business case template for Energy VaR project"
Input: Meeting minutes + financial analysis
Expected: icc-business-case-filler invoked
Result: Partial population (~40-60%)
```

**Test Case 2: ICC from ITC**
```
Query: "Complete ICC template using the ITC template we created earlier"
Input: Populated ITC template + additional docs
Expected: icc-business-case-filler invoked
Result: Higher population (~60-80%) due to ITC pre-population
```

#### 3.3 Test Disambiguation

```
Query: "Complete the template for Energy VaR"  # Ambiguous
Expected: Agent asks "ITC or ICC template?"
```

Update change-agent if needed to clarify:
```markdown
When user says "complete template" without specifying:
- If project is new/early stage → Assume ITC
- If project is ITC-approved → Assume ICC
- If unclear → Ask user to clarify
```

---

## Implementation Checklist

### Phase 1: Rename ITC Skill ✅
- [ ] Rename skill directory: `project-template-filler` → `itc-template-filler`
- [ ] Update `SKILL.md` name and description with ITC-specific keywords
- [ ] Update `README.md` with ITC-specific content
- [ ] Update `change-agent.md` skill reference
- [ ] Update `docs/skills-guide.md` skill list
- [ ] Update `docs/itc-template-filler-reference.md` skill name
- [ ] Update main `README.md`
- [ ] Test skill invocation with "complete ITC template"

### Phase 2: Create ICC Skill ✅
- [ ] Analyze ICC template structure (17 sheets, ~2000 fields)
- [ ] Document ICC template in `docs/icc-template-analysis.md`
- [ ] Create skill directory `.claude/skills/icc-business-case-filler/`
- [ ] Create/symlink helper modules
  - [ ] Symlink `excel_helpers.py`
  - [ ] Symlink `extraction_helpers.py`
  - [ ] Create `icc_field_mappings.py` (ICC-specific)
  - [ ] Create `populate_icc_template.py` (with ITC pre-population)
- [ ] Write `SKILL.md` with ICC-specific keywords
- [ ] Write `README.md` for ICC skill
- [ ] Add skill to `change-agent.md`
- [ ] Create `docs/icc-business-case-reference.md`
- [ ] Update `docs/skills-guide.md` with ICC skill

### Phase 3: Testing ✅
- [ ] Test ITC skill invocation (verify rename worked)
- [ ] Test ICC skill invocation (new skill)
- [ ] Test ICC with ITC pre-population
- [ ] Test disambiguation ("complete template" → which one?)
- [ ] Update documentation based on testing

---

## Risk Assessment

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Breaking existing ITC usage** | High | Careful rename, thorough testing |
| **ICC complexity overwhelming** | Medium | Phase implementation, start with core sheets |
| **ITC→ICC mapping incomplete** | Medium | Clear gap analysis, manual completion expected |
| **Skill disambiguation failures** | Low | Update change-agent with clarification logic |

### Success Criteria

✅ **ITC skill still works** after rename
✅ **ICC skill invokes** with correct keywords
✅ **ITC→ICC pre-population** works for ~20-30 common fields
✅ **Gap analysis** clearly identifies missing financial details
✅ **Documentation** explains ITC vs ICC difference

---

## Estimated Effort

| Phase | Effort | Complexity |
|-------|--------|------------|
| **Phase 1: Rename ITC** | 1-2 hours | Low |
| **Phase 2: Create ICC** | 6-8 hours | Medium-High |
| **Phase 3: Testing** | 2-3 hours | Medium |
| **Total** | **9-13 hours** | |

---

## Future Enhancements

1. **Cascade Updates**: When ITC template changes, offer to update ICC
2. **Financial Wizard**: Interactive prompts for complex financial fields
3. **Risk Library**: Pre-populated risk categories based on project type
4. **Benefit Tracking**: Link ICC benefits to actual outcomes over time
5. **Multi-Project**: Handle program-level ICC with multiple sub-projects

---

## Appendix: Governance Flow

```
Project Lifecycle Governance Gates:

┌──────────────────────────────────────────────────────────────┐
│ Gate 1: ITC (Investment Technology Committee)                │
│ ─────────────────────────────────────────────────────────── │
│ Purpose:    Strategic fit, prioritization                    │
│ Template:   ITC Project Template (4 sheets)                  │
│ Focus:      Problem, benefits, high-level scope              │
│ Approval:   Proceed to detailed planning                     │
│ Skill:      itc-template-filler                             │
└──────────────────────────────────────────────────────────────┘
                            ↓
                  ITC Approved ✓
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ Planning Phase (3-6 months)                                  │
│ ─────────────────────────────────────────────────────────── │
│ - Detailed requirements                                       │
│ - Budget development                                          │
│ - Resource planning                                           │
│ - Risk assessment                                             │
│ - Vendor quotes                                               │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ Gate 2: ICC (Investment & Change Committee)                  │
│ ─────────────────────────────────────────────────────────── │
│ Purpose:    Final business case approval                     │
│ Template:   ICC Business Case Template (17 sheets)           │
│ Focus:      Detailed budget, resources, timeline, risks      │
│ Approval:   Funding approval, proceed to execution           │
│ Skill:      icc-business-case-filler                        │
└──────────────────────────────────────────────────────────────┘
                            ↓
                  ICC Approved ✓
                            ↓
                Project Execution
```

---

**Document Version**: 1.0
**Status**: Implementation Plan Ready for Approval
**Next Step**: Begin Phase 1 (Rename ITC Skill)
