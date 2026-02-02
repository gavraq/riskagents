---
name: climate-scorecard-filler
description: Completes Climate & Environmental Risk Scorecards for credit applications. Use when the front office requests credit limit extensions and needs to assess counterparty climate and environmental risks. Evaluates physical risks (acute/chronic climate events) and transition risks (policy, technology, market sentiment changes). Supports both generic framework and bank-specific templates (ICBC Standard Bank). Keywords - climate scorecard, environmental risk, ESG credit assessment, transition risk, physical risk, climate credit risk, ICBC scorecard.
allowed-tools: [Read, Write, WebSearch, Bash]
---

# Climate & Environmental Risk Scorecard Filler

## Purpose
This skill helps Front Office departments complete the Climate & Environmental Risk Scorecard (Appendix E) required when requesting additional credit limits for counterparties. The scorecard assesses both physical and transition climate risks to determine if credit rating adjustments are needed.

## Bank-Specific Templates

The skill supports two modes:

1. **Generic Framework** - Flexible scorecard suitable for any bank (default)
2. **ICBC Standard Bank Template** - Exact scorecard format used by ICBC Standard Bank with specific risk factor questions

When a user specifies "ICBC Standard Bank" or "ICBC scorecard", automatically use the ICBC-specific template.

## When to Use
- Front office teams preparing credit papers for credit limit increases
- Annual credit reviews requiring environmental risk assessment updates
- New counterparty onboarding requiring ESG risk evaluation
- Credit Committee submissions requiring Appendix E documentation
- Transactions involving environmentally sensitive sectors (Energy, Mining, Industrials, Agriculture)

## Scorecard Framework

The Climate & Environmental Risk Scorecard evaluates two main risk categories:

### 1. Transition Risks
Assess financial risks from the transition to a low-carbon economy:

**Policy & Regulatory Risk**
- Exposure to carbon pricing mechanisms (carbon taxes, ETS schemes)
- Impact of energy transition policies
- Pollution control and resource conservation regulations
- Jurisdictional regulatory standards and enforcement quality
- Compliance with emerging climate disclosure requirements

**Technology Risk**
- Disruption from clean energy and energy-saving technologies
- Exposure to stranded asset risk (fossil fuel-dependent business models)
- Investment in low-carbon alternatives and R&D
- Technological readiness for transition

**Market & Sentiment Risk**
- Shifting consumer preferences toward low-carbon products
- Changes in investor sentiment on carbon-intensive assets
- Market share vulnerability to disruptive business models
- Access to green financing and capital markets

**Legal & Liability Risk**
- Litigation risk from failure to mitigate or adapt
- Climate-related disclosure obligations
- Contractual risks related to emissions commitments

### 2. Physical Risks
Assess risks from climate-related physical events:

**Acute Physical Risks**
- Exposure to hurricanes, floods, wildfires
- Vulnerability to droughts and water scarcity
- Heat wave impacts on operations
- Geographic concentration in high-risk areas

**Chronic Physical Risks**
- Sea-level rise impacts on assets and operations
- Rising mean temperatures affecting productivity
- Ocean acidification (for marine-dependent sectors)
- Long-term water stress

**Ecosystem Risks**
- Exposure to deforestation and biodiversity loss
- Pollution risks (air, water, soil, marine)
- Supply chain dependencies on at-risk ecosystems

## Scoring Methodology

### Risk Impact Scores (1-5)
1. **Negligible** - No material exposure or well-mitigated risks
2. **Low** - Minor exposure with adequate mitigation measures
3. **Medium** - Moderate exposure with some mitigation in place
4. **High** - Significant exposure with limited mitigation
5. **Critical** - Severe exposure with inadequate mitigation

### Sector-Based Risk Materiality

Refer to the Bank's Environmental Risk Policy for sector classifications:

**Prohibited Sectors (No Appetite)**
- Mountain top removal mining
- Coal mining and processing
- Arctic drilling and exploration
- Oil (tar) sands
- Coal-fired power plants
- Deforestation/tropical rainforest burning
- Palm oil production
- Commercial drift net fishing
- Tobacco production

**Restricted Sectors (Limited Appetite)**
- Coal mining and fracking (< 25% credit economic capital)
- Cement manufacturing
- Paper & pulp
- Uranium/thorium mining
- Chemical/fertilizer production
- Logging

**Monitored Sectors (Full Appetite with Monitoring)**
- Oil & Gas
- Chemicals
- Automobiles
- Manufacturing
- Airlines
- Metals processing
- Power generation (non-coal)
- Agriculture

## Assessment Process

### Step 1: Gather Counterparty Information
- Company sustainability reports and disclosures
- TCFD (Task Force on Climate-related Financial Disclosures) reports
- CDP (Carbon Disclosure Project) submissions
- ESG ratings from Sustainalytics, MSCI, S&P Global
- Industry sector analysis
- Geographic exposure analysis
- Public source reviews (media, NGO reports)
- Client policies for managing environmental risk

### Step 2: Evaluate Transition Risks
For each transition risk category:
1. Assess current exposure level
2. Review counterparty mitigation strategies
3. Consider forward-looking scenarios (policy changes, technology shifts)
4. Assign risk score (1-5)
5. Document rationale with specific evidence

### Step 3: Evaluate Physical Risks
For each physical risk category:
1. Identify geographic exposure to climate hazards
2. Assess asset vulnerability (facilities, supply chains)
3. Review business continuity and adaptation plans
4. Consider climate scenarios (RCP 2.6, 4.5, 8.5)
5. Assign risk score (1-5)
6. Document rationale with specific evidence

### Step 4: Calculate Overall Climate Risk Score
- Weight transition and physical risks based on sector and time horizon
- Short-term (0-5 years): Transition risks typically more material
- Long-term (5-30 years): Physical risks increase in materiality
- Apply sector-specific adjustments

### Step 5: Determine Rating Override
Based on the overall climate risk score:

**No Override Required**
- Overall risk score ≤ 2.5
- Strong mitigation strategies in place
- Sector is Monitored category with low exposure

**Consider Downward Override**
- Overall risk score 2.5 - 3.5
- Sector is Restricted with moderate-high exposure
- Weak mitigation strategies
- High concentration in at-risk geographies

**Mandatory Downward Override**
- Overall risk score > 3.5
- Sector is Prohibited
- Critical exposure with inadequate mitigation
- Regulatory action likely or pending

### Step 6: Document Findings
Complete Appendix E with:
- Summary of key climate risks identified
- Scoring rationale for each risk category
- Mitigation measures in place
- Rating override recommendation (if any)
- Monitoring requirements and review triggers
- Forward-looking risk evolution assessment

## Information Sources

### Public Data Sources
- Company annual reports and sustainability reports
- CDP Climate Change questionnaires
- TCFD reports
- ESG rating agency reports (MSCI, Sustainalytics, S&P Global)
- Industry association reports
- NGO reports (WWF, Greenpeace, Climate Action Tracker)
- Media searches for environmental incidents

### Proprietary Tools
- RiskFrontier climate scenarios (if available)
- Oxford Economics Global Climate Service shocks
- Internal climate stress test results
- Sector-specific climate risk models

### Regulatory Sources
- **PRA SS5/25 guidance (UK)** - Replaces SS3/19 from December 2025
- BCBS Principles for climate-related financial risks
- ISSB IFRS S2 Climate-related Disclosures
- MAS Guidelines on Environmental Risk Management (Singapore)
- NGFS climate scenarios
- IPCC climate projections
- Country-specific climate policies and NDCs

### Geographic Climate Data
- World Resources Institute Aqueduct (water stress)
- Climate Central sea-level rise maps
- NASA climate data
- National meteorological services

## Output Format

The completed scorecard should be structured as:

```
CLIMATE & ENVIRONMENTAL RISK SCORECARD
Counterparty: [Name]
Country: [Country]
Sector: [Sector]
Assessment Date: [Date]
Prepared By: [Name, Department]

TRANSITION RISK ASSESSMENT
┌─────────────────────────────────┬───────┬─────────────────────────┐
│ Risk Category                   │ Score │ Rationale               │
├─────────────────────────────────┼───────┼─────────────────────────┤
│ Policy & Regulatory Risk        │  X/5  │ [Brief justification]   │
│ Technology Risk                 │  X/5  │ [Brief justification]   │
│ Market & Sentiment Risk         │  X/5  │ [Brief justification]   │
│ Legal & Liability Risk          │  X/5  │ [Brief justification]   │
├─────────────────────────────────┼───────┼─────────────────────────┤
│ TRANSITION RISK SCORE          │  X.X  │ [Weighted average]      │
└─────────────────────────────────┴───────┴─────────────────────────┘

PHYSICAL RISK ASSESSMENT
┌─────────────────────────────────┬───────┬─────────────────────────┐
│ Risk Category                   │ Score │ Rationale               │
├─────────────────────────────────┼───────┼─────────────────────────┤
│ Acute Physical Risks            │  X/5  │ [Brief justification]   │
│ Chronic Physical Risks          │  X/5  │ [Brief justification]   │
│ Ecosystem Risks                 │  X/5  │ [Brief justification]   │
├─────────────────────────────────┼───────┼─────────────────────────┤
│ PHYSICAL RISK SCORE            │  X.X  │ [Weighted average]      │
└─────────────────────────────────┴───────┴─────────────────────────┘

OVERALL ASSESSMENT
┌─────────────────────────────────┬─────────────────────────────────┐
│ Overall Climate Risk Score      │  X.X / 5                        │
│ Sector Classification           │  [Prohibited/Restricted/        │
│                                 │   Monitored/None]               │
│ Rating Override Required        │  [Yes/No]                       │
│ Override Direction              │  [Downward/None]                │
│ Override Notches                │  [X notches]                    │
└─────────────────────────────────┴─────────────────────────────────┘

SUMMARY & RECOMMENDATIONS
[2-3 paragraph summary of key findings, material risks, mitigation measures,
and any recommended rating adjustments or monitoring requirements]

KEY RISK DRIVERS
- [List top 3-5 most material climate risk factors]

MITIGATION MEASURES IN PLACE
- [List key counterparty mitigation strategies]

MONITORING & REVIEW TRIGGERS
- [Specify conditions requiring scorecard update]
- [Define review frequency]

DATA SOURCES & REFERENCES
- [List all sources used in assessment]
```

## Instructions for Claude

When a user requests help completing a climate scorecard:

1. **Clarify the Request and Template Selection**
   - Confirm counterparty name and sector
   - **Ask which bank template to use**: "Is this for ICBC Standard Bank or a generic scorecard?"
   - If ICBC Standard Bank mentioned, use the specific template at `templates/icbc_standard_bank_template.py`
   - Identify available information sources
   - Determine if this is new assessment or annual review
   - Check for existing scorecards to update

2. **Gather Information**
   - Search for publicly available ESG/climate disclosures
   - Review any provided client materials
   - Research sector-specific climate risks
   - Identify geographic exposure to climate hazards

3. **Interactive Assessment**
   - Guide the user through each risk category
   - Ask clarifying questions about counterparty practices
   - Request missing information if critical gaps exist
   - Suggest data sources where information is incomplete

4. **Scoring & Rationale**
   - Apply consistent scoring methodology
   - Provide clear, evidence-based rationale
   - Reference specific data points and sources
   - Compare to sector peers where possible

5. **Rating Override Analysis**
   - Calculate overall risk score
   - Check against sector classification
   - Determine if override is warranted
   - Provide clear recommendation with justification

6. **Document Completion**
   - Generate completed scorecard in specified format
   - Include all required sections
   - Provide summary suitable for Credit Committee
   - Suggest monitoring triggers and review frequency

7. **Output Delivery**
   - Save completed scorecard to appropriate location
   - Offer to export to Word/Excel format if needed
   - Provide markdown version for easy review
   - Generate summary for inclusion in credit paper

## Examples

### Example 1: ICBC Standard Bank Template
```
User: "I need to complete an ICBC climate scorecard for GCB Bank in Ghana"

Claude: I'll help you complete the ICBC Standard Bank climate scorecard for GCB Bank.

I'll use the ICBC-specific template which has detailed risk factor questions with 0-5
scoring (where 5 = best/lowest risk - note the reverse scoring).

First, let me gather information:
1. Do you have GCB's latest annual report or sustainability disclosures?
2. What is the CIF number and current credit rating?
3. Who is the credit manager for this counterparty?

I'll search for publicly available information while you gather those details...

[Searches for GCB ESG data, Ghana climate risks, sector analysis]

Now I'll guide you through the ICBC template questions:

**Intent to Transition:**
- Does GCB explicitly target net-zero by 2050? [0-5 where 5=yes with plan]
- Does GCB publish TCFD or equivalent report? [0-5 where 5=comprehensive]
- Does GCB have governance/teams to address climate risks? [0-5 where 5=robust]

**Vulnerabilities:**
- Material asset concentrations in vulnerable sectors? [0-5 where 5=none]
- Operates in country with FX/fiscal dependency on vulnerable sector? [0-5]
...

[Completes ICBC-formatted scorecard with all specific risk factors]
```

### Example 2: Generic Framework
```
User: "I need a climate scorecard for XYZ Petroleum, a Nigerian oil company - not ICBC format"

Claude: I'll complete a generic climate scorecard for XYZ Petroleum using the
flexible framework.

First, let me gather some information:
1. Do you have XYZ Petroleum's latest sustainability report or CDP submission?
2. What is the primary business - upstream exploration, midstream pipelines,
   or downstream refining?
3. What credit limit are we considering?

I'll search for publicly available ESG information while you gather those details...

[Searches for company ESG data, sector analysis, Nigeria climate risks]

Based on my research, here's what I found:
- XYZ Petroleum operates primarily upstream oil production in Niger Delta
- Nigeria has high physical risk from coastal flooding and acute weather
- Oil & Gas sector is "Monitored" under our Environmental Risk Policy
- Transition risk is HIGH due to stranded asset risk and policy changes
...
```

### Example 2: Solar Energy Developer
```
User: "Complete scorecard for GreenSun Energy - they develop solar farms in California"

Claude: I'll assess GreenSun Energy's climate scorecard. Solar energy
developers generally have low transition risk (they're part of the solution)
but may have physical risks.

Let me evaluate:

TRANSITION RISKS (Expected: Low)
- Policy Risk: LOW (1/5) - Benefits from renewable energy policies
- Technology Risk: LOW (1/5) - Core business aligned with clean tech
- Market Risk: LOW (1/5) - Growing demand for renewable energy
- Legal Risk: LOW (1/5) - No stranded asset concerns

PHYSICAL RISKS:
- Acute: MEDIUM (3/5) - California wildfire and drought exposure
- Chronic: MEDIUM (2/5) - Heat impacts on panel efficiency
- Ecosystem: LOW (1/5) - Minimal ecosystem dependencies

Overall Score: 1.5/5 - NO OVERRIDE REQUIRED

[Generates full scorecard]
```

## Common Pitfalls to Avoid

1. **Over-reliance on ESG ratings** - Ratings vary widely; verify with primary sources
2. **Ignoring forward-looking scenarios** - Current low risk doesn't mean future low risk
3. **Sector stereotyping** - Individual company practices vary within sectors
4. **Geographic blind spots** - Supply chain exposures may be in different geographies
5. **Mitigation credit without verification** - Verify claimed mitigation measures
6. **Short-term bias** - Consider long-term physical risks (10-30 year horizon)
7. **Data gaps** - Document assumptions when data unavailable; flag for follow-up

## Quality Checks

Before finalizing the scorecard:
- ✓ All risk categories scored and justified
- ✓ Sources cited for key claims
- ✓ Sector classification verified against policy
- ✓ Rating override logic clearly explained
- ✓ Monitoring triggers specified
- ✓ Consistent with similar counterparties
- ✓ Forward-looking scenarios considered
- ✓ Mitigation measures verified not just claimed

## Output Formats

The skill generates scorecards in multiple formats:

### 1. Markdown (Default)
The `generate_enhanced_scorecard()` method produces markdown output suitable for:
- Pasting into credit papers
- Review in Claude Code
- Conversion to other formats

### 2. Word Document (.docx)
Use `climate_scorecard_document_builder.py` to generate professional Word documents with:
- **Branded cover page** with www.risk-agents.com
- **PRA SS5/25 Aligned** badge
- Professional formatting with tables
- Color-coded risk indicators
- All SS5/25 compliance sections

**Usage:**
```python
from climate_scorecard_document_builder import ClimateScorecardDocumentBuilder

builder = ClimateScorecardDocumentBuilder()
doc = builder.create_scorecard_document(
    scorecard=my_scorecard,
    bank_name="Example Bank",
    prepared_for="Credit Committee"
)
builder.save_document(Path("output/scorecard.docx"))
```

**Document Structure:**
1. Cover Page (www.risk-agents.com branded)
2. Executive Summary
3. Counterparty Profile
4. Transition Risk Assessment
5. Physical Risk Assessment
6. Scenario Analysis Quality (SS5/25)
7. Litigation Risk (if distinct channel)
8. Combined Assessment
9. Risk Appetite Alignment (SS5/25)
10. ICAAP Considerations (SS5/25)
11. Data Quality Declaration (SS5/25)
12. Conclusions & Recommendations
13. Monitoring Triggers
14. Regulatory References

## Credit Workflow System Integration

When requests originate from the **Credit Risk Workflow System**, this skill produces structured JSON output instead of markdown. This enables automated integration with credit decision systems.

### Detection Criteria

The skill detects credit workflow requests when the incoming message contains:

```json
{
  "source_system": "credit_workflow",
  "request_type": "climate_scorecard_generation",
  "counterparty": {
    "name": "Counterparty Name",
    "sector": "Sector",
    "country": "Country"
  }
}
```

Both `source_system: "credit_workflow"` AND `request_type: "climate_scorecard_generation"` must be present.

### JSON Output Format

When credit workflow is detected, return JSON with this structure:

```json
{
  "scorecard_data": {
    // ~80 fields - see Extended Field Requirements below
  },
  "confidence_scores": {
    // 0.0-1.0 confidence for each field
  },
  "generation_notes": "Data sources, assumptions, and gaps"
}
```

### ⚠️ CRITICAL: Enum Fields Must Use EXACT Values Only

**DO NOT** return descriptions or explanatory text for enum/choice fields. The database has strict character limits (mostly 50 chars) and will truncate or reject invalid values.

**WRONG:**
```json
"capex_alignment_trajectory": "The company's green capital expenditure is projected to increase significantly over the next 5 years"
"market_sentiment_investor_pressure": "There is significant pressure from institutional investors to divest from fossil fuels"
"pillar_2_treatment": "Climate risk is material and should be treated as a medium capital add-on under Pillar 2"
```

**CORRECT:**
```json
"capex_alignment_trajectory": "increasing"
"market_sentiment_investor_pressure": "high"
"pillar_2_treatment": "medium_add_on"
```

**All enum fields and their ONLY valid values:**

| Field | Valid Values ONLY |
|-------|-------------------|
| `assessment_type` | `initial`, `annual_review`, `event_triggered`, `material_change` |
| `net_zero_target_scope` | `scope_1`, `scope_1_2`, `scope_1_2_3` |
| `tcfd_disclosure_level` | `none`, `partial`, `full`, `verified` |
| `capex_alignment_trajectory` | `increasing`, `stable`, `decreasing` |
| `carbon_intensity_trend` | `declining`, `stable`, `increasing` |
| `stranded_asset_exposure` | `none`, `low`, `medium`, `high` |
| `tech_disruption_risk_level` | `low`, `medium`, `high`, `critical` |
| `market_sentiment_investor_pressure` | `low`, `medium`, `high` |
| `green_market_growth_potential` | `none`, `low`, `medium`, `high`, `transformative` |
| `green_revenue_trend` | `declining`, `stable`, `growing`, `rapidly_growing` |
| `acute_hazard_exposure` | `low`, `medium`, `high`, `critical` |
| `ecosystem_dependency_level` | `none`, `low`, `medium`, `high` |
| `adaptation_capability_level` | `none`, `limited`, `developing`, `mature` |
| `risk_appetite_category` | `avoid`, `manage`, `monitor`, `acceptable` |
| `pillar_2_treatment` | `not_material`, `low_add_on`, `medium_add_on`, `high_add_on` |
| `data_quality_overall` | `poor`, `fair`, `good`, `excellent` |
| `overall_transition_risk_score` | `low`, `medium`, `high`, `critical` |
| `overall_physical_risk_score` | `low`, `medium`, `high`, `critical` |
| `overall_climate_risk_rating` | `A`, `B`, `C`, `D`, `E` |

**Short string field with strict limit:**
| Field | Max Length | Example |
|-------|------------|---------|
| `market_sentiment_esg_rating` | **20 chars** | `"MSCI BB"` or `"Sustainalytics 38.6"` |

Put any explanatory text in the relevant `_assessment` text fields (e.g., `tech_disruption_assessment`, `competitive_advantage_assessment`), NOT in the enum fields.

### Extended Field Requirements

When processing credit workflow requests, you MUST assess ALL of the following fields:

#### Section 1: Assessment Context
- `assessment_type` - "initial" | "annual_review" | "event_triggered" | "material_change"

#### Section 2: Transition Risk - Preparedness
| Field | Type | Description |
|-------|------|-------------|
| `net_zero_target_exists` | boolean | Has committed to net-zero |
| `net_zero_target_year` | integer | Target year (e.g., 2050) |
| `net_zero_target_scope` | enum | "scope_1" | "scope_1_2" | "scope_1_2_3" |
| `net_zero_science_based` | boolean | SBTi validated |
| `net_zero_score` | integer 1-5 | Overall net-zero assessment |
| `tcfd_disclosure_level` | enum | "none" | "partial" | "full" | "verified" |
| `tcfd_disclosure_score` | integer 1-5 | Disclosure quality |
| `climate_governance_board` | boolean | Board oversight exists |
| `climate_governance_exec_accountability` | boolean | Named executive responsible |
| `climate_governance_incentives_linked` | boolean | Compensation linked to climate |
| `climate_governance_score` | integer 1-5 | Governance quality |
| `transition_plan_exists` | boolean | Has transition plan |
| `transition_plan_published` | boolean | Plan is public |
| `transition_plan_milestones` | string | Key milestones description |
| `transition_plan_score` | integer 1-5 | Plan credibility |
| `green_capex_percentage` | float | % of capex on green projects |
| `capex_alignment_trajectory` | string | Paris-aligned trajectory assessment |
| `capex_alignment_score` | integer 1-5 | Capex alignment quality |

#### Section 3: Transition Risk - Vulnerability
| Field | Type | Description |
|-------|------|-------------|
| `carbon_intensity_scope1` | float | tCO2e per $M revenue (Scope 1) |
| `carbon_intensity_scope2` | float | tCO2e per $M revenue (Scope 2) |
| `carbon_intensity_scope3` | float | tCO2e per $M revenue (Scope 3) |
| `carbon_intensity_trend` | enum | "decreasing" | "stable" | "increasing" |
| `carbon_intensity_score` | integer 1-5 | Carbon intensity assessment |
| `stranded_asset_exposure` | enum | "none" | "low" | "medium" | "high" |
| `stranded_asset_types` | string | Types of potentially stranded assets |
| `stranded_asset_score` | integer 1-5 | Stranded asset risk |
| `policy_pressure_jurisdictions` | string | Key regulatory jurisdictions |
| `policy_pressure_carbon_pricing_exposure` | boolean | Subject to carbon pricing |
| `policy_pressure_score` | integer 1-5 | Policy/regulatory pressure |
| `tech_disruption_risk_level` | enum | "low" | "medium" | "high" | "critical" |
| `tech_disruption_assessment` | string | Technology disruption narrative |
| `tech_disruption_score` | integer 1-5 | Tech disruption vulnerability |
| `market_sentiment_esg_rating` | string | External ESG rating (e.g., "MSCI BBB") |
| `market_sentiment_investor_pressure` | string | Investor engagement description |
| `market_sentiment_score` | integer 1-5 | Market sentiment risk |
| `litigation_current_cases` | integer | Number of active climate cases |
| `litigation_historical_cases` | integer | Number of past climate cases |
| `litigation_exposure_assessment` | string | Litigation risk narrative |
| `litigation_score` | integer 1-5 | Legal/litigation risk |
| `country_dependency_high_risk_revenue` | float | % revenue from high-risk countries |
| `country_dependency_score` | integer 1-5 | Country transition dependency |

#### Section 4: Transition Risk - Opportunity
| Field | Type | Description |
|-------|------|-------------|
| `green_market_growth_potential` | enum | "none" | "low" | "medium" | "high" |
| `green_market_growth_assessment` | string | Market opportunity narrative |
| `green_market_growth_score` | integer 1-5 | Growth potential (1=best) |
| `green_revenue_percentage` | float | % revenue from green products |
| `green_revenue_trend` | enum | "decreasing" | "stable" | "increasing" |
| `green_revenue_score` | integer 1-5 | Green revenue (1=best) |
| `competitive_advantage_assessment` | string | Competitive position narrative |
| `competitive_advantage_score` | integer 1-5 | Advantage (1=best) |

#### Section 5: Physical Risk Assessment
| Field | Type | Description |
|-------|------|-------------|
| `acute_hazard_exposure` | enum | "none" | "low" | "medium" | "high" |
| `acute_hazard_types` | array[string] | ["floods", "hurricanes", "wildfires", ...] |
| `acute_hazard_score` | integer 1-5 | Acute hazard risk |
| `chronic_exposure_assessment` | string | Chronic risk narrative |
| `chronic_exposure_score` | integer 1-5 | Chronic climate risk |
| `ecosystem_dependency_level` | enum | "none" | "low" | "medium" | "high" |
| `ecosystem_dependency_assessment` | string | Ecosystem dependencies narrative |
| `ecosystem_dependency_score` | integer 1-5 | Ecosystem risk |
| `adaptation_capability_level` | enum | "none" | "low" | "medium" | "high" |
| `adaptation_investments` | string | Adaptation measures description |
| `adaptation_capability_score` | integer 1-5 | Adaptation capability |
| `scenario_analysis_conducted` | boolean | Has conducted scenario analysis |
| `scenario_analysis_scenarios` | array[string] | Scenarios used (e.g., "RCP 4.5") |
| `scenario_analysis_time_horizons` | array[string] | Time horizons (e.g., "2030", "2050") |
| `scenario_analysis_integration` | string | How scenarios inform strategy |
| `scenario_analysis_score` | integer 1-5 | Scenario analysis quality |

#### Section 6: Risk Appetite Alignment
| Field | Type | Description |
|-------|------|-------------|
| `risk_appetite_category` | enum | "prohibited" | "restricted" | "monitored" | "standard" |
| `risk_appetite_justification` | string | Rationale for category |
| `risk_appetite_conditions` | string | Any conditions/covenants |

#### Section 7: Capital & ICAAP Considerations
| Field | Type | Description |
|-------|------|-------------|
| `pillar_2_treatment` | string | Pillar 2 capital treatment |
| `icaap_materiality_assessment` | string | ICAAP materiality narrative |
| `capital_add_on_recommendation` | float | Recommended capital add-on % |

#### Section 8: Data Quality Declaration
| Field | Type | Description |
|-------|------|-------------|
| `data_sources` | array[string] | All sources used |
| `data_proxies_used` | array[string] | Proxies/estimates used |
| `data_gaps_identified` | array[string] | Known data gaps |
| `data_quality_overall` | enum | "high" | "medium" | "low" |

#### Section 9: Summary & Recommendations
| Field | Type | Description |
|-------|------|-------------|
| `overall_transition_risk_score` | float | 1.0-5.0 weighted score |
| `overall_physical_risk_score` | float | 1.0-5.0 weighted score |
| `overall_climate_risk_rating` | enum | "A" | "B" | "C" | "D" | "E" |
| `key_risk_drivers` | array[string] | Top risk factors |
| `key_opportunities` | array[string] | Green opportunities |
| `recommended_mitigations` | array[string] | Risk mitigations |
| `monitoring_triggers` | array[string] | Review triggers |
| `next_review_date` | string | ISO date for next review |

### Confidence Scoring Guidelines

Assign confidence scores (0.0-1.0) based on data source quality:

| Source Type | Confidence | Example |
|-------------|------------|---------|
| `verified_disclosure` | 0.95 | Audited sustainability report |
| `user_provided` | 0.95 | User explicitly confirmed |
| `company_disclosure` | 0.90 | Annual report, TCFD report |
| `esg_rating` | 0.85 | MSCI, Sustainalytics ratings |
| `multiple_sources` | 0.80 | Corroborated from 2+ sources |
| `derived` | 0.75 | Calculated from other fields |
| `industry_proxy` | 0.60 | Industry average applied |
| `sector_average` | 0.55 | Sector benchmark used |
| `estimate` | 0.50 | Reasonable estimate |
| `default` / `null` | 0.30 | No data, null value |

### Missing Data Strategy

When data is unavailable:
1. Set the field value to `null`
2. Set confidence to `0.30`
3. Add the field name to `data_gaps_identified` array
4. Note in `generation_notes` what data would improve assessment

### Credit Workflow Example

```
Incoming request:
{
  "source_system": "credit_workflow",
  "request_type": "climate_scorecard_generation",
  "counterparty": {
    "name": "ABC Energy Ltd",
    "sector": "Oil & Gas",
    "country": "United Kingdom"
  },
  "credit_application": {
    "id": "CA-2025-001234",
    "credit_request_amount": 50000000,
    "currency": "GBP"
  }
}

Claude response (JSON):
{
  "scorecard_data": {
    "assessment_type": "initial",
    "net_zero_target_exists": true,
    "net_zero_target_year": 2050,
    "net_zero_science_based": false,
    "net_zero_score": 3,
    // ... all 80 fields
    "overall_climate_risk_rating": "C",
    "key_risk_drivers": [
      "High stranded asset exposure",
      "Carbon pricing risk in UK ETS"
    ]
  },
  "confidence_scores": {
    "net_zero_target_exists": 0.90,
    "net_zero_target_year": 0.90,
    "net_zero_science_based": 0.85,
    // ... confidence for each field
  },
  "generation_notes": "Assessment based on ABC Energy 2024 Annual Report, TCFD Report, and MSCI ESG rating. Data gaps in Scope 3 emissions and adaptation investments."
}
```

### Python Integration

Use the `credit_workflow_output` module for programmatic integration:

```python
from credit_workflow_output import (
    is_credit_workflow_request,
    parse_credit_workflow_request,
    generate_credit_workflow_response,
    CreditWorkflowOutput
)

# Check if request is from credit workflow
if is_credit_workflow_request(request_data):
    parsed = parse_credit_workflow_request(request_data)

    # Generate scorecard (using existing EnhancedClimateScorecard)
    scorecard = EnhancedClimateScorecard(...)
    # ... populate scorecard

    # Generate JSON response
    json_response = generate_credit_workflow_response(scorecard)
    return json_response
```

## Related Skills
- **itc-template-filler** - For project approval templates
- **icc-business-case-filler** - For business case templates
- **meeting-minutes** - For structuring ESG committee notes
- **status-reporter** - For ongoing climate risk monitoring

## Policy References
- Environmental Risk Policy v4.0 (March 2025)
- Credit Rating & Support Policy
- **PRA SS5/25 - Enhancing banks' and insurers' approaches to managing climate-related risks** (December 2025, replaces SS3/19)
- BCBS Principles for effective management and supervision of climate-related financial risks
- ISSB IFRS S2 Climate-related Disclosures
- MAS Guidelines on Environmental Risk Management
