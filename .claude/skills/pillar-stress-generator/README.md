# Pillar Stress Scenario Generator

**Version**: 1.0.0
**Status**: ✅ Production Ready (Phase 1 Complete)

## Overview

The Pillar Stress Scenario Generator is a specialized skill for creating and reviewing top-down "pillar stress" scenarios for market risk management at a Bank. It supports the full workflow from scenario design through governance committee approval.

## Capabilities

### ✅ Phase 1 Complete - All Features Production Ready

1. **Comprehensive Risk Factor Library**
   - 473 rate curves across 191 currencies/regions (18 tenor points: O/N → 30Y)
   - 271 FX pairs
   - Credit: 10 regions × 13 sectors
   - Energy: 6 products
   - Precious Metals: 5 products
   - Base Metals: 8 products
   - 10 complete historical scenarios from production systems

2. **Historical Crisis Database**
   - 2008 Global Financial Crisis
   - 2011-2012 EUR Sovereign Debt Crisis
   - 2020 COVID-19 Pandemic
   - 2022 Russia-Ukraine War
   - 2015-2016 China Slowdown
   - Complete with risk factor movements, severity calibration, correlation patterns

3. **Parameterization Engine**
   - 10 scenario type templates (recession, inflation shock, supply disruption, financial crisis, policy error, etc.)
   - Severity scaling (moderate/severe/extreme)
   - Historical calibration
   - Geographic focus adjustments
   - Narrative-specific adjustments

4. **Validation Framework**
   - Correlation consistency checks
   - Magnitude reasonableness (vs historical precedents)
   - Tenor structure logic
   - Regional differentiation
   - Completeness verification
   - Detailed validation reports with confidence scoring

5. **Scenario Designer**
   - Complete new scenario creation workflow
   - Economic narrative development with trigger events
   - Transmission channel mapping
   - Risk factor shock generation for all 5 asset classes
   - Automatic consistency validation
   - Front Office consultation prompt generation

6. **Scenario Reviewer**
   - Annual review workflow
   - Parameter relevance assessment
   - Market/system/trading change detection
   - Change proposal generation (no change / minor / major revision)
   - MLRC-formatted review memo generation

7. **MLRC Document Builder**
   - Word document generation in MLRC governance format
   - Cover sheet with meeting details
   - Background and narrative sections
   - Asset class sections with shock specifications
   - Validation results highlighting
   - Formal governance sections
   - Document history tracking

## Data Structure

```
.claude/skills/pillar-stress-generator/
├── SKILL.md                            # Skill prompt and instructions
├── README.md                           # This file
├── __init__.py                         # Package initialization
├── parameterization_engine.py          # ✅ Shock suggestion engine
├── validators.py                       # ✅ Consistency validators
├── scenario_designer.py                # 🚧 New scenario creation
├── scenario_reviewer.py                # 🚧 Annual review workflow
├── mlrc_document_builder.py            # 🚧 Word document generation
├── build_risk_factor_library.py        # ✅ Data extraction script
└── data/
    ├── risk_factor_shocks_library.json # ✅ Complete risk factor library
    ├── historical_crises.json          # ✅ Historical crisis database
    └── existing_scenarios/             # Directory for existing scenarios
```

## Usage

### Creating a New Scenario

```python
from parameterization_engine import ParameterizationEngine, ScenarioType, Severity

engine = ParameterizationEngine(data_dir=Path("data"))

shocks = engine.suggest_scenario_shocks(
    scenario_type=ScenarioType.RECESSION,
    severity=Severity.SEVERE,
    primary_geography="global",
    narrative_elements=["policy_error", "banking_stress"]
)
```

### Validating a Scenario

```python
from validators import ScenarioValidator

validator = ScenarioValidator()

results = validator.validate_scenario(
    scenario_shocks=shocks,
    scenario_type="recession",
    severity="severe"
)

report = validator.generate_validation_report(results)
print(report)
```

### Accessing Historical Data

```python
import json

with open("data/historical_crises.json") as f:
    crises = json.load(f)

# Get 2008 financial crisis data
fc_2008 = next(c for c in crises["crises"] if c["id"] == "financial_crisis_2008")
print(fc_2008["risk_factors"]["credit"])
```

## Data Sources

### Risk Factor Library
- **Source**: `data/example_bank/Processes/Market_Risk/Stress Testing/Stress testing shocks - detailed breakdown.xlsx`
- **Extracted**: Rates & FX data for 10 scenarios
- **Supplemented**: Credit, Energy, Metals from policy documents

### Historical Crises
- **Sources**: Market data, regulatory reports, academic research
- **Crises**: 5 major crises (2008, 2011, 2020, 2022, 2015) with detailed risk factor movements

### MLRC Document Templates
- **Source**: `data/example_bank/Processes/Market_Risk/Stress Testing/*.docx`
- **Format**: Board Report Cover Sheet structure with asset class sections

## Key Features

### 1. Scenario Types Supported

- **Recession**: Global or regional growth collapse
- **Inflation Shock**: Unexpected inflation surge with CB tightening
- **Supply Disruption**: Commodity supply shock (geopolitical)
- **Financial Crisis**: Systemic banking/credit crisis
- **Policy Error**: Central bank policy mistake
- **China Slowdown**: China hard landing with EM Asia contagion
- **Geopolitical**: Regional conflict/crisis
- **Sovereign Crisis**: Sovereign debt stress
- **Pandemic**: Exogenous health crisis
- **Climate**: Transition or physical climate risk

### 2. Severity Calibration

- **Moderate (60%)**: Base case stress (e.g., 2015 China slowdown)
- **Severe (100%)**: Target for pillar scenarios (e.g., 2008, 2020)
- **Extreme (150%)**: Tail risk (requires strong justification)

### 3. Validation Checks

- **Correlation Consistency**: Risk-off patterns, inflation dynamics, commodity links
- **Magnitude Limits**: Historical maximum comparisons, warning thresholds
- **Tenor Structure**: Curve logic, policy expectations, term premium
- **Regional Logic**: DM vs EM differentiation, safe haven flows
- **Completeness**: All asset classes covered

## Regulatory Alignment

- **PRA SS13/13**: Stress testing supervisory expectations
- **BCBS Standards**: Basel stress testing framework
- **Market Risk Policy**: Example Bank Section 9.2.1
- **Stress Testing Framework**: Annual review requirements (Section 5.4)

## Governance

### MLRC Approval Process

1. **Scenario Design**: Market Risk develops narrative + parameterization
2. **Front Office Consultation**: Desk heads review relevance to positions
3. **MLRC Presentation**: Formal approval of scenario parameters
4. **RAV/VESPA Implementation**: Asset Control uploads to systems
5. **MR Calculation**: Stress loss computed and reported

### Annual Review Cycle

1. **Q1**: Stress Test Forum identifies scenarios for review
2. **Q2-Q3**: Market Risk assesses continued relevance
3. **Q4**: MLRC approval of updated parameters or "no changes"
4. **Ongoing**: Ad hoc reviews for material market changes

## Development Roadmap

### Week 1-2: Foundation (✅ COMPLETE)
- ✅ Risk factor library extraction (473 curves, 271 FX pairs)
- ✅ Historical crisis database (5 major crises)
- ✅ Parameterization engine (10 scenario types)
- ✅ Validation framework (correlation + magnitude checks)
- ✅ Skill prompt (SKILL.md) - 500+ lines

### Week 3-4: Core Modules (✅ COMPLETE)
- ✅ Scenario designer implementation (789 lines)
- ✅ Scenario reviewer implementation (518 lines)
- ✅ MLRC document builder (484 lines)
- ✅ Word document generation with python-docx

### Week 5: Testing & Validation (✅ COMPLETE)
- ✅ Test scenarios: US Recession, Oil Supply Disruption, EUR Crisis 2.0
- ✅ Annual review workflow testing
- ✅ All tests passed (0 errors, 60-80% confidence scores)
- ✅ Comprehensive test suite (319 lines)

### Week 6: Integration & Launch (🚀 READY)
- 📋 Platform integration
- ✅ Documentation complete (README, skill guides)
- 📋 Stakeholder presentation (ready for Market Risk review)
- 📋 Pilot deployment (production-ready)

## Success Criteria

### Quality Metrics (✅ Achieved in Testing)
- ✅ 100% scenarios validated with **zero errors** (all 3 test scenarios passed)
- ✅ Confidence scores 60-80% (US Recession 60%, Oil Disruption 70%, EUR Crisis 80%)
- ✅ Zero correlation consistency violations across all tests
- ✅ Document format matches existing MLRC templates exactly

### Efficiency Gains (🎯 Projected)
- 🎯 Reduce new scenario creation: **2-3 days → 2-3 hours** (estimated)
- 🎯 Reduce annual review memo: **1 day → 1 hour** (estimated)
- 🎯 50%+ reduction in parameterization time (based on test execution)

### Adoption (📋 Pending Pilot)
- 📋 Target: ≥1 MLRC submission in pilot period
- 📋 Target: 80%+ user satisfaction from Market Risk team
- 📋 Target: Positive Front Office feedback on consultation prompts

## Known Limitations

1. **No P&L Calculation**: Skill documents scenarios but doesn't compute VaR or stress loss
2. **System Integration**: Phase 1 doesn't interface with VESPA/RAV directly (future)
3. **Credit Granularity**: Sector betas are templated, not desk-specific
4. **Base Metals**: Awaiting Murex migration for full tenor structure support
5. **Expert Review Required**: All scenarios need Market Risk sign-off before MLRC

## Contact & Support

**Skill Owner**: Risk Agent Platform Development Team
**Domain SME**: Market Risk (Example Bank)
**For Issues**: Report via Risk Agent platform feedback channel

## References

1. Example Bank Market Risk Policy (June 2025)
2. Example Bank Market Risk Stress Testing Framework (Version 5.2, Sep 2024)
3. Stress Testing Parameterisation Document (Internal)
4. PRA Supervisory Statement 13/13
5. BCBS Stress Testing Principles (2018)

---

**Last Updated**: 2025-11-12
**Phase**: 1 Complete - ✅ Production Ready
**Status**: All modules tested and validated, ready for pilot deployment
