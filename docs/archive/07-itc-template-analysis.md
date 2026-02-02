# ITC Project Template Analysis

## Overview

The ITC (Investment Technology Committee) Project Template is a comprehensive Excel workbook used for project governance at ICBC Standard Bank. It requires detailed information across multiple dimensions before presenting to the committee.

## Template Structure

### Sheets

1. **ITC Project Proposal** (Main sheet) - 102 fields
2. **Scope Elements** - 51 fields
3. **Estimates** - 199 fields
4. **Sheet2** - 6 fields (appears to be reference data)

## Section 1: Project Problem Statement

**Fields to populate:**
- **D4**: Project Name (e.g., "Business case for Energy VaR Migration")
- **E6**: Submitting Business Function
- **E7**: Business Sponsor
- **E8**: IT ExCo Sponsor
- **E9**: Submission Date
- **E11**: Background & Problem Statement (multi-line text field)

**Readiness Assessment:**
- E22: Immediately
- E23: Within 6mths
- E24: 6mths --> 1 year
- E25: 1 year plus

## Section 2: Project Benefits / Costs / Duration

**Benefit Themes** (Mark with X in column E, provide values in column H):

| Row | Benefit Theme | Column E | Value Column H |
|-----|---------------|----------|----------------|
| 28 | Revenue generation | Mark X | Revenue Benefit = £ |
| 29 | Non-FTE Cost Reduction | Mark X | Non FTE Cost Benefit = £ |
| 30 | FTE Cost Reduction | Mark X | FTE Cost Benefit = £ |
| 31 | Regulatory | Mark X | Reg Benefit = description |
| 32 | Capital & Liquidity Cost Avoidance | Mark X | Capital/Liquidity Benefit = £ |
| 33 | Control | Mark X | Control Benefit = description |
| 34 | Improve capability | Mark X | Capability Benefit = description |
| 35 | SLA Termination | Mark X | SLA Benefit = £ |
| 36 | Revenue Protection | Mark X | Revenue Protection Benefit = £ |
| 37 | Other | Mark X | Other Benefit = description |

**Business Unit Beneficiary** (rows 40-44):
- E40: Front Office (mark X), G40: How?
- E41: Finance (mark X), G41: How?
- E42: Risk Management (mark X), G42: How?
- E43: Compliance / Legal (mark X), G43: How?
- E44: Operations (mark X), G44: How?

## Scope Elements Sheet

**Columns:**
- A: High-Level Scope (requirement description)
- B: Scope Understood (Yes/No)
- C: BRD & Design (Yes/No)
- D: Enhancement? (Yes/No/Like for Like)
- E: Sponsorship (business area)
- F: Why (rationale)
- G: Quantifiable Benefits
- H: Resources Needed

**Requirements captured:**
- R01: Full revaluation of Murex Energy trades
- R02: Decommission redundant QP and Vespa processes
- R03: Vespa process and reporting changes
- R04: Time series smoothing & date roll methodology on Xeno
- R05: Time series smoothing & date roll methodology on FMDM
- R06: Volatility surface conversion
- R07: Full revaluation of RightAngle Energy

## Estimates Sheet

**Columns:**
- B: Task/Activity Description
- C: Dependencies
- D: Duration
- E: Start Date
- F: Finish Date
- G: Who (owner/resource)
- H: Notes

**Major workstreams:**
1. Trading - Vol Surface changes (tasks 1.1-1.5)
2. Market Risk - Vol Surface Timeseries (tasks 2.1-2.3)
3. Additional detailed tasks with dependencies

## Data Sources for Population

### From Meeting Minutes
- Project background and problem statement
- Key decisions
- Stakeholders identified (sponsors, owners)
- Timeline discussions
- Resource requirements

### From Project Planning
- Scope elements
- Requirements
- Dependencies
- Resource allocation
- Timeline/milestones

### From Benefit Analysis/Business Case
- Benefit themes
- Quantifiable benefits
- Cost estimates
- FTE impacts

### From Technical Assessment
- System changes required
- Dependencies
- Technical resources needed
- Duration estimates

## Population Strategy

### Phase 1: Basic Information
1. Extract from meeting minutes:
   - Project name/title
   - Business sponsor
   - Key stakeholders
   - Problem statement
   - Timeline readiness

2. Extract from discussions:
   - Benefit themes (which ones apply)
   - Business units impacted
   - High-level scope

### Phase 2: Detailed Scope
1. From requirements/scope documents:
   - Scope Elements sheet population
   - Each requirement with:
     - Understanding level
     - Enhancement vs like-for-like
     - Sponsorship
     - Rationale
     - Benefits
     - Resources

### Phase 3: Estimates
1. From project plan/work breakdown:
   - Task list
   - Dependencies
   - Durations
   - Owners
   - Start/finish dates
   - Notes/assumptions

### Phase 4: Benefits Quantification
1. From business case:
   - Revenue impacts (£)
   - Cost savings (£)
   - FTE reductions (#)
   - Regulatory/control benefits (description)
   - Capability improvements (description)

## Skill Design Approach

The skill should:

1. **Accept inputs:**
   - Project name
   - Meeting minutes content
   - Project plan/scope document
   - Business case information
   - Existing template path
   - Output path

2. **Process:**
   - Parse input documents
   - Extract relevant information
   - Map to template fields
   - Identify gaps (fields that couldn't be populated)
   - Generate populated template

3. **Output:**
   - Populated Excel file
   - Gap analysis report (what's missing)
   - Confidence scores per section
   - Recommendations for manual completion

## Implementation Considerations

### Technical Requirements
- **openpyxl**: Excel manipulation
- **pandas**: Data handling
- **python-docx**: Word document parsing (if needed)
- Template preservation (formatting, formulas, data validation)

### Intelligent Extraction
- NLP-based extraction from meeting minutes
- Pattern matching for dates, names, amounts
- Context-aware field mapping
- Confidence scoring for extractions

### Gap Handling
- Clear identification of missing fields
- Suggestions based on similar projects
- Required vs optional field distinction
- Validation rules from template

## Next Steps

1. Create `project-template-filler` skill
2. Define extraction patterns
3. Implement Excel manipulation logic
4. Add validation and gap analysis
5. Test with Energy VaR project data

---

*Analysis Date: 2025-01-05*
*Template: ITC Project Template.xlsx*
