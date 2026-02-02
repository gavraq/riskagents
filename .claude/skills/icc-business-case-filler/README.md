# ICC Business Case Filler Skill

Automates population of ICC (Investment & Change Committee) Business Case templates for banking governance processes.

**Governance Context**: ICC is the **second governance gate** in the project approval process. After ITC (Investment Technology Committee) approval establishes strategic alignment, ICC requires a comprehensive business case with detailed financials, resources, timelines, and risk management for final project funding approval.

## Quick Start

### As a Skill (Recommended)

The ICC Business Case Filler is automatically available when using the Risk Agent CLI:

```bash
$ uv run riskagent

You: Complete the ICC business case template for the Energy VaR project using the ITC template we created
```

The agent will automatically invoke the `icc-business-case-filler` skill.

### As a Standalone Script

You can also run the population script directly:

```bash
# Basic usage
uv run python .claude/skills/icc-business-case-filler/populate_icc_template.py \
  --template data/ICC_Template.xlsm \
  --output output/ICC_EnergyVaR_Populated.xlsm

# With ITC pre-population (recommended)
uv run python .claude/skills/icc-business-case-filler/populate_icc_template.py \
  --template data/ICC_Template.xlsm \
  --output output/ICC_EnergyVaR_Populated.xlsm \
  --itc-template data/ITC_EnergyVaR_Completed.xlsm \
  --clarification-output output/ICC_Clarifications.md

# Non-interactive mode (no clarification questions)
uv run python .claude/skills/icc-business-case-filler/populate_icc_template.py \
  --template data/ICC_Template.xlsm \
  --output output/ICC_Populated.xlsm \
  --no-interactive
```

## Key Feature: Interactive Clarification Mode

**Unlike one-shot template population**, this skill uses an **interactive clarification approach**:

### How It Works

1. **Initial Population** (40-60% complete):
   - Pre-populates from ITC template if provided (~30-40 fields)
   - Extracts from business case documents
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

### Example Output

```
✓ Pre-populated 35 fields from ITC template
✓ Extracted 12 fields from meeting minutes
⚠  47 fields populated (40% complete)
⚠  15 CRITICAL fields missing
⚠  23 HIGH priority fields missing

Generating clarification report...

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
```

## Template Structure

The ICC Business Case template contains **17 sheets** with approximately **2000+ fields**:

**Core Sheets:**
- **Project Summary**: Executive overview, key dates, total costs
- **Finances**: Detailed budget with quarterly phasing (~1190 fields!)
- **Milestones & Benefits**: Timeline and quantified benefits
- **RAIDs**: Risks, Assumptions, Issues, Dependencies
- **Business and Asset Class**: Business unit impact analysis
- **Technology Impact**: IT infrastructure changes
- **OPR Checklist**: Operational risk assessment
- **Dependencies**: Cross-project dependencies
- **Project Governance**: Governance structure
- ... and 8 more sheets

## ITC → ICC Pre-Population

If you provide a completed ITC template, the skill automatically copies relevant fields:

| ICC Field | ITC Source | Notes |
|-----------|------------|-------|
| Project Name | ITC D4 | Direct copy |
| Sponsor | ITC E7 | Direct copy |
| Problem Statement | ITC E11 | Base for expansion |
| Benefit Themes | ITC E28-E37 | **Must be quantified in ICC** |
| High-level Scope | ITC Scope Elements | **Must be expanded in ICC** |
| Timeline Estimates | ITC E48-E49 | **Must be detailed in ICC** |

**Typical ITC→ICC Pre-population**: 30-40 fields (~20% of template)

## Bundled Modules

### Shared Modules (Symlinked from itc-template-filler)

- **excel_helpers.py**: Safe Excel manipulation with merged cell handling
- **extraction_helpers.py**: Multi-source data extraction with confidence scoring

### ICC-Specific Modules

- **icc_field_mappings.py**: Field definitions with priorities, categories, clarification prompts
- **populate_icc_template.py**: Main population engine with interactive clarification

## Command-Line Options

```
--template PATH           Path to ICC Business Case template (required)
--output PATH            Output path for populated template (required)
--itc-template PATH      Path to populated ITC template (for pre-population)
--clarification-output   Path to save clarification report markdown file
--no-interactive         Disable interactive clarification mode
--quiet                  Suppress progress messages
```

## Use Cases

### Scenario 1: ITC-Approved Project Needs ICC

**Input:**
- Populated ITC template (from previous approval)
- Updated financial analysis with vendor quotes
- Resource allocation plan
- Risk register

**Process:**
1. Skill pre-populates 35 fields from ITC template
2. Skill extracts 12 additional fields from documents
3. Skill identifies 15 critical missing fields
4. Skill generates targeted clarification questions
5. User provides missing information
6. Skill completes template (85% populated)

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
1. Skill extracts ~40-50 fields from business case
2. Skill identifies 60+ missing fields
3. Skill generates extensive clarification report
4. User provides information in batches (Critical first)
5. Multiple rounds of clarification
6. Iterative completion over 2-3 sessions

**Output:**
- ICC template 70% complete after round 1
- 90% complete after round 2
- 95% complete after round 3

## Field Priority Levels

- 🔴 **CRITICAL**: Required for ICC approval (project start date, total cost, sponsor, PM)
- 🟡 **HIGH**: Strongly recommended (risk register, key milestones, FTE)
- 🟢 **MEDIUM**: Good to have (detailed benefit quantification, dependencies)
- ⚪ **LOW**: Optional (additional comments, supporting details)

## Integration with Risk Agent Workflow

**Typical Project Governance Flow:**

```
1. Early Stage → Use itc-template-filler skill
   ↓ ITC Approval ✓

2. Detailed Planning Phase (3-6 months)
   - Develop detailed financials
   - Secure resource commitments
   - Complete risk assessment
   - Get vendor quotes
   ↓

3. ICC Preparation → Use icc-business-case-filler skill
   - Pre-populate from ITC template
   - Add detailed financial info
   - Interactive clarification for gaps
   - Iterative completion
   ↓ ICC Approval ✓

4. Project Execution
```

## Technical Requirements

- Python 3.11+
- openpyxl package (for Excel manipulation)
- pathlib, datetime (standard library)

All dependencies are managed via `pyproject.toml` when using the Risk Agent CLI.

## Related Documentation

- **[SKILL.md](./SKILL.md)** - Complete skill reference with field mappings and clarification system details
- **[ITC Template Filler Reference](../../../docs/06b-itc-template-filler-reference.md)** - Reference for the first governance gate
- **[Skills Guide](../../../docs/06-skills-guide.md)** - General skills framework documentation
- **[ICC Implementation Plan](../../../docs/icc-business-case-skill-plan.md)** - Original implementation plan and design

## Support

For issues or questions:
1. Check the [Skills Guide Troubleshooting](../../../docs/06-skills-guide.md#troubleshooting) section
2. Review the [ICC Implementation Plan](../../../docs/icc-business-case-skill-plan.md) for design rationale
3. Examine the SKILL.md for detailed field mappings

---

**Version**: 1.0
**Last Updated**: 2025-01-08
**Supports Template**: ICC Business Case Template 2025
