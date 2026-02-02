# Bank-Specific Climate Scorecard Templates

This directory contains bank-specific implementations of climate risk scorecards. Each template follows the exact format, questions, and scoring methodology used by that bank.

## Available Templates

### 1. ICBC Standard Bank Template

**File:** [`icbc_standard_bank_template.py`](icbc_standard_bank_template.py)

**Scoring Method:** Reverse scoring (0-5 where **5 = best**/lowest risk)

**Structure:**
- **Counterparty Details** (CIF, Sector, Industry Code, Credit Manager, Current Rating)
- **Transition Risk Assessment** (11 specific risk factors)
  - Intent to Transition (3 factors): Net-zero target, TCFD reporting, Governance
  - Vulnerabilities (8 factors): Sector concentration, Country dependency, Regulatory pressure, etc.
- **Physical Risk Assessment** (3 specific risk factors)
  - Asset concentration in vulnerable areas
  - Scenario analysis capability
  - Office exposure
- **Combined Assessment** (average of transition and physical)
- **Rating Adjustment** (-2, -1, 0, +1 notches)
- **Concluding Remarks**

**Key Differences from Generic Framework:**
- Reverse scoring (5 = best vs generic 5 = worst)
- Specific risk factor questions vs flexible categories
- Two-tier transition risk (Intent + Vulnerabilities)
- Simpler physical risk assessment (3 factors vs 3 categories)
- Rating adjustment in notches (-2 to +1)

**Usage:**
```python
from templates.icbc_standard_bank_template import ICBCStandardBankScorecard

scorecard = ICBCStandardBankScorecard(
    counterparty="GCB",
    cif="100060256",
    country="Ghana",
    sector="Bank",
    industry_code_crs="64194",
    industry_name="General Banks",
    credit_manager="Robin Rouger",
    current_rating="RG24"
)

# Set transition factors (note: 5 = best)
scorecard.set_transition_factor("net_zero_target", 0, "No net-zero commitment")
scorecard.set_transition_factor("tcfd_reporting", 0, "No TCFD report")
scorecard.set_transition_factor("governance_teams", 2, "ESG committee in place")

# Set physical factors
scorecard.set_physical_factor("asset_concentration_climate_risk", 1, "Ghana coastal flooding risk")

# Generate scorecard
scorecard.concluding_remarks = "Your analysis here..."
print(scorecard.generate_icbc_scorecard())
```

**Output Example:** See [`../examples/gcb_bank_example.md`](../examples/gcb_bank_example.md) (generic) vs `output/gcb_icbc_scorecard.md` (ICBC-specific)

---

## When to Use Which Template

### Use ICBC Standard Bank Template When:
- User explicitly mentions "ICBC Standard Bank" or "ICBC scorecard"
- Credit paper is for ICBC Standard Bank Plc submission
- User provides CIF number (Customer Identification Number)
- User asks about specific ICBC risk factors (e.g., "Does CP target net-zero by 2050?")

### Use Generic Framework When:
- User doesn't specify a bank
- User wants flexible scoring approach
- Bank-specific template not available
- User requests "generic climate scorecard"

---

## Scoring Comparison

| Aspect | Generic Framework | ICBC Template |
|--------|------------------|---------------|
| **Scoring Direction** | 1 = best, 5 = worst | 0 = worst, 5 = best |
| **Transition Risk Factors** | 4 broad categories | 11 specific questions |
| **Physical Risk Factors** | 3 broad categories | 3 specific questions |
| **Rating Override** | Yes/No + notches | Notches (-2 to +1) |
| **Flexibility** | High - adapt questions | Low - fixed questions |
| **Use Case** | Any bank, any sector | ICBC credit papers |

---

## ICBC Template Risk Factors Reference

### Transition Risk - Intent to Transition (3 factors)

| Question | Score 5 (Best) | Score 0 (Worst) |
|----------|----------------|-----------------|
| Does CP explicitly target net-zero by 2050? | Yes with credible plan | No commitment |
| Does CP publish TCFD or equivalent? | Comprehensive TCFD | No disclosure |
| Does CP have governance/teams for climate risk? | Dedicated function, board oversight | No governance |

### Transition Risk - Vulnerabilities (8 factors)

| Question | Score 5 (Best) | Score 0 (Worst) |
|----------|----------------|-----------------|
| Material asset concentrations in vulnerable sectors? | None | High concentration |
| Operates in country with FX/fiscal dependency on vulnerable sector? | No dependency | High dependency |
| Vulnerable to regulatory decarbonization pressure? | Not vulnerable | Highly vulnerable |
| Structures/actions to mitigate capital charges? | Comprehensive plan | No plan |
| Risk assets/business lines become unviable/stranded? | No risk | High stranding risk |
| Risk of increased funding cost from carbon intensity? | No risk | High funding risk |
| Vulnerable to climate activists/litigation? | No vulnerability | Active litigation |
| Stand to benefit from transition? | Yes, well-positioned | No benefit |

### Physical Risk (3 factors)

| Question | Score 5 (Best) | Score 0 (Worst) |
|----------|----------------|-----------------|
| Asset concentrations in climate-vulnerable areas? | None | High concentration |
| Assessed portfolio vulnerability via scenario analysis? | Comprehensive analysis | No analysis |
| Offices exposed to climate risk factors? | Not exposed | Highly exposed |

---

## Rating Adjustment Guidance (ICBC)

Based on Combined Average Score (reverse scoring: higher = better):

| Combined Score | Rating Adjustment | Rationale |
|----------------|-------------------|-----------|
| **< 1.5** | -1 to -2 notches | Very high climate risk; material credit deterioration likely |
| **1.5 - 2.5** | -1 notch (if sensitive sector) | High climate risk; downgrade for Oil & Gas, Mining, etc. |
| **2.5 - 3.5** | Monitor, possible -0.5 | Moderate climate risk; close monitoring required |
| **> 3.5** | 0.0 (no adjustment) | Low climate risk; no adjustment typically |
| **Prohibited Sector** | -2 notches + DECLINE | Automatic downgrade regardless of score |

**Notation:** "If positive = -1, if neutral = -0, if negative = +1"
- This means: -1 = downgrade by 1 notch (e.g., RG16 → RG17)
- 0 = no change
- +1 = upgrade by 1 notch (rare for climate risk)

---

## Adding New Bank Templates

To add a template for a new bank:

1. **Create new Python file** in this directory: `{bank_name}_template.py`

2. **Implement bank-specific class:**
   ```python
   from dataclasses import dataclass

   @dataclass
   class YourBankScorecard:
       # Bank-specific fields
       counterparty: str
       # ... other required fields

       def set_risk_factor(self, factor: str, score: int, rationale: str):
           # Custom scoring logic
           pass

       def calculate_scores(self):
           # Bank-specific calculation
           pass

       def generate_scorecard(self) -> str:
           # Generate bank-formatted output
           pass
   ```

3. **Update SKILL.md** to include new template in description and examples

4. **Add example** in `../examples/{bank_name}_example.md`

5. **Test** with real credit paper data if available

6. **Document** in this README

---

## Template File Structure

Each bank template should include:

```python
# Module docstring explaining the bank and format
"""
{Bank Name} Climate & Environmental Risk Scorecard Template

This module implements the specific scorecard template used by {Bank Name}
...
"""

# Imports
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Main scorecard class
@dataclass
class BankNameScorecard:
    # Required fields
    counterparty: str
    country: str
    sector: str
    # ... bank-specific fields

    # Risk factor fields
    # ... specific to bank template

    # Methods
    def set_risk_factor(self, ...):
        """Set individual risk factor scores"""
        pass

    def calculate_scores(self):
        """Calculate section and overall scores"""
        pass

    def generate_scorecard(self) -> str:
        """Generate formatted scorecard output"""
        pass

    def to_dict(self) -> Dict:
        """Export as dictionary for JSON/Excel"""
        pass

# Example usage function
def example_scorecard():
    """Example demonstrating template usage"""
    pass

# Main execution for testing
if __name__ == "__main__":
    example = example_scorecard()
    print(example.generate_scorecard())
```

---

## Testing Templates

Test each template with:

```bash
# Run template example
python templates/{bank_name}_template.py

# Check output
cat output/{counterparty}_{bank}_scorecard.md

# Verify scores match expected values
# Compare to actual credit paper if available
```

---

## Maintenance

**Version Control:**
- Each template should track bank policy version (e.g., "Environmental Risk Policy v4.0")
- Update templates when bank changes scorecard format or questions
- Maintain backward compatibility or version templates separately

**Quality Checks:**
- Verify scoring direction (normal vs reverse)
- Confirm all bank-specific fields are captured
- Test rating adjustment logic
- Validate output format matches bank credit paper templates

---

## Support

For questions about:
- **Generic framework**: See [`../README.md`](../README.md)
- **SKILL usage**: See [`../SKILL.md`](../SKILL.md)
- **Adding templates**: Contact Risk Management or see this README
- **ICBC specifics**: Refer to Environmental Risk Policy v4.0

---

**Last Updated:** 2025-11-29
**Templates Available:** 1 (ICBC Standard Bank)
**Maintained By:** Risk Management / Front Office Credit
