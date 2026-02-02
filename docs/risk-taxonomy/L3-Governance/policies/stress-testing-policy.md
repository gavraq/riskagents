---
# Policy Metadata
policy_id: MR-L3-005
policy_name: Market Risk Stress Testing Policy
version: 1.1
effective_date: 2025-01-17
next_review_date: 2026-01-17
owner: Head of Market Risk
approving_committee: RMC
document_classification: Internal
supersedes: null

# Taxonomy Linkages
parent_policy: MR-L3-001  # Market Risk Policy
l1_requirements:
  - REQ-L1-001  # CRR/CRR III
  - REQ-L1-003  # FRTB
  - REQ-L1-004  # SS13/13 Market Risk
  - REQ-L1-010  # PRA Stress Testing
l2_risk_types:
  - MR-L2-001   # Market Risk (General)
  - MR-L2-002   # Interest Rate Risk (Trading)
  - MR-L2-003   # Foreign Exchange Risk
  - MR-L2-004   # Equity Risk
  - MR-L2-005   # Commodity Risk
  - MR-L2-006   # Credit Spread Risk (Trading)
  - MR-L2-007   # Volatility Risk
  - MR-L2-008   # Illiquidity Risk
  - MR-L2-009   # Concentration Risk (Market)
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-002   # MLRC Terms of Reference
  - MR-L3-003   # VaR Limit Framework
  - MR-L3-004   # VaR Policy
l4_processes:
  - MR-L4-001   # Market Risk Process Orchestration
  - MR-L4-006   # Risk Engine Calculation
  - MR-L4-007   # Market Risk Reporting & Sign-off
  - MR-L4-011   # Stress Testing
  - MR-L4-014   # Aged Inventory Monitoring
l5_controls:
  - MR-L5-002   # Stress Limits Controls
  - MR-L5-005   # Concentration Limits Controls
l6_models:
  - MR-L6-001   # Historical Simulation VaR/SVaR
  - MR-L6-002   # ECAP Methodology
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-008  # Risk ODS
---

# Market Risk Stress Testing Policy

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Policy ID** | MR-L3-005 |
| **Version** | 1.1 |
| **Effective Date** | 17 January 2025 |
| **Next Review** | 17 January 2026 |
| **Parent Policy** | Market Risk Policy (MR-L3-001) |
| **Owner** | Head of Market Risk |
| **Approving Committee** | Risk Management Committee (RMC) |

---

## 1. Introduction

### 1.1 Purpose

As part of the Market Risk Policy framework, all risk factors are subject to stress shocks under the Market Risk Stress Framework to determine loss vulnerabilities in the trading portfolio under market stress moves. This Policy establishes the governance framework for stress testing at Meridian Global Bank ("the Bank").

Stress testing is performed on a weekly basis with capability to run daily if required during periods of market stress.

### 1.2 Relationship with VaR

In addition to individual risk factor stress measures, the trading book and particular sub-portfolios are subject to stress testing and scenario analysis - combinations of extreme moves across a range of risk factors.

Portfolio stress scenarios are a key market risk control that work **in conjunction with** Value-at-Risk (VaR):

| VaR | Stress Testing |
|-----|----------------|
| Historical simulation based on past returns | Blunt shocks applied to all risk factors |
| 99% confidence interval (1-in-100 day loss) | Deliberately targets tail risk beyond 99% frontier |
| Backward-looking (historical data) | Can be forward-looking (hypothetical scenarios) |
| Captures normal market volatility | Captures extreme/crisis scenarios |

### 1.3 Scope

The Bank's stress testing programme includes:
- All traded linear and non-linear products
- All asset classes in the trading book
- All legal entities within Meridian Global Bank Group

### 1.4 Regulatory Context

| Regulation | Reference | Key Requirements |
|------------|-----------|------------------|
| **CRR Art 325bh** | Stress testing requirements | Comprehensive stress testing programme |
| **PRA SS13/13 Ch 8** | Market risk stress testing | Scenario design, governance, reporting |
| **PRA Stress Testing** | Annual Cyclical Scenario (ACS) | Bank-wide stress test contribution |
| **ICAAP** | Pillar 2 capital | Stress testing for capital adequacy |

---

## 2. Scope of Stress Testing

### 2.1 Risk Factors Covered

The stress testing programme considers the following:

| Risk Category | Stress Considerations |
|---------------|----------------------|
| **Concentration Risk** | Impact of unwinding large positions relative to market depth |
| **Liquidity Horizons** | Position exit times across all asset classes under stressed conditions |
| **One-Way Markets** | Crowded positioning where market moves against widely-held positions |
| **Event/Jump Risk** | Default events, rating migrations, sudden price gaps |
| **Asymmetric Risk** | Deep out-of-the-money options; onshore vs offshore positions |
| **Price Grouping Sensitivity** | Positions sensitive to clustering of prices |
| **Other Material Risks** | Risks not captured appropriately in VaR (recovery rates, implied correlations, volatility skew) |

### 2.2 Liquidity Horizon Calibration

Stress shocks are calibrated to reflect the nature of underlying portfolios and time required to hedge or manage risk under severe conditions:
- **Standard Calibration**: 10-day liquidity horizon aligned with regulatory VaR/SVaR
- **Concentration Assessment**: Monthly ICAAP concentration risk assessments use extended horizons where appropriate
- **Asset-Specific Horizons**: Illiquid assets may use horizons up to 25 days per ECAP methodology

### 2.3 Quarterly Risk Assessment

Market Risk is responsible quarterly to assess:
- **Net Risk**: Outright directional risk impact
- **Curve Risk**: Tenor impact across yield curves
- **Basis Risk**: Bond-swap, futures vs physical, onshore/offshore currency basis

Such positions should be incorporated into relevant stress scenarios. If no new positions are identified, this must be formally attested.

### 2.4 Scenario Design Responsibility

Market Risk is responsible for identifying stress scenarios that highlight underlying risk factor vulnerabilities. Scenarios must:
- Test effects of adverse movements in market volatilities
- Consider correlated impacts across competing asset classes
- Challenge assumptions underlying the VaR model
- Be appropriate to the Bank's portfolio composition

Results are reviewed by senior management and form an intrinsic Level 1 limit supporting the Risk Appetite Framework.

---

## 3. Types of Market Risk Stress

### 3.1 Worst-Case Stress (VaR/SVaR Based)

The "worst-case" base stress loss is the greatest loss produced by each day's 1-day or 10-day VaR or SVaR. This measure includes all severe market events during the historical observation period.

Market Risk consults with Business to determine stress scenario parameters but ultimately discretion rests with Market Risk to interpret simulations for monitoring purposes, including:
- Selection of most appropriate window (stress or historic)
- Holding period
- Portfolio aggregation level

### 3.2 Severe Historical Event Stress

Severe historical events are those **outside** the historical observation period underlying VaR measures. The specific market moves associated with such events may be:
- Directly applied to the trading book
- Built into hypothetical stress scenarios (more common)

### 3.3 Hypothetical Stress Scenarios

Hypothetical scenarios are developed by Market Risk and may be based on:
- **Historical Events**: Including events within the historical data series
- **Current Thematic Issues**: Events considered possible at point in time (e.g., geopolitical crises, policy changes, market dislocations)
- **Concentration Findings**: From monthly ICAAP assessments and fortnightly risk meetings
- **Point of Weakness Analysis**: Weekly identification of key trading strategy vulnerabilities

In selecting scenarios, Market Risk considers:
- Major risks from daily risk factor and stress exposures
- Issuer risk exposures
- Country risk exposures
- Current market conditions and emerging risks

### 3.4 Point of Weakness (PoW) Stress

In addition to top-down pillar scenarios, Market Risk performs **bottom-up** Point of Weakness stress analysis weekly:

**Purpose**:
- Identify main vulnerabilities/top risks most sensitive to price changes weighted by P&L impact
- Define extreme but plausible market price changes for identified strategies

**Process**:
1. **Weekly Identification**: Market Risk identifies top risk positions and strategies
2. **Scenario Design**: Specific stress scenarios designed for each strategy
3. **Weekly Forum**: PoW discussion with Trading Heads and Risk
4. **Monthly Deep Dive**: Meeting with CRO, Head of Trading, and senior risk

PoW supplements top-down pillar stresses by focusing on **specific vulnerabilities** in current positioning rather than generic macro scenarios.

### 3.5 Reverse Stress Testing

Reverse stress tests identify conditions that would threaten the Bank's viability:
- Performed quarterly
- Identifies "what would need to happen" to cause severe losses
- Results reported to RMC
- Informs scenario design and risk appetite discussions

---

## 4. Stress Testing Execution

### 4.1 Frequency and Level

| Stress Type | Frequency | Level | Governance |
|-------------|-----------|-------|------------|
| **Pillar Scenarios** | Weekly (daily capability) | Entity, Business Unit | MLRC/RMC |
| **Historical Scenarios** | Weekly | Entity, Business Unit | MLRC |
| **Point of Weakness** | Weekly | Strategy/Position | MLRC |
| **Reverse Stress** | Quarterly | Entity | RMC |
| **Environmental Stress** | Quarterly | Entity | RMC |

### 4.2 Conduct of Stress Testing

Market Risk is responsible for:
- Market risk stress testing execution
- Scenario parameterisation and maintenance
- Results analysis and commentary
- Reporting to governance forums

### 4.3 Reporting to Regulators

Market Risk ensures stress testing results cover all trading book positions. As part of IMA permission:
- Stress loss exposure reported to PRA **quarterly**
- Ad hoc regulatory reporting requirements met as needed
- Annual Cyclical Scenario (ACS) contribution prepared

### 4.4 Reporting to Management

| Forum | Frequency | Content |
|-------|-----------|---------|
| **RMC** | Monthly | Stress results covering entire trading book; capacity to absorb losses vs appetite |
| **MLRC** | Weekly | Pillar stress trends; PoW analysis; scenario review |
| **ExCo/Top Risks Pack** | Weekly | Stress testing results for senior management |
| **Board Risk Committee** | Quarterly | Executive summary; Level 1 stress limit status |
| **Group Reporting** | Monthly | Stress by Global Markets and business decomposition |

RMC evaluates capacity to absorb market risk stress losses in accordance with the Risk Appetite Statement and identifies steps to control or reduce risks where appropriate.

### 4.5 Alignment with Group Stress Testing

Market Risk takes necessary steps to align stress testing methodology and results for any Group-level stress submissions to ensure consistency and comparability.

### 4.6 Pre-Trade Scenario Analysis

Market Risk may set up, modify, maintain, and improve scenarios for **pre-trade scenario analysis**:
- Used where regulations require providing pre-trade scenario analyses to clients
- Scenarios designed in consultation with the client
- Governed under standard stress testing framework

---

## 5. Standard Pillar Scenarios

### 5.1 Scenario Inventory

The Bank maintains a set of pillar stress scenarios covering major risk events:

| Scenario | Type | Key Shocks | Stress Limit |
|----------|------|------------|--------------|
| **Global Financial Crisis** | Historical | Credit spreads +500bp, Equities -40%, Vol +200% | $190m |
| **COVID-19 Shock** | Historical | Vol +300%, Oil -50%, Credit +300bp | $125m |
| **Rates Shock Up** | Hypothetical | Parallel +200bp across curves | $100m |
| **Rates Shock Down** | Hypothetical | Parallel -100bp (floor considerations) | $75m |
| **EM Crisis** | Hypothetical | EM FX -30%, EM Spreads +300bp | $95m |
| **Stagflation** | Hypothetical | Rates +150bp, Equities -25%, Commodities +30% | $95m |
| **Credit Crunch** | Hypothetical | IG spreads +150bp, HY +400bp, defaults +3% | $100m |
| **Geopolitical Event** | Hypothetical | Oil +40%, Safe haven rally, EM sell-off | $90m |
| **Worst-of Pillar** | Dynamic | Worst result across all scenarios | $190m |

### 5.2 Scenario Parameters

Each scenario specifies shocks to:
- Interest rates (parallel, steepening, flattening, inversion)
- Credit spreads (by rating, sector, geography)
- Equity indices (developed, emerging, sector)
- FX rates (G10, EM, crosses)
- Commodities (energy, metals, agricultural)
- Volatilities (equity, FX, rates)
- Correlations (where material)

### 5.3 Environmental Stress Scenarios

Environmental risk scenarios are maintained alongside standard pillar stresses:

| Scenario | Type | Key Considerations |
|----------|------|-------------------|
| **Disorderly Transition** | Climate | Carbon price spike, stranded assets, sector re-pricing |
| **Physical Risk Event** | Climate | Commodity supply disruption, insurance losses |
| **Green Swan** | Climate | Sudden climate-driven market correction |

Environmental scenarios:
- Designed at same severity as other pillar stresses
- Reviewed annually
- Consider transition risk (policy, technology, market sentiment)
- Consider physical risk (weather events, collateral impacts)

---

## 6. Stress Loss Limits and Appetite

### 6.1 Stress Loss Appetite

The Bank's Market Risk Stress Loss appetite is subject to limits set in line with the Risk Appetite Statement, owned and approved at Board level.

### 6.2 Limit Structure

| Limit Type | Level | Value | Approval |
|------------|-------|-------|----------|
| **Worst-of Pillar Stress** | Level 1 | $190m | Board/RMC |
| **Individual Pillar Scenario** | Level 1 | Per scenario table | RMC |
| **Business Unit Stress** | Level 2 | Allocated from L1 | MLRC |

The maximum stress loss derived through various stress types is assigned **Level 1 Limit** status under Market Risk Appetite.

### 6.3 Limit Monitoring

Market Risk monitors exposure against stress loss limits **at least weekly**:
- Daily monitoring capability during stressed markets
- Any limit breaches dealt with per Market Risk Policy breach management (Section 7.4)
- Trends and near-breaches escalated to MLRC

### 6.4 Ad Hoc Limit Adjustments

Stress loss limits may be reviewed and revised at any time by appropriately authorised risk committees if the financial stability of the Bank requires it.

---

## 7. Scenario Review and Maintenance

### 7.1 Annual Review

Market Risk is responsible for ensuring stress test scenarios remain:
- **Relevant**: Appropriate to current portfolio composition
- **Severe**: Sufficiently stressed to identify tail risks
- **Plausible**: Based on reasonable (if extreme) market conditions
- **Comprehensive**: Covering all material risk factors

Scenarios are reviewed **at least annually** with focus on:
- Regularly applied scenarios remaining fit for purpose
- Ad hoc scenarios (responding to market conditions/concentrations)
- Scenarios that identify events most harmful to the Bank, even if improbable

### 7.2 Monthly Updates

Market Risk provides new or amended Point of Weakness scenarios or Top Risks analysis to MLRC on **minimum monthly** basis.

### 7.3 Basis Risk Integration

Market Risk incorporates basis risk scenarios into existing pillar stresses as identified through quarterly assessment (Section 2.3), including:
- Bond-swap basis
- Futures vs physical
- Onshore/offshore currency basis
- Cross-currency basis

### 7.4 Scenario Change Governance

| Change Type | Approval | Documentation |
|-------------|----------|---------------|
| **New Pillar Scenario** | RMC | Full scenario specification; rationale |
| **Pillar Parameter Change** | MLRC | Impact assessment; rationale |
| **PoW Scenario Update** | Market Risk (noted at MLRC) | Weekly PoW report |
| **Scenario Retirement** | MLRC | Justification for removal |

---

## 8. Governance

### 8.1 Committee Oversight

| Committee | Role |
|-----------|------|
| **Board Risk Committee** | Approve Level 1 stress limits; quarterly stress review |
| **RMC** | Recommend stress limits; monthly stress reporting; reverse stress review |
| **MLRC** | Weekly stress monitoring; scenario review; PoW discussion |
| **Stress Forum** | Enterprise-wide stress coordination (established Q1 2023) |

### 8.2 Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| **Market Risk** | Scenario design, execution, analysis, reporting; limit monitoring; PoW process |
| **Risk Methodology & Analytics** | Methodology support; scenario calibration |
| **RAV** | Stress data validation; scenario setup in Risk Engine |
| **Front Office** | Participate in PoW discussions; provide position context |
| **CRO** | Stress appetite recommendation; escalation point |

---

## 9. Related Documents

### 9.1 Parent and Sibling Policies

| Document | Relationship |
|----------|--------------|
| [Market Risk Policy (MR-L3-001)](./market-risk-policy.md) | Parent policy |
| [VaR Policy (MR-L3-004)](./var-policy.md) | Sibling policy; VaR/SVaR governance |
| [Trading Book Boundary Policy (MR-L3-006)](./trading-book-boundary-policy.md) | Sibling policy; scope definition |
| [VaR Limit Framework (MR-L3-003)](./var-limit-framework.md) | Limit structure |

### 9.2 Supporting Processes

| Process | Reference |
|---------|-----------|
| Stress Testing | MR-L4-011 |
| Risk Engine Calculation | MR-L4-006 |
| Market Risk Reporting & Sign-off | MR-L4-007 |

### 9.3 Supporting Skills

| Skill | Purpose |
|-------|---------|
| [Pillar Stress Generator](../../../../.claude/skills/pillar-stress-generator/) | Parameterise stress scenarios |
| [Stress Scenario Suggester](../../../../.claude/skills/stress-scenario-suggester/) | Research emerging risks for scenarios |

---

## 10. Exceptions

There are no exceptions to this Policy. Any deviations require RMC approval and must be documented.

---

## 11. Definitions

| Term | Definition |
|------|------------|
| **Pillar Stress** | Top-down macro scenario applied to entire portfolio |
| **PoW** | Point of Weakness - bottom-up stress of specific strategies |
| **Reverse Stress** | Test identifying conditions threatening viability |
| **Historical Scenario** | Stress based on actual historical market event |
| **Hypothetical Scenario** | Stress based on plausible but not yet occurred event |
| **Stress Limit** | Maximum acceptable loss under stress scenario |
| **Liquidity Horizon** | Time required to exit position under stress |

---

## 12. Policy Contact

| Field | Details |
|-------|---------|
| **Policy Owner** | Head of Market Risk |
| **Technical Queries** | Risk Methodology & Analytics |
| **Operational Queries** | Risk Reporting, Analysis & Validation |

---

## 13. Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-17 | Initial version | RMC |
| 1.1 | 2025-01-17 | Converted all amounts from GBP to USD for reporting consistency | RMC |

---

*This policy is the property of Meridian Global Bank. Unauthorised distribution is prohibited.*

*End of Document*
