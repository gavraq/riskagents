# Pillar Stress Scenario Generator - Complete Reference

**Skill Name**: `pillar-stress-generator`
**Purpose**: Create and review top-down "pillar stress" scenarios for market risk management
**Status**: Production Ready (v1.0)
**Last Updated**: 2025-11-12

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [What Are Pillar Stress Scenarios?](#what-are-pillar-stress-scenarios)
3. [How It Works](#how-it-works)
4. [Bundled Modules](#bundled-modules)
5. [Scenario Types & Templates](#scenario-types--templates)
6. [Risk Factor Library](#risk-factor-library)
7. [Validation Framework](#validation-framework)
8. [Real-World Examples](#real-world-examples)
9. [MLRC Governance Process](#mlrc-governance-process)
10. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Creating a New Scenario

```
Create a stress scenario for a Middle East oil supply disruption.
The trigger is regional conflict disrupting 3 million barrels/day through shipping lanes.
Make it a severe scenario lasting 6+ months.
```

The skill will:
1. ✅ Generate economic narrative with trigger event and transmission channels
2. ✅ Parameterize shocks for all 5 asset classes (Rates/FX, Credit, Energy, Precious Metals, Base Metals)
3. ✅ Validate correlation consistency and shock magnitudes
4. ✅ Generate Front Office consultation prompts
5. ✅ Produce MLRC-formatted Word document
6. ✅ Create validation report with confidence score

### Annual Review of Existing Scenario

```
Review the "Financial Crisis 2024" scenario for annual assessment.
Market changes: volatility regime shifted higher, EM spreads compressed.
System changes: Base Metals migrating to new system, Precious Metals vol shocks now relative.
Trading changes: Iron Ore discontinued, Cobalt added for Base Metals.
```

The skill will:
1. ✅ Assess each asset class for continued relevance
2. ✅ Detect parameter changes needed (market/system/trading)
3. ✅ Propose updates with rationale
4. ✅ Generate MLRC review memo
5. ✅ Recommend: approve as-is / with changes / major revision

### What You Get

**For New Scenarios**:
- Complete JSON parameterization file
- MLRC Word document (governance format)
- Validation report with confidence score (typically 60-80%)
- Front Office consultation prompts by desk

**For Annual Reviews**:
- Asset class review assessments
- Change proposals with rationale
- MLRC review memo (markdown format)
- Recommendation (approve as-is / with changes / major revision)

---

## What Are Pillar Stress Scenarios?

### Definition

**Pillar Stress Scenarios** are top-down, macro-economic stress scenarios that test the resilience of the entire trading portfolio across multiple asset classes. They represent plausible-but-severe market disruptions calibrated to historical precedents.

### Key Characteristics

1. **Top-Down**: Start with macro narrative, cascade to risk factors
2. **Comprehensive**: Cover all 5 asset classes (Rates/FX, Credit, Energy, Precious Metals, Base Metals)
3. **Severe**: Target ~100% severity (equivalent to 2008, 2020 events)
4. **Coherent**: Correlation patterns must be internally consistent
5. **Historically-Calibrated**: Shocks based on observed crisis magnitudes

### Contrast with PoW (Point of Weakness) Scenarios

| Feature | Pillar Stress | PoW Stress |
|---------|---------------|------------|
| **Approach** | Top-down (macro → risk factors) | Bottom-up (strategy → relevant risks) |
| **Scope** | Full portfolio, all asset classes | Specific trading strategy |
| **Severity** | Severe (~100%, 2008/2020-like) | Moderate-Severe (strategy-specific) |
| **Frequency** | Annual review, ad hoc for major events | Quarterly or on strategy changes |
| **Governance** | MLRC approval required | MLRC noting (unless material) |
| **Example** | "Global Recession with Banking Crisis" | "Flattening of USD curve (2Y-10Y)" |

### Regulatory Context

- **PRA SS13/13**: Supervisory expectations for stress testing
- **BCBS Standards**: Basel stress testing framework
- **ICBC Market Risk Policy (June 2025)**: Section 9.2.1 - Stress Testing
- **Stress Testing Framework (v5.2, Sep 2024)**: Section 5.4 - Annual review requirements

---

## How It Works

### Workflow: New Scenario Creation

```
1. Define Scenario Narrative
   ├── Trigger event (e.g., "Fed overtightens monetary policy")
   ├── Scenario type (recession, inflation shock, supply disruption, etc.)
   ├── Severity (moderate / severe / extreme)
   ├── Primary geography (US, EUR, global, etc.)
   └── Narrative elements (policy_error, banking_stress, etc.)
        ↓
2. Generate Transmission Channels
   ├── How does trigger event propagate?
   ├── What are the key economic mechanisms?
   ├── Which asset classes are affected first?
   └── What are the second-order effects?
        ↓
3. Parameterize Risk Factor Shocks
   ├── Load scenario type template
   ├── Apply severity scaling (60% / 100% / 150%)
   ├── Adjust for geography (DM vs EM, regional focus)
   ├── Calibrate to historical precedents
   └── Apply narrative-specific adjustments
        ↓
4. Validate Consistency
   ├── Correlation patterns (risk-off, inflation shock, commodity links)
   ├── Magnitude limits (vs historical maximums)
   ├── Tenor structure logic (curve shape, policy expectations)
   ├── Regional differentiation (safe havens, contagion)
   └── Completeness (all asset classes covered)
        ↓
5. Generate Consultation Prompts
   ├── Identify affected trading desks
   ├── Generate desk-specific questions
   ├── Flag unusual or extreme parameters
   └── Request feedback on scenario relevance
        ↓
6. Build MLRC Documentation
   ├── Cover sheet with meeting details
   ├── Background and economic narrative
   ├── Asset class sections with shock tables
   ├── Validation results and warnings
   ├── Front Office consultation section
   └── Formal governance sections
        ↓
7. Output & Review
   ├── JSON parameterization file
   ├── MLRC Word document
   ├── Validation report (markdown)
   └── Confidence score (60-80% typical)
```

### Workflow: Annual Review

```
1. Load Existing Scenario
   ├── Read current parameterization
   ├── Load historical context
   └── Understand scenario intent
        ↓
2. Assess Market Changes
   ├── Have risk factor relationships shifted?
   ├── Are volatility regimes different?
   ├── Have spreads compressed/widened structurally?
   └── Are correlations still representative?
        ↓
3. Assess System Changes
   ├── Platform migrations or other shystem changes
   ├── Calculation methodology changes
   ├── Data source updates
   └── Risk model enhancements
        ↓
4. Assess Trading Changes
   ├── Products discontinued
   ├── New products added
   ├── Desk structure changes
   └── Strategy shifts
        ↓
5. Propose Changes by Asset Class
   ├── No change (scenario still relevant)
   ├── Minor adjustment (update specific parameters)
   ├── Major revision (re-parameterize)
   └── Provide rationale for each
        ↓
6. Generate Review Memo
   ├── Background and context
   ├── Asset class assessments
   ├── Change proposals with rationale
   ├── Overall recommendation
   └── MLRC-formatted markdown
```

### Confidence Scoring

The skill assigns confidence scores based on:

| Factor | Weight | Impact |
|--------|--------|--------|
| **Scenario Type** | 40% | Known types (recession, 2008-like) = higher confidence; Novel types = lower |
| **Historical Precedent** | 30% | Strong historical analogue (2008, 2020) = higher; Unprecedented = lower |
| **Severity** | 20% | Moderate/Severe = higher; Extreme = lower (requires more justification) |
| **Validation Results** | 10% | Zero errors = bonus; Warnings = slight penalty |

**Typical Scores**:
- **80-90%**: Well-established scenario type (recession, financial crisis) with strong historical precedent
- **60-80%**: Novel combination or geography but reasonable calibration (most pillar scenarios)
- **40-60%**: Unprecedented scenario type or extreme severity requiring expert review
- **<40%**: Missing critical data or severe validation errors

---

## Bundled Modules

The skill includes 7 Python modules totaling **~3,200 lines of code**:

### 1. parameterization_engine.py (435 lines)

**Purpose**: Suggest risk factor shocks based on scenario type, severity, and narrative

**Key Classes**:
```python
class ScenarioType(Enum):
    RECESSION = "recession"
    INFLATION_SHOCK = "inflation_shock"
    SUPPLY_DISRUPTION = "supply_disruption"
    FINANCIAL_CRISIS = "financial_crisis"
    POLICY_ERROR = "policy_error"
    CHINA_SLOWDOWN = "china_slowdown"
    GEOPOLITICAL = "geopolitical"
    SOVEREIGN_CRISIS = "sovereign_crisis"
    PANDEMIC = "pandemic"
    CLIMATE = "climate"

class Severity(Enum):
    MODERATE = "moderate"  # 60% scaling
    SEVERE = "severe"      # 100% scaling (target)
    EXTREME = "extreme"    # 150% scaling

class ParameterizationEngine:
    def suggest_scenario_shocks(
        self,
        scenario_type: ScenarioType,
        severity: Severity,
        primary_geography: str,
        narrative_elements: List[str],
        custom_adjustments: Optional[Dict] = None
    ) -> Dict[str, List[RiskFactorShock]]:
        """Returns suggested shocks for all asset classes"""
```

**Usage**:
```python
from parameterization_engine import ParameterizationEngine, ScenarioType, Severity

engine = ParameterizationEngine(data_dir=Path("data"))

shocks = engine.suggest_scenario_shocks(
    scenario_type=ScenarioType.POLICY_ERROR,
    severity=Severity.SEVERE,
    primary_geography="US",
    narrative_elements=["policy_error", "recession"]
)

# Returns dict with keys: rates_fx, credit, energy, precious_metals, base_metals
```

### 2. validators.py (523 lines)

**Purpose**: Validate scenario consistency (correlation, magnitude, tenor structure)

**Key Classes**:
```python
class ValidationLevel(Enum):
    ERROR = "error"      # Must fix before MLRC submission
    WARNING = "warning"  # Review recommended
    INFO = "info"        # Informational

class ScenarioValidator:
    def validate_scenario(
        self,
        scenario_shocks: Dict[str, Any],
        scenario_type: str,
        severity: str
    ) -> List[ValidationResult]:
        """Returns list of validation findings"""

    def generate_validation_report(
        self,
        validation_results: List[ValidationResult]
    ) -> str:
        """Returns markdown validation report"""
```

**Validation Checks**:
1. **Correlation Consistency**:
   - Risk-off pattern: USD/JPY/CHF strengthen, EM weaken, equities down, spreads widen
   - Inflation shock: rates up, commodities up, FX mixed
   - Commodity links: oil/gas correlation, energy/precious metals

2. **Magnitude Limits**:
   - Compare to historical maximums (2008 = 600bp credit, 80% oil)
   - Flag if >150% of historical maximum
   - Warn if >120% of historical maximum

3. **Tenor Structure**:
   - Curve shape logic (flattening in recession, steepening in recovery)
   - Policy expectations (short end responds to CB, long end to growth)
   - Term premium consistency

4. **Regional Differentiation**:
   - DM vs EM spread differences
   - Safe haven flows (USD, JPY, CHF, EUR core)
   - Contagion patterns

5. **Completeness**:
   - All asset classes covered
   - Major currencies included (USD, EUR, GBP, JPY, etc.)
   - All tenors specified (O/N through 30Y)

**Usage**:
```python
from validators import ScenarioValidator

validator = ScenarioValidator()

validation_results = validator.validate_scenario(
    scenario_shocks=shocks,
    scenario_type="policy_error",
    severity="severe"
)

# Check for errors
errors = [v for v in validation_results if v.level == ValidationLevel.ERROR]
if errors:
    print("❌ Scenario has validation errors:")
    for error in errors:
        print(f"  - {error.message}")

# Generate report
report = validator.generate_validation_report(validation_results)
print(report)
```

### 3. scenario_designer.py (789 lines)

**Purpose**: Complete new scenario creation workflow

**Key Classes**:
```python
@dataclass
class ScenarioMetadata:
    scenario_name: str
    scenario_type: str
    severity: str
    primary_geography: str
    created_by: str
    created_date: str
    version: str

@dataclass
class EconomicNarrative:
    trigger_event: str
    narrative_text: str
    transmission_channels: List[str]
    key_assumptions: List[str]
    timeline: Dict[str, str]

@dataclass
class AssetClassShocks:
    asset_class: str
    description: str
    rationale: str
    shocks: Dict[str, Any]
    historical_analogue: Optional[str]
    confidence: float

@dataclass
class StressScenario:
    metadata: ScenarioMetadata
    narrative: EconomicNarrative
    asset_class_shocks: List[AssetClassShocks]
    validation_results: List[ValidationResult]
    consultation_prompts: Dict[str, List[str]]
    confidence_score: float
    next_steps: List[str]

class ScenarioDesigner:
    def create_scenario(
        self,
        scenario_name: str,
        trigger_event: str,
        scenario_type: ScenarioType,
        severity: Severity,
        primary_geography: str,
        narrative_elements: List[str],
        transmission_channels: List[str],
        key_assumptions: List[str],
        timeline: Optional[Dict[str, str]] = None,
        created_by: str = "Market Risk",
        custom_shocks: Optional[Dict] = None
    ) -> StressScenario:
        """Returns complete StressScenario object"""
```

**Usage**:
```python
from scenario_designer import ScenarioDesigner, ScenarioType, Severity

designer = ScenarioDesigner(data_dir=Path("data"))

scenario = designer.create_scenario(
    scenario_name="US Recession with Fed Policy Error",
    trigger_event="Federal Reserve overtightens monetary policy despite weakening economy",
    scenario_type=ScenarioType.POLICY_ERROR,
    severity=Severity.SEVERE,
    primary_geography="US",
    narrative_elements=["policy_error", "recession"],
    transmission_channels=[
        "Fed raises rates 50bps despite negative GDP",
        "Corporate credit spreads widen sharply",
        "USD strengthens on rate differentials"
    ],
    key_assumptions=[
        "Fed prioritizes inflation target over growth",
        "Corporate sector overleveraged"
    ],
    timeline={
        "onset": "Q1 2025 - Fed hikes despite weak data",
        "peak": "Q2-Q3 2025 - Recession materializes",
        "recovery": "Q4 2025-Q1 2026 - Fed pivots"
    }
)

# Save scenario
output_file = designer.save_scenario(scenario, output_dir)
print(f"Scenario saved to: {output_file}")
print(f"Confidence: {scenario.confidence_score:.0f}%")
```

### 4. scenario_reviewer.py (518 lines)

**Purpose**: Annual review workflow for existing scenarios

**Key Classes**:
```python
class ChangeType(Enum):
    NO_CHANGE = "no_change"
    MINOR_ADJUSTMENT = "minor_adjustment"
    MAJOR_REVISION = "major_revision"

@dataclass
class AssetClassReview:
    asset_class: str
    change_type: ChangeType
    rationale: str
    proposed_parameters: Optional[Dict[str, Any]]
    affected_products: Optional[List[str]]
    system_changes: Optional[List[str]]

@dataclass
class ScenarioReviewResult:
    scenario_name: str
    reviewer: str
    review_date: str
    market_changes_since_last_review: List[str]
    system_changes: List[str]
    trading_changes: Dict[str, List[str]]
    asset_class_reviews: List[AssetClassReview]
    recommended_action: str  # "approve_as_is", "approve_with_changes", "major_revision_needed"

class ScenarioReviewer:
    def review_scenario(
        self,
        scenario_name: str,
        reviewer: str = "Market Risk",
        market_changes: Optional[List[str]] = None,
        system_changes: Optional[List[str]] = None,
        trading_changes: Optional[Dict[str, List[str]]] = None
    ) -> ScenarioReviewResult:
        """Returns review assessment with change proposals"""
```

**Usage**:
```python
from scenario_reviewer import ScenarioReviewer

reviewer = ScenarioReviewer(data_dir=Path("data"))

review_result = reviewer.review_scenario(
    scenario_name="Financial Crisis 2025",
    reviewer="Market Risk",
    market_changes=[
        "Volatility regime shifted higher vs 2024",
        "EM spreads compressed significantly"
    ],
    system_changes=[
        "Base Metals migrating to Murex (target 2025)",
        "Precious Metals vol shocks changed to relative"
    ],
    trading_changes={
        "Base Metals": [
            "Iron Ore trading discontinued",
            "Cobalt trading added"
        ]
    }
)

# Generate review memo
memo = reviewer.generate_review_memo(review_result)
print(memo)
```

### 5. mlrc_document_builder.py (484 lines)

**Purpose**: Generate MLRC-formatted Word documents

**Key Classes**:
```python
class MLRCDocumentBuilder:
    def create_new_scenario_document(
        self,
        scenario: StressScenario,
        meeting_date: str,
        presenter: str = "Market Risk"
    ) -> Document:
        """Returns python-docx Document for new scenario"""

    def create_annual_review_document(
        self,
        review_result: ScenarioReviewResult,
        meeting_date: str
    ) -> Document:
        """Returns python-docx Document for annual review"""
```

**Document Structure (New Scenario)**:
1. **Cover Sheet**:
   - Document Name
   - Meeting Date (MLRC)
   - Presenter
   - Context
   - Purpose

2. **Background**:
   - Trigger Event
   - Economic Narrative
   - Key Assumptions

3. **Asset Class Sections** (5 sections):
   - Description
   - Rationale
   - Historical Analogue
   - Proposed Shocks (table format)

4. **Validation Results**:
   - Errors (red, must address)
   - Warnings (orange, review recommended)

5. **Front Office Consultation**:
   - Desk-specific questions
   - Parameter feedback requests

6. **Conclusions**:
   - Confidence Score
   - Next Steps

7. **References**:
   - ICBCS Stress Testing Parameterisation

8. **Document History**:
   - Prepared by
   - Date
   - Reviewed by 2nd line

9. **Formal Governance**:
   - Reviewing committee
   - Outcome (to be completed post-MLRC)
   - Actions (to be completed post-MLRC)

**Usage**:
```python
from mlrc_document_builder import MLRCDocumentBuilder

builder = MLRCDocumentBuilder()

# For new scenario
doc = builder.create_new_scenario_document(
    scenario=scenario,
    meeting_date="15 December 2025",
    presenter="Market Risk"
)

# Save
output_path = Path("outputs/US_Recession_MLRC.docx")
builder.document = doc
builder.save_document(output_path)
```

### 6. test_scenarios.py (319 lines)

**Purpose**: Comprehensive test suite for all functionality

**Test Scenarios**:
1. **US Recession with Fed Policy Error** (policy_error, severe, US)
2. **Middle East Oil Supply Disruption** (supply_disruption, severe, global)
3. **EUR Sovereign Crisis 2.0** (recession, severe, EUR)
4. **Annual Review** (Financial Crisis 2025)

**Usage**:
```bash
cd .claude/skills/pillar-stress-generator/
python test_scenarios.py
```

**Expected Output**:
```
================================================================================
PILLAR STRESS SCENARIO GENERATOR - TEST SUITE
================================================================================

TEST 1: Creating US Recession with Fed Policy Error scenario...
   📄 Scenario saved to: test_output/test1/us_recession_with_fed_policy_error_20251112.json
   📊 Asset classes: 5
   ✅ Validation: 0 errors, 1 warning
   🎯 Confidence: 60%
✅ Test 1 Complete - Confidence Score: 60%

TEST 2: Creating Middle East Oil Supply Disruption scenario...
   📄 Scenario saved to: test_output/test2/middle_east_oil_supply_disruption_20251112.json
   📊 Asset classes: 5
   ✅ Validation: 0 errors, 1 warning
   🎯 Confidence: 70%
✅ Test 2 Complete - Confidence Score: 70%

TEST 3: Creating EUR Sovereign Crisis 2.0 scenario...
   📄 Scenario saved to: test_output/test3/eur_sovereign_crisis_2.0_20251112.json
   📊 Asset classes: 5
   ✅ Validation: 0 errors, 1 warning
   🎯 Confidence: 80%
✅ Test 3 Complete - Confidence Score: 80%

TEST 4: Conducting annual review of existing scenario...
   📄 Review memo saved to: test_output/test4/annual_review_memo.md
   📊 Asset classes reviewed: 5
   🔄 Changes proposed: 3
   ✅ Recommendation: major_revision_needed
✅ Test 4 Complete - Recommendation: major_revision_needed

================================================================================
✅ ALL TESTS PASSED - No validation errors detected
================================================================================
```

### 7. build_risk_factor_library.py

**Purpose**: Extract risk factor data from production Excel file and structure for use

**Functionality**:
- Reads "Stress testing shocks - detailed breakdown.xlsx"
- Extracts 473 rate curves across 191 currencies
- Extracts 271 FX pairs
- Supplements with Credit, Energy, Precious/Base Metals from policy docs
- Outputs structured JSON library

---

## Scenario Types & Templates

The skill supports 10 scenario types, each with pre-configured shock templates:

### 1. Recession

**Typical Pattern**:
- **Rates**: Flight to quality (core DM rates down, peripheral up)
- **FX**: USD/JPY/CHF strengthen (safe havens), EM weaken
- **Credit**: Spreads widen (IG +150bp, HY +300bp)
- **Energy**: Demand destruction (oil -30%)
- **Precious Metals**: Gold up (safe haven), industrial metals down
- **Base Metals**: Copper/aluminum down (demand destruction)

**Historical Examples**: 2008 Financial Crisis, 2020 COVID-19

**Severity Scaling**:
- Moderate (60%): 2015 China slowdown-like
- Severe (100%): 2008/2020-like
- Extreme (150%): Beyond historical precedent

### 2. Inflation Shock

**Typical Pattern**:
- **Rates**: Sharp rises across curve (CB tightening)
- **FX**: USD strengthens (Fed leads tightening)
- **Credit**: Spreads widen (higher discount rates)
- **Energy**: Oil/gas rise (inflation driver)
- **Precious Metals**: Gold mixed (inflation vs real rates)
- **Base Metals**: Depends on growth outlook

**Historical Examples**: 1970s stagflation, 2022 post-COVID inflation

### 3. Supply Disruption

**Typical Pattern**:
- **Rates**: Short end up (CB response), long end mixed
- **FX**: Energy exporters strengthen, importers weaken
- **Credit**: Energy sector tightens, others stable
- **Energy**: Massive spike (50-80%)
- **Precious Metals**: Follow energy complex
- **Base Metals**: Mixed (supply vs demand)

**Historical Examples**: 2022 Russia-Ukraine War (energy), 1973 Oil Crisis

### 4. Financial Crisis

**Typical Pattern**:
- **Rates**: Policy rates slashed, long end down (recession fears)
- **FX**: Extreme safe haven flows, EM collapse
- **Credit**: Spreads blow out (especially financials)
- **Energy**: Collapse (demand destruction)
- **Precious Metals**: Gold up sharply (crisis hedge)
- **Base Metals**: Industrial demand collapses

**Historical Examples**: 2008 Lehman Crisis, 2011 EUR Sovereign Crisis

### 5. Policy Error

**Typical Pattern**:
- **Rates**: Initial tightening, then reversal expectations
- **FX**: Initial policy currency strength, then reversal
- **Credit**: Spreads widen (policy mistake → recession)
- **Energy**: Mixed (depends on growth impact)
- **Precious Metals**: Gold up (policy uncertainty)
- **Base Metals**: Down (growth concerns)

**Historical Examples**: 1994 Fed "speed tightening", 2018 Q4 "autopilot" error

### 6. China Slowdown

**Typical Pattern**:
- **Rates**: Core DM rally (flight to quality), China cuts
- **FX**: CNY/CNH weaken, EM Asia contagion, AUD/NZD down
- **Credit**: China IG/HY widen, commodities exporters widen
- **Energy**: Demand shock (China = 15% global demand)
- **Precious Metals**: Mixed (safe haven vs industrial demand)
- **Base Metals**: Severe (China = 50% global copper demand)

**Historical Examples**: 2015-2016 China equity crash + devaluation

### 7. Geopolitical

**Typical Pattern** (varies by region):
- **Rates**: Safe havens rally, affected region rises
- **FX**: Regional currencies weaken, safe havens strengthen
- **Credit**: Regional spreads widen
- **Energy**: Depends on region (Middle East = spike)
- **Precious Metals**: Gold up (uncertainty)
- **Base Metals**: Mixed

**Historical Examples**: 2022 Russia-Ukraine, 2011 Arab Spring, 2020 US-China trade war

### 8. Sovereign Crisis

**Typical Pattern**:
- **Rates**: Affected sovereigns spike, safe havens rally
- **FX**: Affected currency collapses, EUR/USD down
- **Credit**: Sovereign spreads blow out, sovereign-bank doom loop
- **Energy**: Mixed
- **Precious Metals**: Gold up
- **Base Metals**: Down (Euro area demand)

**Historical Examples**: 2011-2012 EUR Sovereign Debt Crisis (Greece, Italy, Spain)

### 9. Pandemic

**Typical Pattern**:
- **Rates**: Collapse (CB easing + recession)
- **FX**: USD initially up (liquidity), then down (Fed easing)
- **Credit**: Initial blow-out, then CB support
- **Energy**: Severe demand destruction
- **Precious Metals**: Gold up sharply
- **Base Metals**: Initial collapse, then recovery on stimulus

**Historical Examples**: 2020 COVID-19

### 10. Climate (Transition or Physical)

**Typical Pattern** (emerging):
- **Rates**: Depends on policy response (carbon pricing = inflation?)
- **FX**: Energy importers benefit, fossil exporters suffer
- **Credit**: Fossil fuel sectors widen, green sectors tighten
- **Energy**: Depends on transition scenario (oil down long-term)
- **Precious Metals**: Mixed
- **Base Metals**: Copper/lithium up (green transition)

**Historical Examples**: Limited (2021 EU carbon price spike most relevant)

---

## Risk Factor Library

The skill includes a comprehensive library extracted from production systems:

### Rates & FX

**Coverage**:
- **473 rate curves** across **191 currencies/regions**
- **18 tenor points**: O/N, 1W, 1M, 2M, 3M, 6M, 9M, 1Y, 18M, 2Y, 3Y, 4Y, 5Y, 7Y, 10Y, 15Y, 20Y, 30Y
- **271 FX pairs** (spot + forward points)

**Example Structure** (JSON):
```json
{
  "asset_class": "rates_fx",
  "scenarios": {
    "financial_crisis_2008": {
      "rates": {
        "USD": {
          "curve_type": "government",
          "shocks_bps": {
            "O/N": -500,
            "3M": -450,
            "2Y": -200,
            "10Y": -100,
            "30Y": -50
          }
        }
      },
      "fx": {
        "EURUSD": {
          "spot_shock_pct": -15.2,
          "rationale": "Flight to USD safe haven"
        }
      }
    }
  }
}
```

**Key Currencies**:
- **G10**: USD, EUR, GBP, JPY, CHF, CAD, AUD, NZD, NOK, SEK
- **EM Asia**: CNY, CNH, HKD, SGD, KRW, TWD, INR, IDR, MYR, THB, PHP
- **EM EMEA**: TRY, ZAR, RUB, PLN, CZK, HUF, ILS, EGP
- **EM Latam**: BRL, MXN, CLP, COP, PEN, ARS

### Credit

**Coverage**:
- **10 regions**: US, EUR, UK, Japan, EM Asia, EM EMEA, EM Latam, Aus/NZ, Canada, China
- **13 sectors**: Financials, Energy, Basic Materials, Industrials, Consumer Cyclical, Consumer Non-Cyclical, Technology, Telecom, Utilities, Real Estate, Government, Sovereign, Other

**Structure**:
```json
{
  "asset_class": "credit",
  "regions": ["US", "EUR", "UK", "Japan", ...],
  "sectors": ["Financials", "Energy", ...],
  "scenarios": {
    "financial_crisis_2008": {
      "US": {
        "Financials": {
          "IG_spread_shock_bps": 600,
          "HY_spread_shock_bps": 1200,
          "rationale": "Banking sector stress, counterparty risk"
        },
        "Energy": {
          "IG_spread_shock_bps": 300,
          "HY_spread_shock_bps": 800,
          "rationale": "Oil price collapse, credit concerns"
        }
      }
    }
  }
}
```

### Energy

**Coverage**: 6 products
- WTI Crude Oil
- Brent Crude Oil
- Natural Gas (Henry Hub)
- Gas Oil
- Heating Oil
- Gasoline (RBOB)

**Structure**:
```json
{
  "asset_class": "energy",
  "products": ["WTI", "Brent", "NatGas", ...],
  "scenarios": {
    "oil_supply_disruption_2022": {
      "WTI": {
        "price_shock_pct": 52,
        "rationale": "Russia-Ukraine war, sanctions on Russian oil"
      },
      "NatGas": {
        "price_shock_pct": 60,
        "rationale": "European gas shortage, pipeline disruption"
      }
    }
  }
}
```

### Precious Metals

**Coverage**: 5 products
- Gold (XAU)
- Silver (XAG)
- Platinum (XPT)
- Palladium (XPD)
- Rhodium (XRH)

**Structure**:
```json
{
  "asset_class": "precious_metals",
  "products": ["Gold", "Silver", "Platinum", "Palladium", "Rhodium"],
  "scenarios": {
    "financial_crisis_2008": {
      "Gold": {
        "price_shock_pct": 25,
        "rationale": "Flight to safety, central bank reserves"
      },
      "Platinum": {
        "price_shock_pct": -35,
        "rationale": "Industrial demand collapse (auto catalysts)"
      }
    }
  }
}
```

### Base Metals

**Coverage**: 8 products
- Copper (HG)
- Aluminum (ALI)
- Zinc (ZNC)
- Nickel (NI)
- Lead (LLN)
- Tin (SN)
- Cobalt (CO) [recently added]
- Iron Ore [recently discontinued]

**Structure**:
```json
{
  "asset_class": "base_metals",
  "products": ["Copper", "Aluminum", "Zinc", ...],
  "scenarios": {
    "china_slowdown_2015": {
      "Copper": {
        "price_shock_pct": -40,
        "rationale": "China = 50% global demand, construction slowdown"
      },
      "Aluminum": {
        "price_shock_pct": -25,
        "rationale": "Industrial production decline"
      }
    }
  }
}
```

---

## Validation Framework

The skill includes comprehensive validation across 5 dimensions:

### 1. Correlation Consistency

**Risk-Off Pattern** (recession, financial crisis):
```
✅ Rates: Core DM down, peripheral up
✅ FX: USD/JPY/CHF up, EM down
✅ Credit: Spreads widen
✅ Equities: Down
✅ Commodities: Down (except gold)

❌ ERROR: USD weakens in recession (contradicts risk-off)
⚠️ WARNING: Gold down in financial crisis (unusual, not error)
```

**Inflation Shock Pattern**:
```
✅ Rates: Up across curve
✅ FX: USD mixed (depends on relative policy)
✅ Credit: Spreads widen (higher discount rates)
✅ Commodities: Up (inflation driver)

❌ ERROR: Rates down in inflation shock (contradicts CB response)
```

**Commodity Links**:
```
✅ Oil and Gas: Highly correlated (energy complex)
✅ Copper and Aluminum: Correlated (industrial metals)
✅ Gold and Silver: Somewhat correlated (precious metals)

⚠️ WARNING: Oil up 50%, Gas down 20% (unusual divergence)
```

### 2. Magnitude Limits

**Historical Maximums** (used as benchmarks):

| Risk Factor | 2008 Crisis | 2020 COVID | 2022 Ukraine | Maximum Ever |
|-------------|-------------|------------|--------------|--------------|
| **USD 10Y** | -100bp | -150bp | +200bp | -150bp (down) |
| **EUR 10Y** | -50bp | -80bp | +150bp | -80bp (down) |
| **EURUSD** | -15% | -5% | +8% | -25% (1985) |
| **IG Credit** | +600bp | +250bp | +100bp | +600bp |
| **HY Credit** | +1200bp | +800bp | +200bp | +1500bp (2008) |
| **WTI Oil** | -70% | -60% | +52% | -70% (down), +200% (up, 1973) |
| **Gold** | +25% | +30% | +10% | +50% (1979) |
| **Copper** | -60% | -30% | -15% | -60% (2008) |

**Validation Logic**:
```
If shock > 150% of historical maximum:
  → ❌ ERROR: "Exceeds historical precedent by >50%"

If shock > 120% of historical maximum:
  → ⚠️ WARNING: "Exceeds historical precedent, requires strong justification"

If shock > 100% but < 120% of historical maximum:
  → ℹ️ INFO: "At upper end of historical range"
```

### 3. Tenor Structure Logic

**Recession (Policy Easing Expected)**:
```
✅ Correct: Short end down more than long end (curve steepens)
   - 2Y: -200bp
   - 10Y: -100bp
   - 30Y: -50bp

❌ ERROR: Short end down less than long end (curve flattens in recession)
   - 2Y: -50bp
   - 10Y: -100bp
   - 30Y: -150bp
```

**Inflation Shock (Policy Tightening Expected)**:
```
✅ Correct: Short end up more than long end (curve flattens)
   - 2Y: +200bp
   - 10Y: +100bp
   - 30Y: +50bp

❌ ERROR: Short end up less than long end (curve steepens in inflation shock)
```

**Bear Flattening vs Bull Steepening**:
```
Bear Flattening (hawkish CB): 2Y↑↑, 10Y↑, 30Y→
Bull Steepening (dovish CB): 2Y↓↓, 10Y↓, 30Y→
Bear Steepening (stagflation): 2Y↑, 10Y↑↑, 30Y↑↑↑
Bull Flattening (disinflation): 2Y↓, 10Y↓↓, 30Y↓
```

### 4. Regional Differentiation

**Safe Haven Flows**:
```
✅ Correct (Global stress):
   - USD: +10%
   - JPY: +8%
   - CHF: +12%
   - EUR (core): +5%
   - GBP: -5%
   - EM Asia: -15%
   - EM EMEA: -20%

❌ ERROR: CHF weakens in global stress (safe haven should strengthen)
⚠️ WARNING: EM strengthens in risk-off (unusual, needs strong rationale)
```

**DM vs EM Spread Differentiation**:
```
✅ Correct (Financial crisis):
   - US IG: +150bp
   - US HY: +400bp
   - EM IG: +300bp (wider than DM)
   - EM HY: +800bp (wider than DM)

❌ ERROR: EM spreads tighter than DM in crisis
```

### 5. Completeness

**Required Asset Classes**:
- ✅ Rates & FX (at least G10 + major EM)
- ✅ Credit (at least US, EUR, EM regions)
- ✅ Energy (at least WTI, Brent, NatGas)
- ✅ Precious Metals (at least Gold, Silver)
- ✅ Base Metals (at least Copper, Aluminum)

**Required Tenors** (Rates):
- ✅ Policy rate (O/N or 1M)
- ✅ Short end (2Y)
- ✅ Belly (5Y, 10Y)
- ✅ Long end (30Y if available)

---

## Real-World Examples

### Example 1: US Recession with Fed Policy Error

**Scenario Description**:
Federal Reserve overtightens monetary policy despite weakening economy, triggering a hard landing. Fed raises rates 50bps despite negative GDP print and labor market weakness. Corporate credit spreads widen sharply as refinancing becomes problematic.

**Inputs**:
```python
scenario = designer.create_scenario(
    scenario_name="US Recession with Fed Policy Error",
    trigger_event="Federal Reserve overtightens monetary policy despite weakening economy, triggering hard landing",
    scenario_type=ScenarioType.POLICY_ERROR,
    severity=Severity.SEVERE,
    primary_geography="US",
    narrative_elements=["policy_error", "recession"],
    transmission_channels=[
        "Fed raises rates 50bps despite negative GDP print and labor market weakness",
        "Corporate credit spreads widen sharply as refinancing becomes problematic",
        "USD strengthens on rate differentials despite US recession",
        "EM currencies depreciate on capital flight",
        "Equity markets decline on earnings downgrades and higher discount rates"
    ],
    key_assumptions=[
        "Fed prioritizes inflation target over growth",
        "Long and variable lags in monetary policy transmission",
        "Corporate sector overleveraged after years of low rates",
        "Labor market softens but inflation remains sticky at 3.5%"
    ],
    timeline={
        "onset": "Q1 2025 - Fed hikes despite weak data",
        "peak": "Q2-Q3 2025 - Recession materializes, credit stress emerges",
        "recovery": "Q4 2025-Q1 2026 - Fed pivots, gradual stabilization"
    }
)
```

**Outputs**:
- **Confidence Score**: 60%
- **Validation**: 0 errors, 1 warning (extreme USD strength vs recession)
- **Asset Classes Parameterized**: 5 (Rates/FX, Credit, Energy, Precious, Base)
- **Front Office Consultation Prompts**: 12 questions across 5 desks

**Key Shocks**:
- USD 2Y: +150bp (policy error)
- USD 10Y: +50bp (recession expectations limit long end)
- EURUSD: -8% (USD strengthens on rate differentials)
- US IG Credit: +200bp (corporate stress)
- US HY Credit: +500bp (refinancing concerns)
- WTI Oil: -25% (demand destruction)
- Gold: +15% (uncertainty hedge)
- Copper: -30% (recession)

**MLRC Document**: 8 pages, governance-ready format

### Example 2: Middle East Oil Supply Disruption

**Scenario Description**:
Regional conflict escalates, disrupting 3 million barrels/day of oil exports through critical shipping lanes. Oil prices spike 50% as supply is physically disrupted. Inflation expectations rise sharply, forcing central bank tightening.

**Inputs**:
```python
scenario = designer.create_scenario(
    scenario_name="Middle East Oil Supply Disruption",
    trigger_event="Regional conflict escalates, disrupting 3 million barrels/day of oil exports through critical shipping lanes",
    scenario_type=ScenarioType.SUPPLY_DISRUPTION,
    severity=Severity.SEVERE,
    primary_geography="global",
    narrative_elements=["oil_supply_shock", "inflation_expectations"],
    transmission_channels=[
        "Oil prices spike 50% as supply is physically disrupted",
        "Inflation expectations rise sharply, forcing central bank tightening",
        "Energy-importing economies see terms of trade deterioration",
        "Gas prices follow oil higher on energy complex correlation",
        "Consumer spending constrained by higher energy costs, growth slows"
    ],
    key_assumptions=[
        "Disruption lasts 6+ months (not quickly resolved)",
        "Strategic petroleum reserves provide limited buffer",
        "OPEC+ unable or unwilling to fully offset supply loss",
        "Limited demand destruction despite high prices"
    ],
    timeline={
        "onset": "Immediate - conflict escalation, shipping halt",
        "peak": "1-2 months - oil peaks at $135/bbl, policy response begins",
        "recovery": "6-12 months - diplomatic resolution, supply gradually restored"
    }
)
```

**Outputs**:
- **Confidence Score**: 70%
- **Validation**: 0 errors, 1 warning (gold behavior mixed)
- **Asset Classes Parameterized**: 5
- **Front Office Consultation Prompts**: 10 questions

**Key Shocks**:
- USD 2Y: +100bp (Fed tightens on inflation)
- EUR 2Y: +75bp (ECB follows)
- EURUSD: +5% (Euro area more exposed to Middle East oil)
- US IG Credit: +80bp (higher discount rates)
- WTI Oil: +50% (supply disruption)
- Brent Oil: +52% (slightly higher due to European exposure)
- NatGas: +35% (energy complex correlation)
- Gold: +10% (uncertainty, but real rates up)
- Copper: -15% (growth concerns)

**MLRC Document**: 9 pages

### Example 3: EUR Sovereign Crisis 2.0

**Scenario Description**:
Sovereign debt crisis re-emerges in peripheral EUR economies amid fiscal deterioration and political fragmentation. Peripheral sovereign spreads widen sharply (Italy, Spain, Portugal). Sovereign-bank doom loop re-emerges as banks hold government debt.

**Inputs**:
```python
scenario = designer.create_scenario(
    scenario_name="EUR Sovereign Crisis 2.0",
    trigger_event="Sovereign debt crisis re-emerges in peripheral EUR economies amid fiscal deterioration and political fragmentation",
    scenario_type=ScenarioType.SOVEREIGN_CRISIS,
    severity=Severity.SEVERE,
    primary_geography="EUR",
    narrative_elements=["sovereign_stress", "banking_stress"],
    transmission_channels=[
        "Peripheral sovereign spreads widen sharply (Italy, Spain, Portugal)",
        "Sovereign-bank doom loop re-emerges as banks hold government debt",
        "EUR depreciates on capital flight and ECB credibility concerns",
        "Credit spreads widen, especially for EUR financials",
        "Flight to quality into German Bunds and USD"
    ],
    key_assumptions=[
        "ECB constrained by inflation, cannot immediately ease",
        "Fiscal rules prevent aggressive national responses",
        "Political will for bailouts limited vs 2011-2012",
        "Contagion contained to EUR (limited global spillover)"
    ],
    timeline={
        "onset": "Q2 2025 - Sovereign debt auction fails, spreads spike",
        "peak": "Q3 2025 - Banking sector stress, EUR weakness accelerates",
        "recovery": "Q4 2025-Q1 2026 - ECB intervention, fiscal support package"
    }
)
```

**Outputs**:
- **Confidence Score**: 80% (strong historical precedent: 2011)
- **Validation**: 0 errors, 1 warning
- **Asset Classes Parameterized**: 5
- **Front Office Consultation Prompts**: 11 questions

**Key Shocks**:
- Germany 10Y: -80bp (flight to quality into Bunds)
- Italy 10Y: +250bp (sovereign stress)
- Spain 10Y: +200bp (contagion)
- EUR 10Y (avg): +50bp (weighted by spreads)
- EURUSD: -12% (capital flight)
- EUR Financials IG: +400bp (sovereign-bank doom loop)
- EUR Financials HY: +800bp
- Other EUR IG: +150bp
- WTI Oil: -15% (Euro area demand)
- Gold: +18% (crisis hedge)
- Copper: -20% (Euro area demand)

**MLRC Document**: 10 pages, includes section on ECB policy constraints

### Example 4: Annual Review - Financial Crisis 2025

**Review Context**:
- **Scenario**: "Financial Crisis 2025" (existing pillar scenario)
- **Last Review**: December 2024
- **Market Changes**: Volatility regime shifted higher, EM spreads compressed
- **System Changes**: Base Metals migrating to Murex, Precious Metals vol shocks changed to relative
- **Trading Changes**: Iron Ore discontinued, Cobalt added

**Review Results**:
```
Asset Class Reviews:
1. Rates/FX: NO CHANGE
   - Rationale: Market changes (vol regime) don't affect scenario calibration
   - Current parameters remain appropriate

2. Credit: NO CHANGE
   - Rationale: Spread compression is cyclical, not structural
   - Scenario still represents severe stress

3. Energy: NO CHANGE
   - Rationale: No material market or system changes

4. Precious Metals: MINOR ADJUSTMENT
   - Rationale: Vol shocks changed from absolute to relative (Murex migration)
   - Proposed: Convert existing absolute shocks to relative format
   - Affected: Gold, Silver, Platinum, Palladium (all products)

5. Base Metals: MAJOR REVISION
   - Rationale:
     * System migration to Murex (calculation changes)
     * Iron Ore discontinued (remove from scenario)
     * Cobalt added (include in scenario)
   - Proposed:
     * Remove Iron Ore shocks
     * Add Cobalt shocks (calibrate to copper, industrial demand driver)
     * Review all tenor structures (Murex has different convention)
   - Affected: All Base Metals products

Overall Recommendation: MAJOR_REVISION_NEEDED
```

**Review Memo Output**:
- 6 pages (markdown)
- Asset class breakdown with rationale
- Specific parameter change proposals
- Timeline for re-parameterization
- MLRC noting (not approval - review only)

---

## MLRC Governance Process

### What is MLRC?

**MLRC** (Market & Liquidity Risk Committee) is the governance forum for:
- Approving new pillar stress scenarios
- Reviewing annual scenario assessments
- Endorsing scenario parameterization changes
- Overseeing stress testing framework

**Membership**: CRO, Head of Market Risk, Head of Liquidity Risk, CFO, Desk Heads (as needed)

### Scenario Approval Workflow

```
1. Scenario Design (Market Risk)
   ├── Economic narrative development
   ├── Risk factor parameterization
   ├── Validation (correlation, magnitude, completeness)
   └── Confidence scoring
        ↓
2. Front Office Consultation (2-3 weeks)
   ├── Desk heads review scenario relevance
   ├── Feedback on parameter reasonableness
   ├── Confirmation of trading book exposures
   └── Suggested adjustments
        ↓
3. MLRC Paper Preparation (Market Risk)
   ├── MLRC Word document generation (via skill)
   ├── Background and narrative
   ├── Asset class parameter tables
   ├── Validation results
   ├── Front Office feedback summary
   └── Recommendations
        ↓
4. MLRC Meeting (Monthly)
   ├── Market Risk presents scenario
   ├── Discussion of parameters and rationale
   ├── Committee questions and challenges
   ├── DECISION: Approve / Defer / Revise
   └── Document formal governance section
        ↓
5. Post-Approval Implementation (Asset Control)
   ├── Upload parameters to VESPA/RAV systems
   ├── Verify system calculations
   ├── Test scenario execution
   └── Confirm with Market Risk
        ↓
6. Monthly Stress Reporting (Market Risk)
   ├── Execute scenario in systems
   ├── Calculate stress loss
   ├── Report to MLRC
   └── Compare to risk appetite limits
```

### Annual Review Workflow

```
1. Review Trigger (Q1 - Stress Test Forum)
   ├── Identify scenarios for review
   ├── Consider: age, market changes, trading changes
   └── Assign to Market Risk for assessment
        ↓
2. Scenario Assessment (Market Risk, Q2-Q3)
   ├── Market changes since last review?
   ├── System changes (Murex migration)?
   ├── Trading changes (products added/removed)?
   ├── Parameterization still reasonable?
   └── Use skill to generate review memo
        ↓
3. MLRC Review Memo (Q4)
   ├── Present assessment to MLRC
   ├── Recommend: Approve as-is / with changes / major revision
   ├── If changes: Detail proposed adjustments
   └── MLRC decision: Note / Request re-parameterization
        ↓
4. Re-parameterization (if needed)
   ├── Follow new scenario workflow (above)
   ├── Treat as scenario update, not new scenario
   ├── Front Office re-consultation
   └── MLRC approval of updated parameters
```

### MLRC Document Format

The skill generates Word documents matching the required format:

**Cover Sheet**:
```
+-------------------------------------------------------------------+
| Board Report Cover Sheet                                          |
+-------------------------------------------------------------------+
| Document Name    | [Scenario Name] - Scenario Parameters 2025     |
| Meeting Date     | MLRC - [Date]                                  |
| Presenter        | Market Risk                                    |
| Context          | New pillar stress scenario for approval        |
| Purpose          | Approval of stress scenario parameterization  |
+-------------------------------------------------------------------+
```

**Background Section**:
- Trigger Event
- Economic Narrative (2-3 paragraphs)
- Key Assumptions (bulleted)
- Timeline (onset → peak → recovery)

**Asset Class Sections** (5 sections):
- Description (what's being stressed)
- Rationale (why these parameters)
- Historical Analogue (e.g., "2008 Financial Crisis")
- Proposed Shocks (table with risk factors and magnitudes)

**Validation Results**:
- ❌ Errors (if any - must resolve before MLRC)
- ⚠️ Warnings (flagged for discussion)
- ℹ️ Info (context, no action needed)

**Front Office Consultation**:
- Desk-by-desk feedback summary
- Questions asked and responses
- Adjustments made based on feedback

**Conclusions**:
- Recommendation: "Scenario submitted for MLRC approval"
- Confidence Score: e.g., "70% (strong calibration, some novel elements)"
- Next Steps: "Pending MLRC approval, Asset Control implementation"

**Document History**:
```
+-------------------------------------------------------------------+
| Prepared by                       | Market Risk                  |
| Date                              | [Date]                       |
| Reviewed by 2nd line of defence   | N/A                          |
+-------------------------------------------------------------------+
```

**Formal Governance** (completed post-MLRC):
```
+-------------------------------------------------------------------+
| Reviewing committee and meeting date     | MLRC - [Date]         |
| Outcome and key rationale for decision   | *(To be completed)*   |
| Significant matters raised               | *(To be completed)*   |
+-------------------------------------------------------------------+
```

---

## Troubleshooting

### Common Issues

#### 1. Low Confidence Score

**Symptom**: Scenario confidence score <50%

**Possible Causes**:
- Novel scenario type with weak historical precedent
- Extreme severity (>150% historical maximum)
- Validation errors present
- Missing asset class data

**Solutions**:
1. **Check validation results**:
   ```python
   errors = [v for v in scenario.validation_results if v.level == ValidationLevel.ERROR]
   if errors:
       print("Fix these errors:")
       for e in errors:
           print(f"  - {e.message}")
   ```

2. **Review scenario type**:
   - Is this truly unprecedented? Consider using closest historical analogue
   - Can severity be reduced to "severe" (100%) instead of "extreme" (150%)?

3. **Add historical calibration**:
   - Reference specific historical events in narrative
   - Justify novel elements explicitly in key assumptions

4. **Consult historical crisis database**:
   ```python
   with open("data/historical_crises.json") as f:
       crises = json.load(f)
   # Find similar events
   ```

#### 2. Correlation Consistency Errors

**Symptom**: ❌ ERROR in validation report

**Example**:
```
❌ ERROR: USD weakens in recession scenario (contradicts risk-off pattern)
```

**Cause**: FX directions inconsistent with scenario type

**Solution**:
1. **Review risk-off pattern**:
   - Recession → USD/JPY/CHF strengthen (safe havens)
   - Financial crisis → Extreme safe haven flows
   - Inflation shock → USD mixed (depends on Fed vs others)

2. **Check scenario type template**:
   ```python
   engine = ParameterizationEngine(data_dir)
   template = engine._get_scenario_template(ScenarioType.RECESSION)
   print(template['fx_direction'])  # Should show safe haven strengthening
   ```

3. **Override if justified**:
   - If you have strong rationale (e.g., US-specific recession, EUR outperforms)
   - Document in `key_assumptions`
   - Accept warning, don't suppress error

#### 3. Magnitude Too Extreme

**Symptom**: ⚠️ WARNING: Exceeds historical precedent

**Example**:
```
⚠️ WARNING: WTI oil shock (+80%) exceeds 2008 maximum (+70%)
```

**Cause**: Shock magnitude beyond historical observations

**Solution**:
1. **Review historical data**:
   ```python
   with open("data/historical_crises.json") as f:
       crises = json.load(f)
   oil_shocks = [c['risk_factors']['energy']['WTI']['shock']
                 for c in crises['crises']]
   print(f"Historical oil shocks: {oil_shocks}")
   ```

2. **Justify or reduce**:
   - If justified (e.g., scenario involves physical supply destruction): Document in narrative
   - If not justified: Reduce to severe (100%) or moderate (60%)

3. **Use severity scaling**:
   ```python
   # Reduce from EXTREME to SEVERE
   scenario = designer.create_scenario(
       ...,
       severity=Severity.SEVERE  # 100% instead of 150%
   )
   ```

#### 4. Tenor Structure Invalid

**Symptom**: ❌ ERROR: Curve flattens in recession (should steepen)

**Example**:
```
❌ ERROR: USD curve flattens in recession
   - 2Y: -50bp
   - 10Y: -100bp  (more than 2Y)
   - 30Y: -150bp  (more than 10Y)
```

**Cause**: Curve shape inconsistent with scenario (recession → policy easing → steepening)

**Solution**:
1. **Understand curve mechanics**:
   - **Recession** → Short end down more (Fed cuts) → Steepening
   - **Inflation shock** → Short end up more (Fed hikes) → Flattening
   - **Bear flattening** (hawkish): 2Y↑↑, 10Y↑, 30Y→
   - **Bull steepening** (dovish): 2Y↓↓, 10Y↓, 30Y→

2. **Adjust tenor pattern**:
   ```python
   custom_shocks = {
       'rates_fx': {
           'USD': {
               'O/N': -200,   # Policy rate
               '2Y': -180,    # Short end
               '10Y': -100,   # Belly
               '30Y': -50     # Long end
           }
       }
   }

   scenario = designer.create_scenario(
       ...,
       custom_shocks=custom_shocks
   )
   ```

3. **Check scenario type**:
   - Recession/Financial Crisis → Steepening
   - Inflation Shock/Policy Error → Flattening or bear steepening

#### 5. Missing Asset Class Data

**Symptom**: Confidence score penalized, incomplete scenario

**Cause**: Asset class not parameterized (e.g., forgot Energy)

**Solution**:
1. **Check completeness**:
   ```python
   asset_classes = [ac.asset_class for ac in scenario.asset_class_shocks]
   required = ['rates_fx', 'credit', 'energy', 'precious_metals', 'base_metals']
   missing = [ac for ac in required if ac not in asset_classes]
   if missing:
       print(f"Missing: {missing}")
   ```

2. **Add missing asset class**:
   - Ensure `narrative_elements` cover all asset classes
   - Or use `custom_shocks` to explicitly add

#### 6. Front Office Concerns

**Symptom**: Desk heads flag parameter as "unrealistic" during consultation

**Cause**: Parameter doesn't reflect current trading book or market structure

**Solutions**:
1. **Gather desk feedback early**:
   - Use consultation prompts generated by skill
   - Schedule 1-on-1 discussions before MLRC

2. **Adjust based on feedback**:
   - If desk has specific concern (e.g., "We no longer trade Iron Ore"):
     ```python
     # Remove from scenario
     custom_shocks['base_metals'].pop('IronOre', None)
     ```

3. **Document in MLRC paper**:
   - Show that Front Office was consulted
   - Explain adjustments made
   - Justify parameters they challenged (if you disagree)

#### 7. Word Document Generation Fails

**Symptom**: `python-docx` import error or document not generated

**Cause**: python-docx library not installed

**Solution**:
```bash
# Install python-docx
pip install python-docx

# Or use uv
uv add python-docx
```

**Fallback**: Skill automatically generates markdown format if python-docx unavailable:
```python
# Markdown fallback is automatic
scenario_md = designer.save_scenario(scenario, output_dir)
# Outputs .md file instead of .docx
```

#### 8. Scenario Name Collision

**Symptom**: Output file already exists, overwrites previous scenario

**Cause**: Scenario names not unique, or same scenario created multiple times

**Solution**:
1. **Use unique names**:
   ```python
   scenario_name = "US Recession with Fed Policy Error - 2025"  # Add year
   ```

2. **Check output directory**:
   ```bash
   ls test_output/
   # Rename old scenarios before creating new ones
   ```

3. **Version scenarios**:
   ```python
   scenario = designer.create_scenario(
       ...,
       scenario_name="Financial Crisis 2025 - v2"
   )
   ```

---

## Advanced Usage

### Custom Shock Adjustments

Override default parameterization for specific risk factors:

```python
custom_shocks = {
    'rates_fx': {
        'USD': {
            '2Y': -250,  # More aggressive Fed easing
            '10Y': -120,
            '30Y': -60
        },
        'EURUSD': -10  # EUR weaker than default
    },
    'credit': {
        'US': {
            'Financials': {
                'IG_spread_shock_bps': 800  # Worse financial stress
            }
        }
    }
}

scenario = designer.create_scenario(
    ...,
    custom_shocks=custom_shocks
)
```

### Hybrid Scenarios

Combine multiple scenario types:

```python
scenario = designer.create_scenario(
    scenario_name="China Slowdown + Oil Supply Disruption",
    trigger_event="China hard landing coincides with Middle East oil disruption",
    scenario_type=ScenarioType.CHINA_SLOWDOWN,  # Primary
    severity=Severity.SEVERE,
    primary_geography="global",
    narrative_elements=[
        "china_slowdown",
        "oil_supply_shock"  # Secondary element
    ],
    transmission_channels=[...],
    ...
)
```

The engine will blend templates for both scenario types.

### Regional Focus

Adjust shock magnitudes by region:

```python
scenario = designer.create_scenario(
    ...,
    primary_geography="US",  # US-centric
    narrative_elements=[
        "us_policy_error",
        "limited_global_spillover"  # Isolate to US
    ]
)

# Engine automatically:
# - Amplifies USD rate shocks
# - Reduces EUR/GBP/JPY rate shocks
# - Adjusts FX (USD strength vs others)
# - Scales credit shocks (US >> EUR/EM)
```

### Programmatic Scenario Library

Build a library of scenarios:

```python
scenarios = []

for scenario_type in [ScenarioType.RECESSION, ScenarioType.INFLATION_SHOCK]:
    for severity in [Severity.MODERATE, Severity.SEVERE]:
        for geography in ["US", "EUR", "global"]:
            scenario = designer.create_scenario(
                scenario_name=f"{scenario_type.value}_{severity.value}_{geography}",
                trigger_event=f"{scenario_type.value} in {geography}",
                scenario_type=scenario_type,
                severity=severity,
                primary_geography=geography,
                narrative_elements=[scenario_type.value],
                transmission_channels=["..."],
                key_assumptions=["..."]
            )
            scenarios.append(scenario)

# Export all
for s in scenarios:
    designer.save_scenario(s, output_dir / s.metadata.scenario_name)
```

---

## Integration Examples

### With Other Skills

**Workflow: Meeting → Scenario**:
```
1. User: "Create meeting minutes from scenario_planning_meeting.txt"
   → meeting-minutes skill structures notes

2. User: "Create a stress scenario based on the decisions in those meeting minutes"
   → pillar-stress-generator skill extracts scenario details from structured minutes
   → Generates parameterization
```

**Workflow: Project Plan → Stress Testing Initiative**:
```
1. User: "Create a project plan for implementing the new stress scenarios"
   → project-planner skill generates timeline, resources, governance

2. User: "Generate stress scenarios for that project"
   → pillar-stress-generator creates the actual scenarios
```

### With External Systems

**VESPA/RAV Upload** (future):
```python
# After MLRC approval
scenario = designer.create_scenario(...)
output_file = designer.save_scenario(scenario, output_dir)

# Export to VESPA format (future enhancement)
vespa_xml = export_to_vespa(scenario)
upload_to_vespa(vespa_xml)
```

**Stress Loss Calculation** (future):
```python
# Execute scenario in risk system
stress_loss = calculate_stress_loss(scenario, portfolio)
print(f"Stress loss: £{stress_loss:,.0f}")
```

---

## Regulatory Alignment

### PRA SS13/13 Requirements

| Requirement | How Skill Addresses |
|-------------|---------------------|
| **Severe but plausible scenarios** | Severity scaling calibrated to 2008/2020 (100% = severe) |
| **Reverse stress testing** | Can create extreme scenarios (150% severity) to find breaking points |
| **Scenario narrative** | Economic narrative with trigger, transmission, timeline |
| **Governance approval** | MLRC document generation for formal approval |
| **Regular review** | Annual review workflow with change detection |
| **Documentation** | Complete parameterization files + validation reports |

### BCBS Stress Testing Principles

| Principle | How Skill Addresses |
|-----------|---------------------|
| **Principle 1: Comprehensive** | All 5 asset classes covered |
| **Principle 2: Forward-looking** | Scenarios not just historical re-runs |
| **Principle 3: Severe** | 100% severity = 2008/2020-like events |
| **Principle 4: Reverse stress testing** | Extreme (150%) severity option |
| **Principle 7: Stress testing governance** | MLRC approval workflow |
| **Principle 11: Scenario design** | Structured narrative + transmission channels |

### ICBC Market Risk Policy Alignment

| Policy Section | How Skill Addresses |
|----------------|---------------------|
| **Section 9.2.1: Stress Testing** | Implements pillar stress methodology |
| **Section 5.4: Annual Review** | Annual review workflow with MLRC memo |
| **Section 9.2.3: Front Office Consultation** | Generates consultation prompts |
| **Section 9.2.4: MLRC Approval** | MLRC Word document in governance format |

---

## Additional Resources

### Documentation
- [Skills Guide](06-skills-guide.md) - Complete skills framework
- [pillar-stress-generator README](.claude/skills/pillar-stress-generator/README.md) - Quick reference
- [pillar-stress-generator SKILL.md](.claude/skills/pillar-stress-generator/SKILL.md) - AI prompt

### Source Code
- Skill definition: `.claude/skills/pillar-stress-generator/SKILL.md`
- Parameterization engine: `.claude/skills/pillar-stress-generator/parameterization_engine.py`
- Validators: `.claude/skills/pillar-stress-generator/validators.py`
- Scenario designer: `.claude/skills/pillar-stress-generator/scenario_designer.py`
- Scenario reviewer: `.claude/skills/pillar-stress-generator/scenario_reviewer.py`
- MLRC document builder: `.claude/skills/pillar-stress-generator/mlrc_document_builder.py`
- Test suite: `.claude/skills/pillar-stress-generator/test_scenarios.py`

### Data Files
- Risk factor library: `.claude/skills/pillar-stress-generator/data/risk_factor_shocks_library.json`
- Historical crises: `.claude/skills/pillar-stress-generator/data/historical_crises.json`
- Test outputs: `.claude/skills/pillar-stress-generator/test_output/`

### External Links
- [PRA SS13/13 - Stress Testing](https://www.bankofengland.co.uk/prudential-regulation/publication/2013/stress-testing-ss)
- [BCBS Stress Testing Principles (2018)](https://www.bis.org/bcbs/publ/d450.htm)
- [Anthropic: Agent Skills Best Practices](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

---

**Document Version**: 1.0
**Status**: Active Reference
**Last Updated**: 2025-11-12
