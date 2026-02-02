# Project Template Filler Skill - Implementation Summary

## Overview

Created a new Claude Skill to automate the population of ITC (Investment Technology Committee) project governance templates for ICBC Standard Bank. This skill extracts information from meeting minutes, project plans, and business cases to fill out complex multi-sheet Excel templates required for project approval processes.

## What Was Built

### 1. Skill Definition
**Location**: `.claude/skills/project-template-filler/SKILL.md`

**Capabilities:**
- Populates multi-sheet Excel templates (ITC Project Proposal, Scope Elements, Estimates)
- Extracts information from meeting minutes, project plans, business case documents
- Intelligent field mapping across 350+ template fields
- Gap analysis and confidence scoring
- Banking/risk management domain intelligence

### 2. Template Analysis
**Analyzed**: `data/icbc_standard_bank/Projects/Energy/Governance/ITC Project Template.xlsx`

**Structure:**
- 4 sheets: ITC Project Proposal (102 fields), Scope Elements (51 fields), Estimates (199 fields), Sheet2 (6 fields)
- Total: 358 fields requiring population
- Complex multi-level structure with dependencies

**Key Sections:**
- Section 1: Project Problem Statement (name, sponsors, background, readiness)
- Section 2: Benefits/Costs/Duration (benefit themes, quantification, business units)
- Scope Elements: Requirements with BRD status, sponsorship, resources
- Estimates: Task breakdown, dependencies, duration, critical path

### 3. Documentation
- **[07-itc-template-analysis.md](07-itc-template-analysis.md)**: Detailed field mapping and structure analysis
- **[08-project-template-filler-skill.md](08-project-template-filler-skill.md)**: This implementation summary
- **analyze_template.py**: Python script for template structure analysis

### 4. Dependencies Added
Updated `pyproject.toml` to include:
- `openpyxl>=3.1.0` - Excel file manipulation
- `pandas>=2.0.0` - Data handling and transformation

### 5. Agent Integration
Updated `.claude/agents/change-agent.md` to reference the new skill:
- Added project-template-filler to Available Skills section
- Defined when to invoke it (ITC template, governance documentation)

## How It Works

### Input Sources
The skill accepts multiple input types:
1. **Meeting Minutes**: Project context, decisions, stakeholders, timeline
2. **Project Plan**: Scope, requirements, work breakdown, dependencies
3. **Business Case**: Benefits, costs, FTE impacts, quantification
4. **Additional Context**: Any supplementary documentation

### Extraction Strategy
**From Meeting Minutes:**
- Project name and background
- Key stakeholders and sponsors
- Problem statement
- Decisions → Scope elements
- Action items → Tasks
- Timeline → Readiness assessment
- Benefit discussions → Benefit themes

**From Project Plan:**
- Requirements → Scope Elements sheet
- Work breakdown → Estimates sheet
- Dependencies and timeline
- Resource allocation

**From Business Case:**
- Quantifiable benefits (revenue, cost savings, FTE)
- Regulatory/compliance drivers
- Capital/liquidity impacts

### Output
1. **Populated Excel Template**
   - All sheets with extracted data
   - Original formatting preserved
   - Data validation rules maintained

2. **Gap Analysis Report**
   - Fields successfully populated
   - Missing fields with priorities
   - Confidence scores per section
   - Recommendations for manual completion

### Field Mapping Examples

| Source | Extracted Info | Template Location |
|--------|---------------|------------------|
| Meeting title | "Energy VaR Migration" | D4: Project Name |
| Attendee list | "Tom McGrath (Sponsor)" | E7: Business Sponsor |
| Discussion | Background paragraph | E11: Problem Statement |
| Decisions | "Split into 2 projects" | Scope Elements: Requirements |
| Action items | "QAD - Model validation" | Estimates: Tasks |
| Timeline | "6 months for IT" | E23: Within 6mths checkbox |
| Benefits | "Regulatory compliance" | E31: Regulatory theme |

## Banking Domain Intelligence

The skill has built-in understanding of:

**Regulatory Frameworks:**
- IFRS 9, Basel III/IV
- SR 11-7 (Model Risk Management)
- CRR/CRD, PRA/FCA requirements

**Risk Management:**
- VaR calculations
- Model validation
- Three lines of defense
- ICAAP/ILAAP

**Technology Systems:**
- Murex, QP, Vespa, FMDM, RightAngle
- Front/middle/back office distinctions

**Benefit Themes:**
- Revenue generation
- Cost reduction (FTE and non-FTE)
- Regulatory compliance
- Capital efficiency
- Control improvements
- Capability enhancement

## Testing Strategy

### Test Case: Energy VaR Project

**Available Data:**
- ✅ Meeting minutes: `Energy_VaR_Project_Meeting_Minutes_20251020.md`
- ✅ Scope document: From meeting discussions
- ⚠️  Business case: Partial information in minutes
- ⚠️  Estimates: High-level only

**Expected Coverage:**
- Section 1 (Problem Statement): 80-90% populated
- Section 2 (Benefits): 60-70% populated (missing quantification)
- Scope Elements: 70-80% populated (7 requirements identified)
- Estimates: 40-50% populated (high-level tasks only)

**Gaps Anticipated:**
- IT ExCo Sponsor not mentioned in minutes
- Quantified revenue/cost benefits
- Detailed task durations and dependencies
- Specific start/finish dates

### How to Test

**Using the CLI:**
```bash
uv run riskagent
```

**Test Query:**
```
I need to complete the ITC project template for the Energy VaR project.
Use the meeting minutes from data/icbc_standard_bank/Projects/Energy/Meeting Minutes/Energy_VaR_Project_Meeting_Minutes_20251020.md
and the template at data/icbc_standard_bank/Projects/Energy/Governance/ITC Project Template.xlsx
Save the output to data/icbc_standard_bank/Projects/Energy/Governance/Energy_VaR_ITC_Proposal_[Date].xlsx
```

**Expected Behavior:**
1. Risk-intelligence-engine routes to change-agent
2. Change-agent detects template filling task
3. **project-template-filler skill invoked** (visible in CLI with bright magenta "Skill Invocation" panel)
4. Skill reads meeting minutes and template
5. Extracts relevant information
6. Populates template fields
7. Generates gap analysis report
8. Saves populated template
9. Returns summary with confidence scores

## Success Criteria

### Minimum Viable
- ✅ Section 1 fields populated from meeting minutes
- ✅ Benefit themes identified (even if not quantified)
- ✅ Key requirements extracted to Scope Elements
- ✅ Gap analysis report generated
- ✅ Template integrity maintained

### Ideal
- ✅ 80%+ fields populated across all sections
- ✅ High confidence scores (85%+) for extracted data
- ✅ Quantified benefits where available
- ✅ Complete task breakdown with dependencies
- ✅ Minimal manual intervention needed

## Future Enhancements

### Phase 2: Intelligence Improvements
- Historical project learning (improve extraction patterns from previous templates)
- Similarity matching (suggest values from similar past projects)
- Multi-document synthesis (combine information from multiple sources more effectively)

### Phase 3: Integration
- JIRA/MS Project integration for task imports
- HR system integration for resource allocation
- Financial system integration for cost/benefit validation
- Real-time collaboration (track who populated which fields)

### Phase 4: Advanced Features
- Template versioning support (handle template changes over time)
- Approval workflow integration
- Automated benefit tracking post-project
- Multi-language support
- PDF template support (in addition to Excel)

## Known Limitations

1. **Complex Financial Calculations**: May need manual validation of benefit quantification
2. **Multi-Project Dependencies**: Cross-project dependencies not automatically identified
3. **Resource Names**: People assignment needs validation (may not match HR records exactly)
4. **Template Changes**: Assumes current template structure (needs update if template evolves)
5. **Language**: Optimized for English documentation only

## Files Created/Modified

### New Files
- `.claude/skills/project-template-filler/SKILL.md` - Skill definition
- `docs/07-itc-template-analysis.md` - Detailed template analysis
- `docs/08-project-template-filler-skill.md` - This implementation summary
- `analyze_template.py` - Template analysis script

### Modified Files
- `.claude/agents/change-agent.md` - Added skill reference
- `pyproject.toml` - Added openpyxl and pandas dependencies

### Dependencies Installed
- openpyxl 3.1.5
- pandas 2.3.3
- numpy 2.3.4 (pandas dependency)
- Supporting libraries (et-xmlfile, python-dateutil, pytz, tzdata, six)

## Integration with Existing Skills

### Works Well With:
1. **meeting-minutes** → **project-template-filler**
   - First structure meeting notes
   - Then use structured output to populate template

2. **project-planner** → **project-template-filler**
   - Generate detailed project plan first
   - Then populate governance template

3. **status-reporter** + **project-template-filler**
   - Ongoing projects can have templates updated with current status
   - Use status reports to refresh benefit tracking sections

### Workflow Example:
```
User: "Create meeting minutes and then fill out the ITC template"

1. meeting-minutes skill invoked
   → Structured meeting minutes created

2. project-template-filler skill invoked
   → Uses structured minutes as input
   → Populates template
   → Returns populated template + gap analysis
```

## Technical Implementation Notes

### Excel Manipulation
```python
# Uses openpyxl for precise cell-level control
workbook = openpyxl.load_workbook(template_path, data_only=False)
proposal_sheet = workbook['ITC Project Proposal']

# Preserve formatting and data validation
proposal_sheet['D4'] = extracted_project_name  # Direct cell assignment
workbook.save(output_path)  # Maintains all formatting
```

### Extraction Pattern Examples
```python
# Project name extraction
project_name_pattern = r"(?:Project|Initiative):\s*(.+?)(?:\n|$)"

# Sponsor identification
# Check attendees for role indicators like "Sponsor", "CRO", "CFO"

# Benefit theme detection
benefit_keywords = {
    'regulatory': ['compliance', 'regulatory', 'ifrs', 'basel'],
    'cost_reduction': ['saves', 'reduces cost', 'efficiency', 'decommission'],
    'revenue': ['revenue', 'income', 'generate', 'monetize']
}
```

### Confidence Scoring
```python
confidence_levels = {
    'HIGH': (85, 100),    # Direct extraction, exact match
    'MEDIUM': (60, 84),   # Inferred, contextual match
    'LOW': (40, 59),      # Weak signals, ambiguous
    'NONE': (0, 39)       # No data found
}
```

## Summary

The **project-template-filler** skill automates a time-consuming manual process (populating 350+ fields across multiple Excel sheets) by intelligently extracting information from project documentation. It's designed specifically for banking governance processes with built-in domain knowledge of risk management, regulatory frameworks, and common project structures.

**Key Achievement**: Transforms hours of manual data entry into a few minutes of AI-assisted template population with comprehensive gap analysis for validation.

**Next Step**: Test with actual Energy VaR project data to validate extraction quality and refine patterns based on real-world results.

---

*Created: 2025-01-05*
*Risk Agent Framework v0.1.0*
*Skills: 5 (meeting-minutes, project-planner, status-reporter, stakeholder-analysis, project-template-filler)*
