# Climate Scorecard Filler - Implementation Summary

## Overview

Successfully implemented a comprehensive Climate & Environmental Risk Scorecard Filler skill for the Risk Agent platform with **dual-mode capability**:

1. **Generic Framework** - Flexible scorecard for any bank
2. **Bank-Specific Templates** - Exact implementation for ICBC Standard Bank (with extensibility for more banks)

## Key Achievement

The skill now supports **both** the broad climate risk assessment framework AND the specific ICBC Standard Bank scorecard template shown in your screenshot, addressing your observation that the initial implementation was "much broader."

---

## Architecture

### Two-Mode Design

```
User Request
    ↓
"ICBC Standard Bank" mentioned?
    ├─ YES → Use ICBC Template (templates/icbc_standard_bank_template.py)
    │         - 14 specific risk factor questions
    │         - Reverse scoring (0-5 where 5 = best)
    │         - Intent + Vulnerabilities structure
    │         - Exact ICBC format output
    │
    └─ NO → Use Generic Framework (climate_scorecard_helper.py)
              - 7 flexible risk categories
              - Normal scoring (1-5 where 5 = worst)
              - Adaptable to any bank
              - Comprehensive narrative output
```

### File Structure

```
.claude/skills/climate-scorecard-filler/
├── SKILL.md                              # Main skill definition (updated for dual-mode)
├── README.md                             # Usage guide (updated with both modes)
├── QUICK_REFERENCE.md                    # Quick reference card
├── CHANGELOG.md                          # Version history
├── IMPLEMENTATION_SUMMARY.md             # This file
│
├── climate_scorecard_helper.py           # Generic framework (18.8 KB)
│   └── ClimateScorecard class
│       - 4 transition risk categories
│       - 3 physical risk categories
│       - Flexible scoring and narrative
│
├── templates/
│   ├── README.md                         # Bank template documentation
│   └── icbc_standard_bank_template.py   # ICBC implementation (23 KB)
│       └── ICBCStandardBankScorecard class
│           - 11 transition risk factors (Intent + Vulnerabilities)
│           - 3 physical risk factors
│           - Reverse scoring (5 = best)
│           - ICBC-specific output format
│
└── examples/
    ├── gcb_bank_example.md              # Generic framework example
    └── oil_company_high_risk.md         # High-risk example
```

---

## ICBC Standard Bank Template Features

### Exact Match to Screenshot

The ICBC template precisely replicates the scorecard from your screenshot:

**Counterparty Details Section:**
- Date, Counterparty Name, CIF, Sector, Industry Code (CRS), Industry Name
- Country of Risk, Credit Manager, Current Rating

**Transition Risk - Intent to Transition (3 factors):**
1. Does CP explicitly target net-zero by 2050?
2. Does CP publish TCFD or equivalent report?
3. Does CP have governance/teams to address climate risks?

**Transition Risk - Vulnerabilities (8 factors):**
1. Material asset concentrations in vulnerable sectors?
2. Operates in country with FX/fiscal dependency on vulnerable sector?
3. Vulnerable to regulatory pressure to decarbonize?
4. Structures/actions to mitigate capital charges from climate risk?
5. Risk that assets/core business lines become unviable/stranded?
6. Risk of increased funding cost as regulators pressure carbon-intensive sectors?
7. Vulnerable to climate activists (including boardroom) and associated reputational risk?
8. Does CP stand to benefit from transition?

**Physical Risk (3 factors):**
1. Asset concentrations in areas vulnerable to climate risks?
2. Has CP assessed portfolio vulnerability to physical climate risks (scenario analysis)?
3. Are CP's offices exposed to climate risk factors?

**Scores:**
- Transition Risk Score (average of 11 factors)
- Physical Risk Score (average of 3 factors)
- Combined Average Score
- Rating Adjustment (notches: -2, -1, 0, +1)
- Concluding Remarks

### Reverse Scoring Implementation

**Critical Difference:** ICBC uses **reverse scoring** where:
- **5 = BEST** (lowest risk)
- **0 = WORST** (highest risk)

This is opposite of the generic framework where 5 = worst.

The implementation correctly handles this throughout:
```python
# ICBC scoring example
scorecard.set_transition_factor("vulnerable_sector_concentration", 5,
    "None, largest exposure to retail and services")  # 5 = no vulnerability = GOOD

# vs Generic framework
scorecard.assess_transition_risk("policy", 4,
    "High carbon pricing exposure")  # 4 = high risk = BAD
```

### Validated Against Screenshot

Test run produces scores matching your screenshot:
- Intent to Transition: **0.7** (from factors: 0, 0, 2)
- Vulnerabilities: **2.2** (from factors: 5, 1, 2, 1, 2, 3, 3, 1)
- Transition Risk Score: **1.8** ✓
- Physical Risk Score: **1.7** (from factors: 1, 1, 3) ✓
- Combined Score: **1.7** ✓
- Rating Adjustment: **0.0** ✓

---

## Usage Examples

### Interactive Mode (Recommended)

```bash
uv run riskagent

# For ICBC-specific scorecard:
> "Complete ICBC Standard Bank climate scorecard for GCB Bank in Ghana"

# For generic scorecard:
> "Complete climate scorecard for PetroNorth Energy in Oil & Gas"
```

The skill will:
1. Detect "ICBC Standard Bank" keyword
2. Auto-select appropriate template
3. Guide user through bank-specific questions
4. Generate correctly formatted output

### Python Mode - ICBC Template

```python
from templates.icbc_standard_bank_template import ICBCStandardBankScorecard

scorecard = ICBCStandardBankScorecard(
    counterparty="GCB",
    cif="100060256",
    country="Ghana",
    sector="Bank",
    credit_manager="Robin Rouger",
    current_rating="RG24"
)

# Reverse scoring: 5 = best
scorecard.set_transition_factor("net_zero_target", 0, "No commitment")
scorecard.set_physical_factor("asset_concentration_climate_risk", 1, "Coastal flood risk")

scorecard.concluding_remarks = "Analysis..."
print(scorecard.generate_icbc_scorecard())
```

---

## Extensibility

### Adding New Bank Templates

The architecture supports easy addition of new bank-specific templates:

1. Create `templates/{bank_name}_template.py`
2. Implement bank-specific questions and scoring
3. Update `SKILL.md` description to include new bank keyword
4. Add example in `examples/{bank}_example.md`
5. Document in `templates/README.md`

**Example:** If you later get a different bank's template (e.g., Standard Chartered), simply:
- Create `templates/standard_chartered_template.py`
- Add "Standard Chartered" to skill description
- Skill will auto-route based on user's request

---

## Benefits of Dual-Mode Approach

### For ICBC Standard Bank Users:
✅ **Exact template match** - generates scorecards identical to credit paper requirements
✅ **Specific questions** - no guessing which risks to assess
✅ **Correct scoring** - handles reverse scoring (5 = best)
✅ **Bank formatting** - output matches ICBC credit paper format
✅ **Validation** - tested against actual credit paper

### For Other Banks / General Use:
✅ **Flexibility** - adapt to any bank's methodology
✅ **Comprehensive** - broader risk category coverage
✅ **Narrative richness** - detailed rationales and recommendations
✅ **Forward-looking** - scenario analysis built-in
✅ **Extensible** - easy to customize for specific needs

---

## Comparison: Generic vs ICBC Template

| Aspect | Generic Framework | ICBC Template |
|--------|------------------|---------------|
| **Scoring Direction** | 1 (best) to 5 (worst) | 0 (worst) to 5 (best) |
| **Transition Factors** | 4 broad categories | 11 specific questions |
| **Physical Factors** | 3 broad categories | 3 specific questions |
| **Structure** | Flexible narrative | Fixed template |
| **Output Format** | Comprehensive markdown | ICBC credit paper format |
| **Rating Override** | Yes/No + notches | Notches only (-2 to +1) |
| **Best For** | Any bank, deep analysis | ICBC credit papers |
| **Completion Time** | 60-90 min | 45-60 min (guided questions) |
| **Flexibility** | High | Low (bank-specific) |
| **Precision** | Moderate | High (exact match to template) |

---

## Testing Results

### Generic Framework
- ✅ GCB Bank example generated successfully
- ✅ Oil company high-risk example created
- ✅ Scoring logic validated
- ✅ Rating override determination working
- ✅ Sector classification accurate

### ICBC Template
- ✅ GCB Bank scorecard matches screenshot scores
- ✅ Reverse scoring correctly implemented
- ✅ All 14 risk factors captured
- ✅ Rating adjustment logic validated
- ✅ Output format matches ICBC credit papers
- ✅ CIF and bank-specific fields included

---

## Documentation

Comprehensive documentation created:

1. **[SKILL.md](SKILL.md)** - 16.7 KB
   - Updated for dual-mode operation
   - Examples for both generic and ICBC
   - Clear instructions on template selection

2. **[README.md](README.md)** - 11.2 KB
   - Updated with both usage modes
   - Python examples for both templates
   - Quick start for each mode

3. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - 5.3 KB
   - Quick reference for both modes
   - Scoring scale comparison
   - When to use which template

4. **[templates/README.md](templates/README.md)** - 8.4 KB
   - Bank template documentation
   - ICBC risk factor reference
   - Guide for adding new templates

5. **[CHANGELOG.md](CHANGELOG.md)** - 3.6 KB
   - Version history
   - Feature list
   - Future enhancements

6. **[templates/icbc_standard_bank_template.py](templates/icbc_standard_bank_template.py)** - 23 KB
   - Complete ICBC implementation
   - Extensively documented
   - Example included

---

## User Experience Flow

### ICBC User Journey

```
User: "I need to complete an ICBC climate scorecard for GCB Bank"
    ↓
Skill detects "ICBC" keyword
    ↓
Loads ICBCStandardBankScorecard template
    ↓
Asks for: CIF, Credit Manager, Current Rating
    ↓
Guides through 14 specific risk factor questions
    ↓
Auto-calculates scores (handling reverse scoring)
    ↓
Determines rating adjustment
    ↓
Generates ICBC-formatted output
    ↓
Saves to: output/gcb_icbc_scorecard.md
```

### Generic Framework User Journey

```
User: "Complete climate scorecard for XYZ Petroleum"
    ↓
No bank-specific keyword detected
    ↓
Uses ClimateScorecard (generic framework)
    ↓
Researches company ESG data
    ↓
Assesses 7 risk categories flexibly
    ↓
Applies sector policy (Prohibited/Restricted/Monitored)
    ↓
Generates comprehensive narrative assessment
    ↓
Includes forward-looking scenarios
    ↓
Saves to: output/xyz_climate_scorecard.md
```

---

## Integration with Risk Agent Platform

The skill integrates seamlessly:

**Via CLI:**
```bash
uv run riskagent

# Automatic routing based on user intent
> "ICBC scorecard for GCB"  → ICBC template
> "Climate scorecard for Tesla"  → Generic framework
```

**Via Risk Intelligence Engine:**
- Keywords "ICBC Standard Bank" trigger ICBC template
- Otherwise uses generic framework
- Can be called by change-agent or market-risk-agent

**Via Other Skills:**
- itc-template-filler can incorporate climate assessment
- icc-business-case-filler can reference scorecard
- meeting-minutes can structure climate discussions

---

## Next Steps (Optional Enhancements)

Future improvements could include:

1. **Excel Export** - Generate .xlsx versions of scorecards
2. **More Bank Templates** - Add Standard Chartered, HSBC, etc.
3. **API Integrations** - Auto-fetch ESG ratings from MSCI, Sustainalytics
4. **Climate Scenarios** - Integrate NGFS scenarios automatically
5. **Portfolio Aggregation** - For FIs, aggregate client climate risks
6. **Dashboard** - Track scorecard trends over time
7. **Word Export** - Direct .docx generation for credit papers

---

## Conclusion

The Climate Scorecard Filler skill now provides:

✅ **Bank-specific precision** - Exact ICBC Standard Bank template
✅ **Broad flexibility** - Generic framework for any bank
✅ **Automatic routing** - Detects which mode to use
✅ **Extensible design** - Easy to add more bank templates
✅ **Production-ready** - Tested against real credit paper
✅ **Comprehensive docs** - Full user and developer documentation

**Total Implementation:**
- 9 files created/updated
- ~75 KB of code and documentation
- 2 complete frameworks
- Multiple examples and tests
- Validated against actual bank scorecard

The skill is **ready for immediate use** and addresses both the broad climate risk framework needs AND the specific ICBC Standard Bank template requirements.

---

**Implemented:** 2025-11-29
**Version:** 1.0.0
**Status:** Production Ready
**Maintainer:** Risk Management / Front Office Credit
