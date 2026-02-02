---
name: icc-business-case-filler
description: Automatically fills out ICC (Investment & Change Committee) Business Case Template Excel files with interactive clarification for missing information. Use when user asks to "complete ICC template", "fill ICC business case", "populate ICC template", or "prepare ICC approval". This is the second governance gate after ITC approval, requiring detailed financials, resources, and implementation plans.
---

# ICC Business Case Filler Skill

## Purpose

Automates the population of **ICC (Investment & Change Committee) Business Case templates** for final project approval and funding. This is the **second governance gate** in the project approval process, following ITC approval. ICC requires comprehensive business case documentation including detailed financials, resource plans, milestones, and risk management.

**Governance Context**:
- **ITC (First Gate)**: Strategic alignment → use `itc-template-filler` skill
- **ICC (Second Gate)**: Detailed business case → use THIS skill

## When to Use

**ALWAYS USE THIS SKILL** (do not write custom Python scripts) when:
- User asks to "complete ICC template" or "fill ICC business case"
- User mentions "ICC Business Case Template" or "Investment & Change Committee"
- User needs detailed business case after ITC approval
- User asks to "prepare for ICC" or "get ICC approval"
- User has ITC-approved project and needs funding approval

**Keywords that trigger this skill:**
"ICC template", "ICC business case", "Investment & Change Committee", "complete ICC", "prepare ICC", "ICC approval"

## 🌟 Key Feature: Interactive Clarification Mode

**Unlike one-shot template population**, this skill uses an **interactive clarification approach** for the complex ICC template:

### How It Works

1. **Initial Population** (40-60% complete):
   - Pre-populates from ITC template if provided (~30-40 fields)
   - Extracts from meeting minutes and business case documents
   - Populates all fields with available information

2. **Gap Analysis** (Intelligent identification):
   - Identifies missing CRITICAL fields (required for ICC approval)
   - Identifies missing HIGH priority fields (strongly recommended)
   - Categorizes gaps by: Financials, Timeline, Resources, Risks, etc.

3. **Targeted Clarification Questions** (Organized by priority):
   - Generates specific questions for missing information
   - Groups questions by category and priority
   - Provides context: which sheet, which cell, why it's needed
   - Includes validation hints (date format, currency, etc.)

4. **Iterative Completion**:
   - User provides answers to clarification questions
   - Skill populates additional fields
   - Repeats until all CRITICAL fields complete

### Example Workflow

```
User: "Complete the ICC template for Energy VaR project using the ITC template we created"

Skill:
  ✓ Pre-populated 35 fields from ITC template
  ✓ Extracted 12 fields from meeting minutes
  ⚠  47 fields populated (40% complete)
  ⚠  15 CRITICAL fields missing
  ⚠  23 HIGH priority fields missing

  Generating clarification report...

[Returns organized questions like:]

## Financial Details 🔴 CRITICAL

**Total Capital Expenditure** (Sheet: Finances, Cell: E10)
- What is the total CapEx for this project across all years? (in £'000)
- Validation: numeric_currency

**Total Operational Expenditure** (Sheet: Finances, Cell: E11)
- What is the total OpEx for this project across all years? (in £'000)
- Validation: numeric_currency

## Timeline & Milestones 🔴 CRITICAL

**Expected Project Start Date** (Sheet: Project Summary, Cell: F6)
- What is the expected project start date?
- Validation: DD/MM/YYYY format

[...continues with all missing critical fields...]

---

User: [Provides answers]

Skill:
  ✓ Populated 15 additional CRITICAL fields
  ✓ Template now 85% complete
  ⚠  8 HIGH priority fields still missing

  [Generates follow-up questions for remaining high-priority items]
```

## What This Skill Provides

### 1. Comprehensive Template Population (17 Sheets)

The ICC template has **17 sheets** with ~2000+ fields:

**Core Sheets:**
- **Project Summary**: Executive overview, key dates, costs
- **Finances**: Detailed budget with quarterly phasing (~1190 fields!)
- **Milestones & Benefits**: Timeline and quantified benefits
- **RAIDs**: Risks, Assumptions, Issues, Dependencies
- **Business and Asset Class**: Business unit impact analysis
- **Technology Impact**: IT infrastructure changes
- **OPR Checklist**: Operational risk assessment
- **Dependencies**: Cross-project dependencies
- **Project Governance**: Governance structure
- ... and 8 more sheets

### 2. ITC Template Pre-Population

If you provide the populated ITC template, the skill automatically copies:

| ICC Field | ITC Source | Notes |
|-----------|------------|-------|
| Project Name | ITC D4 | Direct copy |
| Sponsor | ITC E7 | Direct copy |
| Problem Statement | ITC E11 | Base for expansion |
| Benefit Themes | ITC E28-E37 | **Must be quantified in ICC** |
| High-level Scope | ITC Scope Elements | **Must be expanded in ICC** |
| Timeline Estimates | ITC E48-E49 | **Must be detailed in ICC** |

**Typical ITC→ICC Pre-population**: 30-40 fields (~20% of template)

### 3. Intelligent Gap Analysis

The skill categorizes missing fields by:

**Priority Levels:**
- 🔴 **CRITICAL**: Required for ICC approval (project start date, total cost, sponsor, PM)
- 🟡 **HIGH**: Strongly recommended (risk register, key milestones, FTE)
- 🟢 **MEDIUM**: Good to have (detailed benefit quantification, dependencies)
- ⚪ **LOW**: Optional (additional comments, supporting details)

**Categories:**
- Project Information
- Financial Details
- Timeline & Milestones
- Benefits & Business Case
- Risks & Issues
- Resources & Team
- Governance & Compliance

### 4. Clarification Report Generation

**Output Format:**
```markdown
# ICC Business Case - Information Required

## Financial Details

### 🔴 CRITICAL

**Total Project Cost 2025** (Sheet: Project Summary, Cell: F8)
- What is the total project cost for 2025? (in £'000)
- *Validation: numeric_currency*

**Total CapEx** (Sheet: Finances, Cell: TBD)
- What is the total Capital Expenditure across all years?
- *Validation: numeric_currency*

### 🟡 HIGH

**Total FTE Requirement** (Sheet: Finances, Cell: TBD)
- What is the total FTE requirement for this project?
- *Validation: numeric*

[...continues...]

## Next Steps

1. Review the critical (🔴) questions first - required for ICC approval
2. Provide answers for high priority (🟡) questions
3. Medium/low priority can be addressed later if needed
```

## Input Parameters

### Required
- `template_path`: Path to ICC Business Case Template (.xlsm file)
- `output_path`: Where to save populated template (.xlsm file)

### Optional but Recommended
- `itc_template_path`: Path to populated ITC template (enables 30-40 field pre-population)
- `source_documents`: List of file paths to extract information from (meeting minutes, business cases, plans, etc.)
  - Example: `["data/meeting.md", "data/financial_analysis.docx", "data/risk_register.xlsx"]`
- `interactive_mode`: Default `true` - enables clarification questions for missing fields
- `verbose`: Default `true` - show progress messages

### Advanced
- `business_case_data`: Pre-extracted dictionary of business case information (optional, advanced use only)
- `clarification_output_path`: Where to save clarification report markdown file

## How to Invoke This Skill

The skill is designed to be called via the Risk Agent CLI. When invoked, it should:

1. **Read the ICC template** from the specified path
2. **Pre-populate from ITC** if ITC template path provided
3. **Extract from source documents** if provided (meeting minutes, business cases, etc.)
4. **Identify gaps** in critical and high-priority fields
5. **Generate clarification questions** if in interactive mode
6. **Save the populated template** with preserved VBA macros
7. **Return results** including clarification report

### Skill Invocation Template

```python
# When this skill is invoked, call the populate_icc_template function:
from .populate_icc_template import populate_icc_template

result = populate_icc_template(
    template_path=args['template_path'],
    output_path=args['output_path'],
    itc_template_path=args.get('itc_template_path'),
    source_documents=args.get('source_documents'),  # List of file paths
    interactive_mode=args.get('interactive_mode', True),
    verbose=args.get('verbose', True)
)

# result contains:
# - success: bool
# - message: str
# - populated_fields: int
# - pre_populated_from_itc: int
# - missing_critical: list
# - missing_high: list
# - clarification_report: str (if interactive_mode=True)
```

## Output Format

### Populated Excel Template
```
ICC_BusinessCase_[ProjectName]_[Date].xlsm

Sheets:
1. Project Summary (executive overview)
2. Finances (detailed budget with phasing)
3. Milestones & Benefits (timeline + quantified benefits)
4. RAIDs (risk register)
5. ... and 13 more sheets
```

### Clarification Report
```markdown
ICC_BusinessCase_Clarifications_[ProjectName].md

Organized questions by:
- Category (Financials, Timeline, Resources, etc.)
- Priority (Critical → High → Medium → Low)
- Includes: field location, validation rules, context
```

### Gap Analysis Summary
```json
{
  "populated_fields": 47,
  "pre_populated_from_itc": 35,
  "missing_critical": 15,
  "missing_high": 23,
  "completion_percentage": 40
}
```

## Bundled Modules

This skill reuses modules from `itc-template-filler` and adds ICC-specific logic:

### 1. excel_helpers.py (Shared)
Safe Excel manipulation with merged cell handling

### 2. extraction_helpers.py (Shared)
Multi-source data extraction with confidence scoring

### 3. icc_field_mappings.py (NEW)
ICC-specific field definitions with:
- Field locations and priorities
- Clarification prompts for each field
- Validation rules
- Category organization
- ITC→ICC mapping rules

### 4. populate_icc_template.py (NEW)
ICC population engine with:
- ITC pre-population logic
- Gap detection
- Interactive clarification question generation
- Iterative completion support

## Example Usage Scenarios

### Scenario 1: ITC-Approved Project Needs ICC

**Input:**
- Populated ITC template (from previous approval)
- Updated financial analysis with vendor quotes
- Resource allocation plan
- Risk register

**Process:**
```
1. Skill pre-populates 35 fields from ITC template
2. Skill extracts 12 additional fields from documents
3. Skill identifies 15 critical missing fields
4. Skill generates targeted clarification questions
5. User provides missing information
6. Skill completes template (85% populated)
7. Remaining 15% flagged for manual review
```

**Output:**
- ICC template 85% complete
- Clarification report with 8 remaining questions
- Ready for sponsor review

### Scenario 2: New Project (No ITC Yet)

**Input:**
- Comprehensive business case document
- Financial model
- Project plan

**Process:**
```
1. Skill extracts ~40-50 fields from business case
2. Skill identifies 60+ missing fields
3. Skill generates extensive clarification report
4. User provides information in batches (Critical first)
5. Multiple rounds of clarification
6. Iterative completion over 2-3 sessions
```

**Output:**
- ICC template 70% complete after round 1
- 90% complete after round 2
- 95% complete after round 3

## Critical Feature: Merged Cell Handling

**⚠️ IMPORTANT:** ICC templates extensively use merged cells (126 merged ranges in Milestones & Benefits sheet alone!). This skill includes specialized handling inherited from `itc-template-filler`.

The bundled `excel_helpers.py` module automatically handles merged cells - no special action required.

## Integration with ITC Skill

**Typical Project Flow:**

```
1. Early Stage → Use itc-template-filler
   ↓ ITC Approval ✓

2. Detailed Planning Phase (3-6 months)
   - Develop detailed financials
   - Secure resource commitments
   - Complete risk assessment
   - Get vendor quotes
   ↓

3. ICC Preparation → Use icc-business-case-filler
   - Pre-populate from ITC template
   - Add detailed financial info
   - Interactive clarification for gaps
   - Iterative completion
   ↓ ICC Approval ✓

4. Project Execution
```

## Quality Assurance

### Pre-Population Validation
- ✅ ITC template exists and is valid Excel file
- ✅ ITC contains expected sheets and structure
- ✅ ICC template structure matches expected format

### Field-Level Validation
- ✅ Date fields validated (DD/MM/YYYY format)
- ✅ Currency fields validated (numeric, £'000)
- ✅ Enum fields validated (High/Medium/Low)
- ✅ Required fields flagged if missing

### Completion Scoring
- **40-60%**: Initial population (ITC + documents)
- **70-85%**: After critical clarifications
- **85-95%**: After high priority clarifications
- **95%+**: Manual review for edge cases

## Limitations

1. **Financial Complexity**: ~1190 fields in Finances sheet - full automation challenging
2. **Quarterly Phasing**: Budget breakdown by quarter requires detailed financial model
3. **Benefit Quantification**: Requires business case rigor (not just identification)
4. **Risk Register**: Comprehensive risk assessment typically needs workshops
5. **Multi-Year Data**: Historical and future projections need finance team input

**Recommendation**: Expect 2-3 rounds of clarification for complete ICC template

## Future Enhancements

1. **Financial Wizard**: Step-by-step guided prompts for complex financial section
2. **Benefit Calculator**: Help quantify benefits based on project type
3. **Risk Library**: Pre-populated risk templates by domain (regulatory, tech, etc.)
4. **Milestone Auto-Generation**: Generate milestones from project plan
5. **Cascade Updates**: When ITC changes, offer to update ICC template

---

**Last Updated**: 2025-01-08
**Version**: 1.0
**Supports Template**: ICC Business Case Template 2025
**Requires**: ITC approval (strongly recommended)
