## Climate & Environmental Risk Scorecard Filler

### Overview
This skill assists Front Office teams in completing Climate & Environmental Risk Scorecards (Appendix E) for credit applications and annual reviews. It evaluates counterparty exposure to climate-related physical and transition risks, and determines if credit rating adjustments are warranted.

**Two Modes Available:**
1. **Enhanced Generic Framework** - Flexible scorecard with structured assessment (default)
   - Incorporates ICBC template learnings
   - Separates transition preparedness, vulnerability, and opportunity
   - Includes country-level sovereign risk assessment
   - 17 specific assessment factors
2. **Bank-Specific Templates** - Exact format for specific banks (currently: ICBC Standard Bank)

When you specify a bank name (e.g., "ICBC Standard Bank scorecard"), the skill automatically uses that bank's specific template with their exact risk factor questions and scoring methodology. Otherwise, it uses the enhanced generic framework.

### When to Use
- **Credit Applications**: New credit limit requests requiring environmental risk assessment
- **Annual Reviews**: Updating climate risk scorecards for existing counterparties
- **ESG Onboarding**: Initial environmental risk evaluation for new relationships
- **Credit Committee Submissions**: Preparing Appendix E documentation
- **Sensitive Sectors**: Evaluating counterparties in Energy, Mining, Industrials, or Agriculture

### Quick Start

#### Option 1: Interactive Completion (Recommended)
```bash
# From the Risk Agent CLI
uv run riskagent

# Then ask:
"Complete climate scorecard for [Counterparty Name] in [Sector]"
"I need help with a climate risk assessment for our credit paper"
"Complete ICBC Standard Bank climate scorecard for GCB Bank"  # Bank-specific
"Fill out ICBC scorecard for this counterparty"  # Bank-specific shorthand
```

#### Option 2: Python Script - Enhanced Generic Framework
```python
from climate_scorecard_helper import EnhancedClimateScorecard

# Create scorecard
scorecard = EnhancedClimateScorecard(
    counterparty="ABC Corporation",
    country="United Kingdom",
    sector="Oil and Gas",
    prepared_by="Front Office Credit Team"
)

# Assess transition preparedness (1-5 where 5 = worst/none)
scorecard.assess_transition_preparedness(
    net_zero_target=4,              # Weak/aspirational target
    tcfd_disclosure=3,              # Basic TCFD report
    governance_structure=3,         # Board committee exists
    transition_plan=4,              # Limited credibility
    capex_alignment=5,              # Misaligned - expanding production
    rationale="Limited climate governance; plans not aligned with Paris",
    sources=["ABC Annual Report 2024", "TCFD Report"]
)

# Assess transition vulnerability (1-5 where 5 = worst)
scorecard.assess_transition_vulnerability(
    sector_carbon_intensity=5,      # Very high (oil & gas)
    stranded_asset_risk=5,          # Critical risk
    policy_regulatory_risk=4,       # UK carbon pricing, Net Zero target
    technology_disruption=4,        # EV adoption threatens demand
    market_sentiment_risk=4,        # Investor divestment
    legal_litigation_risk=3,        # Some litigation risk
    country_transition_dependency=2,# UK not dependent on oil exports
    rationale="High exposure across all transition risk vectors",
    sources=["IEA Net Zero Report", "UK ETS"]
)

# Assess transition opportunity (1-5 where 1 = best)
scorecard.assess_transition_opportunity(
    market_growth_potential=5,      # No growth in fossil fuels
    green_revenue_share=5,          # <5% from renewables
    competitive_advantage=5,        # No advantage in transition
    rationale="Minimal positioning for energy transition",
    sources=["Company investor presentation"]
)

# Assess physical risks (1-5 where 5 = worst)
scorecard.assess_physical_risk(
    acute_hazard_exposure=2,        # North Sea storms manageable
    chronic_climate_exposure=2,     # Limited chronic impact
    ecosystem_dependency=3,         # Marine ecosystem considerations
    adaptation_capability=3,        # Some resilience planning
    scenario_analysis_done=3,       # Basic scenario analysis
    rationale="Physical risks moderate; transition risks dominate",
    sources=["Met Office UK Climate Projections"]
)

# Add summary
scorecard.summary = "Overall climate risk is VERY HIGH (4.2/5) due to transition risk..."
scorecard.key_risk_drivers = [
    "Stranded asset risk from declining oil demand",
    "High carbon pricing exposure in UK",
    "Investor divestment and ESG exclusions"
]
scorecard.key_opportunities = []  # Limited opportunities

# Generate output
print(scorecard.generate_enhanced_scorecard())
```

#### Option 3: Python Script - ICBC Standard Bank Template
```python
from templates.icbc_standard_bank_template import ICBCStandardBankScorecard

# Create ICBC-specific scorecard
scorecard = ICBCStandardBankScorecard(
    counterparty="GCB",
    cif="100060256",
    country="Ghana",
    sector="Bank",
    industry_code_crs="64194",
    credit_manager="Robin Rouger",
    current_rating="RG24"
)

# Set transition factors (0-5 where 5 = best - NOTE REVERSE SCORING)
scorecard.set_transition_factor(
    "net_zero_target", 0,
    "No - GCB has not committed to net-zero by 2050"
)
scorecard.set_transition_factor(
    "tcfd_reporting", 0,
    "None - No TCFD report published"
)
scorecard.set_transition_factor(
    "vulnerable_sector_concentration", 5,
    "None, largest exposure to retail and services"
)

# Set physical factors
scorecard.set_physical_factor(
    "asset_concentration_climate_risk", 1,
    "Ghana at risk to droughts, coastal erosion, floods"
)

# Add concluding remarks
scorecard.concluding_remarks = "Your analysis..."

# Generate ICBC-formatted output
print(scorecard.generate_icbc_scorecard())
```

### Risk Categories Assessed

#### Transition Risk Assessment (3 Components)

**1. Transition Preparedness** (30% weight)
*Assesses counterparty's intent and capability to transition*
- Net-zero target credibility
- Climate disclosure quality (TCFD/CDP)
- Governance structure (board oversight, committees)
- Transition plan credibility
- Capex alignment with Paris Agreement goals

**2. Transition Vulnerability** (60% weight)
*Assesses exposure to transition risks*
- Sector carbon intensity
- Stranded asset risk
- Policy & regulatory pressure
- Technology disruption vulnerability
- Market & investor sentiment risk
- Legal & litigation risk
- **Country transition dependency** (sovereign fiscal risk)

**3. Transition Opportunity** (10% offset)
*Assesses potential benefits from climate transition*
- Low-carbon market growth potential
- Green revenue share
- Competitive advantage in transition

#### Physical Risk Assessment (5 Factors)
1. **Acute Climate Hazard Exposure** - Hurricanes, floods, wildfires, droughts
2. **Chronic Climate Change Exposure** - Sea-level rise, temperature increases, water stress
3. **Ecosystem Dependency** - Deforestation, biodiversity loss, supply chain vulnerabilities
4. **Adaptation Capability** - Resilience planning, adaptation measures
5. **Scenario Analysis** - Has counterparty assessed their own physical climate risks?

### Scoring Methodology

**Risk Impact Scores (1-5 scale)**
- **1 - Excellent**: No material exposure or well-mitigated risks; or strong climate opportunity
- **2 - Good**: Minor exposure with adequate mitigation measures
- **3 - Adequate**: Moderate exposure with some mitigation in place
- **4 - Weak**: Significant exposure with limited mitigation
- **5 - None/Critical**: Severe exposure with inadequate mitigation; or no climate action

**Transition Risk Calculation**
```
Transition Risk = (30% × Preparedness) + (60% × Vulnerability) - (10% × Opportunity Offset)
```

**Overall Score Calculation**
- Default: 60% transition risk + 40% physical risk (0-5 year horizon)
- Financial Institutions: 70% transition + 30% physical (portfolio-driven)
- Agriculture/Real Estate: 40% transition + 60% physical (asset-driven)

**Rating Override Thresholds**
- **No Override**: Overall score ≤ 2.5, strong mitigation
- **Consider Override**: Score 2.5-3.5, restricted sector
- **Mandatory Override**: Score > 3.5, prohibited sector, weak mitigation

### Sector Classifications (from Environmental Risk Policy)

**🚫 Prohibited (No Appetite)**
- Mountain top removal mining
- Coal mining and processing
- Arctic drilling and exploration
- Oil tar sands
- Coal-fired power plants
- Deforestation/tropical rainforest burning
- Palm oil production
- Commercial drift net fishing
- Tobacco products

**⚠️ Restricted (Limited Appetite)**
- Coal mining and fracking (< 25% credit economic capital)
- Cement manufacturing (transaction-by-transaction)
- Paper & pulp (transaction-by-transaction)
- Uranium/thorium mining (transaction-by-transaction)
- Fertilizer/chemical production (transaction-by-transaction)
- Logging (transaction-by-transaction)

**👁️ Monitored (Full Appetite with Quarterly Reporting)**
- Oil & Gas
- Chemicals
- Automobiles
- General Manufacturing
- Airlines
- Metals processing
- Power generation (non-coal)
- Agriculture

### Information Sources

**Public Data**
- Company sustainability reports and TCFD disclosures
- CDP (Carbon Disclosure Project) submissions
- ESG ratings: MSCI, Sustainalytics, S&P Global, ISS
- Industry association climate reports
- NGO reports (WWF, Greenpeace, Climate Action Tracker)
- Media searches for environmental incidents

**Geographic Climate Data**
- World Resources Institute Aqueduct (water stress)
- Climate Central sea-level rise projections
- NASA/NOAA climate data
- National meteorological services
- IPCC regional climate projections

**Regulatory & Scenarios**
- **PRA SS5/25 guidance (UK)** - Replaces SS3/19 from December 2025
- MAS Environmental Risk Guidelines (Singapore)
- NGFS climate scenarios
- Country NDCs (Nationally Determined Contributions)
- Oxford Economics Global Climate Service (if available)

### Output Formats

The skill generates scorecards in multiple formats:

1. **Markdown** (.md) - For review and inclusion in reports
2. **JSON** (.json) - For programmatic access and integration
3. **Credit Workflow JSON** - Structured ~80-field output for credit systems (see below)
4. **Word** (.docx) - For credit papers (Appendix E) [future]
5. **Excel** (.xlsx) - For tracking and dashboard purposes [future]

### Credit Workflow System Integration

When requests originate from the **Credit Risk Workflow System**, this skill automatically detects the source and produces structured JSON output with ~80 fields suitable for automated credit decision systems.

#### Detection

The skill detects credit workflow requests when the incoming JSON contains:
```json
{
  "source_system": "credit_workflow",
  "request_type": "climate_scorecard_generation"
}
```

#### JSON Output Structure

```json
{
  "scorecard_data": {
    "assessment_type": "initial",
    "net_zero_target_exists": true,
    "net_zero_target_year": 2050,
    // ... ~80 fields total
    "overall_climate_risk_rating": "C"
  },
  "confidence_scores": {
    "net_zero_target_exists": 0.90,
    "net_zero_target_year": 0.90,
    // ... confidence (0.0-1.0) for each field
  },
  "generation_notes": "Assessment sources, assumptions, and data gaps"
}
```

#### ⚠️ CRITICAL: Enum Fields Must Use EXACT Values

**DO NOT** return descriptions for enum fields - use ONLY these exact values:

| Field | Valid Values ONLY |
|-------|-------------------|
| `capex_alignment_trajectory` | `increasing`, `stable`, `decreasing` |
| `market_sentiment_investor_pressure` | `low`, `medium`, `high` |
| `pillar_2_treatment` | `not_material`, `low_add_on`, `medium_add_on`, `high_add_on` |
| `market_sentiment_esg_rating` | Max 20 chars (e.g., `"MSCI BB"`) |

See [SKILL.md](SKILL.md#-critical-enum-fields-must-use-exact-values-only) for complete enum reference.

#### Python Usage

```python
from credit_workflow_output import (
    is_credit_workflow_request,
    parse_credit_workflow_request,
    generate_credit_workflow_response
)
from climate_scorecard_helper import EnhancedClimateScorecard, ConfidenceTracker

# Check if request is from credit workflow
if is_credit_workflow_request(request_data):
    parsed = parse_credit_workflow_request(request_data)

    # Create and populate scorecard
    scorecard = EnhancedClimateScorecard(
        counterparty=parsed["counterparty_name"],
        sector=parsed["counterparty_sector"],
        country=parsed["counterparty_country"]
    )

    # ... assess risks and populate fields ...

    # Generate JSON response
    json_response = generate_credit_workflow_response(scorecard)
    return json_response
```

#### Confidence Scoring

Confidence scores (0.0-1.0) are assigned based on data source quality:

| Source | Confidence |
|--------|------------|
| Verified disclosure (audited) | 0.95 |
| Company disclosure (annual report) | 0.90 |
| ESG rating (MSCI, Sustainalytics) | 0.85 |
| Industry proxy | 0.60 |
| Estimate | 0.50 |
| Null/missing data | 0.30 |

See [SKILL.md](SKILL.md#credit-workflow-system-integration) for full field requirements and schema.

### Example: Completed Scorecard Summary

```
ENHANCED CLIMATE & ENVIRONMENTAL RISK SCORECARD - GCB Bank Ltd

Transition Risk: 2.5/5
  - Preparedness:  4.0/5 (Weak - no TCFD, no net-zero target)
  - Vulnerability:  2.4/5 (Moderate - low direct exposure)
  - Opportunity:    3.3/5 (Neutral - limited green finance)

Physical Risk: 3.4/5
  - Acute Hazards:  4/5 (Coastal flooding risk in Accra)
  - Adaptation:     3/5 (Moderate capability)
  - CP Analysis:    5/5 (No scenario analysis by GCB)

Overall Score: 2.8/5 (Moderate)

Sector Classification: None (Financial Institution)
Rating Override:       NO OVERRIDE REQUIRED

Key Findings:
- Weak climate governance (no TCFD, no scenario analysis)
- Country dependency on vulnerable sectors (mining, agriculture)
- Sovereign climate risk through government securities (33% assets)
- Moderate vulnerability despite weak preparedness

Recommendations:
1. Encourage GCB to develop climate risk management capability
2. Monitor agricultural NPL trends and collateral values
3. Track Ghana sovereign climate fiscal stress
4. Annual review required
```

### Integration with Other Skills

**Upstream Skills**
- Use before completing credit papers
- Incorporate into ESG due diligence process
- Required for Credit Committee submissions

**Downstream Skills**
- Feed into **itc-template-filler** for project approvals
- Support **icc-business-case-filler** business cases
- Reference in **meeting-minutes** for Credit Committee
- Track via **status-reporter** for ongoing monitoring

### Quality Assurance Checklist

Before submitting a scorecard, verify:

- [ ] All risk categories assessed with specific sub-factors
- [ ] Data sources cited for key assertions
- [ ] Sector classification checked against Environmental Risk Policy
- [ ] Rating override logic clearly explained
- [ ] Monitoring triggers and review frequency specified
- [ ] Forward-looking scenarios (5-10 years) considered
- [ ] Mitigation measures verified, not just client claims
- [ ] Opportunity assessment completed (not just risks)
- [ ] Country/sovereign risk transmission considered
- [ ] Counterparty's own climate risk management assessed

### Common Pitfalls to Avoid

1. ❌ **Over-reliance on ESG ratings** - Ratings vary widely; verify with primary sources
2. ❌ **Ignoring forward-looking scenarios** - Current low risk ≠ future low risk
3. ❌ **Sector stereotyping** - Individual practices vary within sectors
4. ❌ **Geographic blind spots** - Check supply chain exposures
5. ❌ **Unverified mitigation claims** - Confirm stated mitigation measures
6. ❌ **Short-term bias** - Consider 10-30 year physical risk horizons
7. ❌ **Missing opportunities** - Assess transition benefits, not just risks
8. ❌ **Ignoring country risk** - Sovereign climate fiscal stress affects all domestic counterparties

### Files in This Skill

```
climate-scorecard-filler/
├── SKILL.md                              # Main skill definition
├── README.md                             # This file
├── QUICK_REFERENCE.md                    # One-page quick reference
├── CHANGELOG.md                          # Version history
├── IMPLEMENTATION_SUMMARY.md             # Implementation notes
├── ICBC_LEARNINGS.md                     # Learnings from ICBC template
├── climate_scorecard_helper.py           # Enhanced generic framework + ConfidenceTracker
├── credit_workflow_output.py             # Credit Workflow System JSON integration
├── examples/
│   ├── gcb_bank_example.md              # Generic framework example
│   └── oil_company_high_risk.md         # Prohibited sector example
└── templates/
    ├── README.md                         # Bank template documentation
    └── icbc_standard_bank_template.py   # ICBC-specific implementation
```

### Testing the Skill

```bash
# Test with example scenario
cd /Users/gavinslater/projects/riskagent
source .venv/bin/activate

# Run enhanced example
python .claude/skills/climate-scorecard-filler/climate_scorecard_helper.py

# Run ICBC example
python .claude/skills/climate-scorecard-filler/templates/icbc_standard_bank_template.py

# Check output
cat output/gcb_climate_scorecard.md
```

### Support & Questions

- Review the Environmental Risk Policy v4.0 for sector classifications
- Consult Credit Rating & Support Policy for rating override guidance
- Contact Risk Management for climate scenario analysis support
- Reference **PRA SS5/25** and MAS Guidelines for regulatory requirements
- See [ICBC_LEARNINGS.md](ICBC_LEARNINGS.md) for enhancement details

### Version History

- **v2.1** (2025-12-31) - Credit Workflow System Integration
  - Added `credit_workflow_output.py` module for JSON API integration
  - Extended dataclasses with ~45 additional fields for full PRA SS5/25 coverage
  - Added `ConfidenceTracker` class for data quality scoring (0.0-1.0)
  - Added `to_credit_workflow_json()` method for structured JSON output
  - Added conversion utilities (score→enum, score→rating)
  - Detection logic for `source_system: "credit_workflow"` requests
  - ~80 total fields across 9 assessment sections
- **v2.0** (2025-11-29) - Enhanced generic framework incorporating ICBC learnings
  - Added transition preparedness/vulnerability/opportunity split
  - Added country-level sovereign risk transmission
  - Added counterparty climate capability assessment
  - Structured question-based approach
  - 17 specific assessment factors
- **v1.0** (2025-11-29) - Initial skill creation
  - Generic framework with 7 risk categories
  - ICBC Standard Bank template
  - Examples and documentation

### Related Documentation

- [SKILL.md](SKILL.md) - Full skill definition and instructions
- [ICBC_LEARNINGS.md](ICBC_LEARNINGS.md) - What we learned from ICBC template
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical implementation details
- [Environmental Risk Policy v4.0](../../data/example_bank/policies/Environmental_Risk/)
- [Credit Paper Example](../../data/example_bank/Projects/Credit\ Workflow/Credit\ paper\ example.docx)
- [TCFD Framework](https://www.fsb-tcfd.org/)
- [NGFS Climate Scenarios](https://www.ngfs.net/ngfs-scenarios-portal/)
