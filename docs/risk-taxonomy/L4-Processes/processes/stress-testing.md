---
# Process Metadata
process_id: MR-L4-011
process_name: Market Risk Stress Testing
version: 1.2
effective_date: 2025-01-16
next_review_date: 2026-01-16
owner: Head of Risk Methodology & Analytics (RMA)
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-001  # Market Risk Process Orchestration
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-003  # FRTB
  - REQ-L1-004  # Basel III/IV
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-002   # MLRC Terms of Reference
l5_controls:
  - MR-L5-002   # Stress Limits Controls
l6_models:
  - MR-L6-004   # Stress Testing Model
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-008  # Risk ODS
---

# Market Risk Stress Testing Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-011 |
| **Version** | 1.0 |
| **Effective Date** | 16 January 2025 |
| **Owner** | Head of Risk Methodology & Analytics (RMA) |

---

## 1. Purpose

The Market Risk Stress Testing process ensures comprehensive identification, parameterisation, and governance of stress scenarios used for:

1. **Regulatory Capital** - Pillar 2A stress testing requirements (ICAAP/ILAAP)
2. **Internal Risk Management** - Limit monitoring and early warning indicators
3. **Board Reporting** - Risk appetite monitoring and strategic decision support
4. **Recovery Planning** - Identification of severe but plausible market stress events

This process governs the full lifecycle of stress scenarios from conception through annual review.

---

## 2. Regulatory Context

### 2.1 Key Requirements

| Regulation | Article/Section | Requirement |
|------------|-----------------|-------------|
| **CRR Article 368** | Stress testing | Institutions using IMA must have a rigorous stress testing programme |
| **PRA Rulebook** | Internal Capital Adequacy | Pillar 2A stress testing for market risk |
| **Basel MAR 30** | Stress testing | Comprehensive stress testing programme requirements |
| **SS13/13** | IMA requirements | Regular stress testing and scenario analysis |

### 2.2 Stress Testing Framework

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     STRESS TESTING FRAMEWORK                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  SCENARIO CLASSIFICATION                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  A. PILLAR STRESS (Firm-Wide)                                                           │
│     ─────────────────────────────────────────────────────────────────────────────────   │
│     • Regular, comprehensive stress tests run on established cadence                    │
│     • Cover ALL 5 asset classes (Rates/FX, Credit, Equities, Commodities)               │
│     • Calibrated to historical crisis precedents (2008, 2020, 2022)                     │
│     • Top-down approach: Macro narrative → Risk factor shocks                           │
│     • Used for: Regulatory capital, ICAAP, Board reporting                              │
│                                                                                         │
│  B. POINT OF WEAKNESS (PoW) STRESS (Portfolio-Specific)                                 │
│     ─────────────────────────────────────────────────────────────────────────────────   │
│     • Portfolio-specific stress tests targeting identified vulnerabilities              │
│     • Triggered by Top Risk Analysis identifying material exposures                     │
│     • Bottom-up approach: Portfolio risk → Relevant stress scenario                     │
│     • May focus on single asset class or desk                                           │
│     • Risks of interest:                                                                │
│       - Concentration (single name, sector, geography)                                  │
│       - Illiquidity (positions in illiquid markets/products)                            │
│       - Basis risk (cross-currency, asset swap, tenor basis)                            │
│       - Country/sovereign risk                                                          │
│       - Idiosyncratic risk (single-name equity, corporate)                              │
│       - Curve risk (specific tenor exposures)                                           │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  STRESS SCENARIO TYPES                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  1. HISTORICAL SCENARIOS                                                                │
│     Replay of actual market events                                                      │
│     • 2008 Global Financial Crisis (Lehman)                                             │
│     • 2010 European Sovereign Debt Crisis                                               │
│     • 2015 CNY Devaluation / Swiss Franc De-peg                                         │
│     • 2020 COVID-19 Market Shock                                                        │
│     • 2022 UK LDI / Gilt Crisis                                                         │
│                                                                                         │
│  2. HYPOTHETICAL SCENARIOS                                                              │
│     Forward-looking scenarios designed for current risk profile                         │
│     • Geopolitical scenarios (e.g., Taiwan conflict, Russia escalation)                 │
│     • Macroeconomic scenarios (e.g., global recession, stagflation)                     │
│     • Market structure scenarios (e.g., liquidity crisis, correlation breakdown)        │
│     • Climate scenarios (e.g., disorderly transition, physical risk event)              │
│                                                                                         │
│  3. REVERSE STRESS TESTS                                                                │
│     Identify scenarios that could threaten viability                                    │
│     • What would cause capital ratio to fall below minimum?                             │
│     • What would cause liquidity stress?                                                │
│     • What would cause operational failure?                                             │
│                                                                                         │
│  4. SENSITIVITY ANALYSIS                                                                │
│     Single risk factor shocks                                                           │
│     • Parallel rate shifts (±100bps, ±200bps)                                           │
│     • Credit spread widening (±50bps, ±100bps)                                          │
│     • FX moves (±10%, ±20%)                                                             │
│     • Equity index moves (±20%, ±40%)                                                   │
│                                                                                         │
│  5. EXTERNAL/AD-HOC SCENARIOS                                                           │
│     Scenarios requested by external bodies or committees                                │
│     • Stress Test Forum requests                                                        │
│     • Regulatory ad-hoc scenarios (PRA, EBA)                                            │
│     • Board/ExCo specific requests                                                      │
│     • Note: Require interpretation step before parameterisation                         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Process Overview

### 3.1 Annual Stress Testing Cycle

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     ANNUAL STRESS TESTING CYCLE                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Q1: SCENARIO REVIEW AND DEVELOPMENT                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Review existing scenarios for relevance                                              │
│  • Identify new scenarios based on emerging risks                                       │
│  • Front Office consultation on plausibility                                            │
│  • RMA draft parameterisation                                                           │
│                                                                                         │
│  Q2: SCENARIO PARAMETERISATION AND VALIDATION                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Detailed parameterisation of risk factor shocks                                      │
│  • Front Office review of shock magnitudes                                              │
│  • Independent validation by RMA                                                        │
│  • MLRC review and challenge                                                            │
│                                                                                         │
│  Q3: APPROVAL AND IMPLEMENTATION                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • MLRC approval of scenario suite                                                      │
│  • Implementation in Risk Engine                                                        │
│  • Parallel run with existing scenarios                                                 │
│  • Update limits if required                                                            │
│                                                                                         │
│  Q4: ONGOING MONITORING AND AD-HOC UPDATES                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Monthly stress P&L monitoring                                                        │
│  • Ad-hoc scenario updates for significant events                                       │
│  • Year-end reporting for ICAAP                                                         │
│  • Preparation for next annual cycle                                                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 High-Level Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     STRESS SCENARIO DEVELOPMENT PROCESS                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────┐
    │   0. TOP RISK        │
    │   ANALYSIS           │
    │   (For PoW Stress)   │
    │                      │
    │   Identify:          │
    │   • Concentration    │
    │   • Illiquidity      │
    │   • Basis risk       │
    │   • Country risk     │
    │   • Curve risk       │
    │                      │
    │   Owner: RMA         │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   1. SCENARIO        │
    │   IDENTIFICATION     │
    │                      │
    │   Inputs:            │
    │   • Market research  │
    │   • Emerging risks   │
    │   • Historical events│
    │   • FO feedback      │
    │   • Top Risk output  │
    │                      │
    │   Decision:          │
    │   Pillar or PoW?     │
    │                      │
    │   Owner: RMA         │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   2. FRONT OFFICE    │
    │   CONSULTATION       │
    │                      │
    │   Purpose:           │
    │   • Plausibility     │
    │   • Market dynamics  │
    │   • Missing factors  │
    │   • Shock magnitudes │
    │                      │
    │   Note: For PoW,     │
    │   engage desk heads  │
    │   EARLY in design    │
    │                      │
    │   Owner: FO + RMA    │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   3. SCENARIO        │
    │   PARAMETERISATION   │
    │                      │
    │   Deliverables:      │
    │   • Risk factor list │
    │   • Shock magnitudes │
    │   • Correlations     │
    │   • Time horizon     │
    │                      │
    │   Output: Excel      │
    │   "Golden Source"    │
    │                      │
    │   Owner: RMA         │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   4. VALIDATION      │
    │   & REVIEW           │
    │                      │
    │   Activities:        │
    │   • Historical test  │
    │   • Coherence check  │
    │   • FO sign-off      │
    │   • RMA validation   │
    │                      │
    │   Owner: RMA         │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   5. MLRC APPROVAL   │
    │                      │
    │   Approval of:       │
    │   • Scenario suite   │
    │   • Parameterisation │
    │   • Limits mapping   │
    │   • Implementation   │
    │                      │
    │   Output: Approved   │
    │   Excel Golden Source│
    │                      │
    │   Owner: MLRC        │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │   6. SYSTEM          │
    │   IMPLEMENTATION     │
    │                      │
    │   Activities:        │
    │   • Upload to Risk   │
    │     Engine           │
    │   • Reconciliation   │
    │     vs Golden Source │
    │   • UAT testing      │
    │   • Go-live          │
    │                      │
    │   Owner: RAV/        │
    │   Risk Tech          │
    └──────────────────────┘
```

### 3.3 Pillar Stress vs Point of Weakness Workflow

| Aspect | Pillar Stress | Point of Weakness (PoW) |
|--------|---------------|------------------------|
| **Trigger** | Annual review cycle, market events | Top Risk Analysis identifies vulnerability |
| **Scope** | Firm-wide, all asset classes | Portfolio-specific, targeted |
| **Approach** | Top-down (narrative → shocks) | Bottom-up (risk → scenario) |
| **FO Engagement** | Workshop for plausibility | Early desk head involvement in design |
| **Calibration** | Historical crisis data (2008, 2020) | Tailored to specific risk |
| **Governance** | Full MLRC paper | MLRC approval (lighter governance) |
| **Examples** | Global Recession, Financial Crisis | EM Sovereign Concentration, EUR Credit Illiquidity |

---

## 4. Front Office Consultation

### 4.1 Purpose

Front Office consultation is **mandatory** for all hypothetical scenarios to ensure:

1. **Plausibility** - Scenarios represent realistic market dynamics
2. **Completeness** - All relevant risk factors are captured
3. **Coherence** - Shock directions and magnitudes are internally consistent
4. **Market Knowledge** - Incorporates FO expertise on correlations and second-order effects

### 4.2 Consultation Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     FRONT OFFICE CONSULTATION PROCESS                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  STEP 1: SCENARIO BRIEFING (RMA → FO)                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • RMA presents proposed scenario narrative and rationale                               │
│  • Initial list of risk factors identified                                              │
│  • Preliminary shock magnitudes based on historical analysis                            │
│  • Distribution to relevant desk heads (Rates, FX, Credit, Equities, Commodities)       │
│                                                                                         │
│  STEP 2: FO FEEDBACK SESSION (Workshop Format)                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Participants:                                                                          │
│  • RMA (Chair)                                                                          │
│  • Market Risk                                                                          │
│  • Relevant Desk Heads and Senior Traders                                               │
│  • Trading Strategists                                                                  │
│                                                                                         │
│  Agenda:                                                                                │
│  1. Scenario narrative review                                                           │
│  2. Risk factor completeness check                                                      │
│  3. Shock magnitude challenge                                                           │
│  4. Correlation and second-order effects discussion                                     │
│  5. Missing dynamics identification                                                     │
│                                                                                         │
│  STEP 3: FEEDBACK DOCUMENTATION (RMA)                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Document all FO feedback and rationale                                               │
│  • Record areas of agreement and disagreement                                           │
│  • Note any recommended shock adjustments                                               │
│  • Capture additional risk factors suggested                                            │
│                                                                                         │
│  STEP 4: REVISED PARAMETERISATION (RMA)                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Incorporate FO feedback into scenario parameters                                     │
│  • Document rationale for any feedback not incorporated                                 │
│  • Circulate revised scenario for FO confirmation                                       │
│                                                                                         │
│  STEP 5: FO SIGN-OFF                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Relevant desk heads sign off on plausibility                                         │
│  • Sign-off recorded in scenario documentation                                          │
│  • Disagreements escalated to Head of Trading and MLRC                                  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 FO Consultation Requirements by Scenario Type

| Scenario Type | FO Consultation Required | Scope |
|---------------|-------------------------|-------|
| **Historical** | Recommended | Review for current portfolio relevance |
| **Hypothetical** | **Mandatory** | Full consultation process |
| **Reverse Stress** | **Mandatory** | Identify plausible triggers |
| **Sensitivity** | Not required | Standard parameterisation |

### 4.4 Documentation Requirements

| Document | Content | Owner |
|----------|---------|-------|
| **Consultation Request** | Scenario narrative, preliminary parameters, questions for FO | RMA |
| **Workshop Minutes** | Attendees, discussion points, feedback, action items | RMA |
| **Feedback Response** | How FO feedback was incorporated (or not) with rationale | RMA |
| **FO Sign-off Form** | Desk head signatures confirming plausibility | FO |

---

## 5. Scenario Parameterisation

### 5.1 Parameterisation Framework

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     SCENARIO PARAMETERISATION FRAMEWORK                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  RISK FACTOR CATEGORIES                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  1. INTEREST RATES                                                                      │
│     ├── Government yield curves (by currency, tenor)                                    │
│     ├── Swap curves (SOFR, ESTER, SONIA, TONAR)                                         │
│     ├── Basis spreads (OIS/LIBOR, cross-currency)                                       │
│     └── Volatilities (swaption vols by expiry/tenor)                                    │
│                                                                                         │
│  2. CREDIT                                                                              │
│     ├── Sovereign spreads (by country, rating)                                          │
│     ├── Corporate spreads (by sector, rating, seniority)                                │
│     ├── CDS indices (CDX, iTraxx)                                                       │
│     └── Recovery rates (by sector, seniority)                                           │
│                                                                                         │
│  3. FOREIGN EXCHANGE                                                                    │
│     ├── Spot rates (vs. USD, cross rates)                                               │
│     ├── FX volatilities (by tenor)                                                      │
│     └── FX forward points                                                               │
│                                                                                         │
│  4. EQUITIES                                                                            │
│     ├── Equity indices (regional)                                                       │
│     ├── Sector indices                                                                  │
│     ├── Single stocks (if concentrated)                                                 │
│     └── Equity volatilities                                                             │
│                                                                                         │
│  5. COMMODITIES                                                                         │
│     ├── Oil prices (Brent, WTI)                                                         │
│     ├── Gas prices (TTF, Henry Hub)                                                     │
│     ├── Precious metals (Gold, Silver)                                                  │
│     └── Agricultural (if applicable)                                                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Parameterisation Standards

| Standard | Description | Rationale |
|----------|-------------|-----------|
| **Historical Calibration** | Shocks calibrated to historical worst-case where possible | Empirical grounding |
| **Coherence** | Related risk factors move in consistent directions | Scenario plausibility |
| **Severity** | Shocks at minimum 99th percentile of historical distribution | Regulatory expectation |
| **Completeness** | All material risk factors included | No hidden risks |
| **Documentation** | Full rationale for each shock magnitude | Audit trail |

### 5.3 Shock Magnitude Guidelines

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     SHOCK MAGNITUDE GUIDELINES                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  INTEREST RATES                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Scenario Type          │ Short End (≤2Y) │ Long End (10Y+) │ Calibration               │
│  ───────────────────────┼─────────────────┼─────────────────┼─────────────────────────  │
│  Moderate stress        │ ±50bps          │ ±30bps          │ ~2 std dev (monthly)      │
│  Severe stress          │ ±100bps         │ ±75bps          │ ~3 std dev (monthly)      │
│  Extreme stress         │ ±200bps         │ ±150bps         │ 2008/2022 calibration     │
│                                                                                         │
│  CREDIT SPREADS                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Scenario Type          │ IG Spreads      │ HY Spreads      │ Calibration               │
│  ───────────────────────┼─────────────────┼─────────────────┼─────────────────────────  │
│  Moderate stress        │ +50bps          │ +150bps         │ ~2 std dev (monthly)      │
│  Severe stress          │ +100bps         │ +300bps         │ ~3 std dev (monthly)      │
│  Extreme stress         │ +200bps         │ +600bps         │ 2008/2020 calibration     │
│                                                                                         │
│  FOREIGN EXCHANGE                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Scenario Type          │ G10 Pairs       │ EM Pairs        │ Calibration               │
│  ───────────────────────┼─────────────────┼─────────────────┼─────────────────────────  │
│  Moderate stress        │ ±5%             │ ±10%            │ ~2 std dev (monthly)      │
│  Severe stress          │ ±10%            │ ±20%            │ ~3 std dev (monthly)      │
│  Extreme stress         │ ±20%            │ ±40%            │ GFC/COVID calibration     │
│                                                                                         │
│  EQUITIES                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Scenario Type          │ DM Indices      │ EM Indices      │ Calibration               │
│  ───────────────────────┼─────────────────┼─────────────────┼─────────────────────────  │
│  Moderate stress        │ -10%            │ -15%            │ ~2 std dev (monthly)      │
│  Severe stress          │ -20%            │ -30%            │ ~3 std dev (monthly)      │
│  Extreme stress         │ -40%            │ -50%            │ 2008/2020 calibration     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.4 Parameterisation Document Template

Each scenario must have a formal parameterisation document including:

| Section | Content |
|---------|---------|
| **1. Scenario Narrative** | Description of the stress event and market dynamics |
| **2. Historical Precedent** | Reference to historical events (if applicable) |
| **3. Risk Factor List** | Complete list of shocked risk factors |
| **4. Shock Magnitudes** | Specific shock values with rationale for each |
| **5. Correlations** | Expected correlation changes (if modelled) |
| **6. Time Horizon** | Instantaneous vs. phased shock |
| **7. FO Consultation** | Summary of FO feedback and how incorporated |
| **8. Calibration Evidence** | Historical data, statistical analysis supporting shocks |
| **9. Approval** | RMA sign-off, FO sign-off |

---

## 6. Validation and Review

### 6.1 RMA Validation

| Validation Check | Description | Threshold |
|------------------|-------------|-----------|
| **Completeness** | All material risk factors included | 100% coverage |
| **Coherence** | Shocks move in consistent directions | No contradictions |
| **Severity** | Shocks meet minimum severity standards | ≥99th percentile |
| **Historical Test** | Scenario would have captured past events | Passes back-test |
| **Documentation** | Full parameterisation document complete | All sections |

### 6.2 Annual Review

| Activity | Timing | Owner |
|----------|--------|-------|
| Review scenario relevance | Q1 | RMA |
| Identify emerging risks | Q1 | RMA + Market Risk |
| FO consultation on new/revised scenarios | Q1-Q2 | RMA + FO |
| Update parameterisation | Q2 | RMA |
| MLRC approval | Q3 | MLRC |
| Implementation | Q3 | Risk Tech |
| Documentation update | Q4 | RMA |

---

## 7. Governance

### 7.1 MLRC Oversight

| Activity | MLRC Role |
|----------|-----------|
| **Annual Scenario Review** | Approve scenario suite for coming year |
| **New Scenario Approval** | Approve any new hypothetical scenarios |
| **Parameterisation Challenge** | Challenge and approve shock magnitudes |
| **Ad-Hoc Updates** | Approve material changes to existing scenarios |
| **Stress Limit Review** | Review stress limits in context of scenarios |

### 7.2 Approval Authorities

| Change Type | Approval Authority | Documentation |
|-------------|-------------------|---------------|
| **New Scenario** | MLRC | Full parameterisation document |
| **Material Parameterisation Change** (>20% shock change) | MLRC | Updated parameterisation with rationale |
| **Minor Parameterisation Change** (<20% shock change) | Head of RMA | Change log with rationale |
| **Administrative Update** (documentation) | RMA | Updated document |

### 7.3 Escalation

| Issue | Escalation Path | Resolution |
|-------|----------------|------------|
| FO disagrees with scenario plausibility | RMA → Head of Trading → MLRC | MLRC decision |
| RMA disagrees with FO shock recommendations | RMA → Head of Market Risk → MLRC | MLRC decision |
| Scenario produces unexpected results | RMA → Market Risk → MLRC | Investigation and remediation |

---

## 8. System Implementation

### 8.1 Golden Source Concept

The MLRC-approved parameterisation is maintained in Excel as the **"Golden Source"**. This ensures:

1. **Single Source of Truth** - One authoritative record of approved shocks
2. **Audit Trail** - Clear linkage from MLRC approval to system implementation
3. **Reconciliation Basis** - System parameters can be verified against approved values

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     PARAMETER DATA FLOW                                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐        │
│   │  RMA        │      │  MLRC       │      │  RAV        │      │  Risk       │        │
│   │  Param-     │ ──▶  │  Approval   │ ──▶  │  Upload     │ ──▶  │  Engine     │        │
│   │  eterisation│      │             │      │             │      │             │        │
│   └─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘        │
│         │                    │                    │                    │                │
│         ▼                    ▼                    ▼                    ▼                │
│   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐        │
│   │  Draft      │      │  Approved   │      │  System     │      │  Stress     │        │
│   │  Excel      │      │  Excel      │      │  Config     │      │  P&L        │        │
│   │             │      │  GOLDEN     │      │             │      │  Output     │        │
│   │             │      │  SOURCE     │      │             │      │             │        │
│   └─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘        │
│                              │                    │                                     │
│                              │    RECONCILE       │                                     │
│                              └────────────────────┘                                     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Implementation Process

| Step | Activity | Owner | Output |
|------|----------|-------|--------|
| 1 | Receive MLRC-approved Excel golden source | RAV | Approved parameter file |
| 2 | Technical review of parameter formats | RAV | Validation checklist |
| 3 | Upload parameters to Risk Engine | RAV | System configuration |
| 4 | **Reconciliation**: Risk Engine vs Excel golden source | RAV | Reconciliation report |
| 5 | UAT testing of stress P&L calculation | RAV + RMA | Test results |
| 6 | Production go-live | Risk Tech | Live scenarios |

### 8.3 Reconciliation Control (CRITICAL)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     PARAMETER RECONCILIATION                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  PURPOSE: Verify Risk Engine parameters match MLRC-approved Golden Source               │
│                                                                                         │
│  SCOPE:                                                                                 │
│  • All risk factor shocks by asset class                                                │
│  • Tenor structures (by maturity bucket)                                                │
│  • Currency pairs and regional differentiation                                          │
│  • Scenario metadata (name, type, severity)                                             │
│                                                                                         │
│  TOLERANCE: ZERO - Parameters must match EXACTLY                                        │
│                                                                                         │
│  FREQUENCY: At implementation and after any parameter change                            │
│                                                                                         │
│  DECISION:                                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  MATCH     → Proceed to UAT and go-live                                                 │
│  MISMATCH  → Investigate, correct system config, re-reconcile                           │
│             (Do NOT proceed until reconciliation passes)                                │
│                                                                                         │
│  EVIDENCE: Reconciliation report retained as audit evidence                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 8.4 Golden Source Contents

The Excel golden source must contain:

| Tab | Content | Format |
|-----|---------|--------|
| **Cover** | Scenario name, type, MLRC approval date, version | Metadata |
| **Narrative** | Economic narrative, trigger, transmission | Text |
| **Rates_FX** | Interest rate and FX shocks by currency/tenor | Parameter table |
| **Credit** | Spread shocks by rating/sector/seniority | Parameter table |
| **Equities** | Index and volatility shocks by region | Parameter table |
| **Commodities** | Energy, precious metals, base metals shocks | Parameter table |
| **Validation** | Coherence checks, historical comparison | Validation results |
| **Approvals** | RMA sign-off, FO sign-off, MLRC reference | Governance |

---

## 9. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| ST-C01 | FO consultation completed for all hypothetical scenarios | Preventive | RMA |
| ST-C02 | Full parameterisation document maintained for each scenario | Preventive | RMA |
| ST-C03 | Annual review of scenario suite completed | Detective | RMA |
| ST-C04 | MLRC approval obtained before implementation | Preventive | RMA |
| ST-C05 | Scenario shocks meet minimum severity standards (≥99th percentile) | Detective | RMA |
| ST-C06 | FO sign-off obtained on plausibility | Preventive | RMA |
| ST-C07 | Historical scenarios updated for current market levels | Detective | RMA |
| ST-C08 | Reverse stress tests performed annually | Detective | RMA |
| ST-C09 | **Golden Source reconciliation**: Risk Engine params match MLRC-approved Excel | Detective | RAV |
| ST-C10 | Top Risk Analysis performed before PoW scenario design | Preventive | RMA |
| ST-C11 | Desk heads engaged early for Point of Weakness scenarios | Preventive | RMA |

---

## 10. Service Levels

| Activity | Target | Threshold | Escalation |
|----------|--------|-----------|------------|
| FO consultation completion | 4 weeks from initiation | 6 weeks | Head of RMA |
| Parameterisation document completion | 2 weeks from FO sign-off | 4 weeks | Head of RMA |
| MLRC approval turnaround | 2 MLRC cycles | 3 cycles | CRO |
| Implementation after approval | 4 weeks | 6 weeks | Head of Risk Tech |
| Annual review completion | Q3 | Q4 | Head of RMA |

---

## 11. Stress P&L Calculation

### 11.1 Risk Engine Integration

Stress P&L calculation is **orchestrated through the Risk Engine** as one of three parallel calculation streams, alongside VaR/SVaR and Sensitivities/Position Reporting. This ensures consistent methodology, data sourcing, and hierarchy aggregation across all market risk metrics.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     RISK ENGINE - THREE PARALLEL CALCULATION STREAMS                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  All three streams share COMMON INPUTS:                                                 │
│  • Valuations ODS: MTM, sensitivities (DV01, CS01, Vega, Delta, Gamma)                  │
│  • Hierarchy ODS: Book → Desk → Business → Division → Entity structure                  │
│  • Time Series ODS: Historical returns, stressed period returns                         │
│                                                                                         │
│  ════════════════════════════════════════════════════════════════════════════════════   │
│                                                                                         │
│  STREAM 1: SENSITIVITIES & POSITION REPORTING                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Input: Sensitivities from Valuations ODS                                             │
│  • Calculation: Aggregation of Greeks up hierarchy                                      │
│  • Output: DV01, CS01, Vega by desk/entity; Position limits; Concentration metrics      │
│  • Frequency: Intraday (hourly refresh)                                                 │
│                                                                                         │
│  STREAM 2: VaR / SVaR CALCULATION                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Input: Sensitivities + Historical returns (500+ days)                                │
│  • Calculation: P&L Strip → Hierarchy Aggregation → Percentile extraction               │
│  • Output: VaR/SVaR by hierarchy level, risk factor contributions                       │
│  • Frequency: Daily (T+1 overnight batch)                                               │
│                                                                                         │
│  STREAM 3: STRESS TESTING                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Input: Sensitivities/Positions + MLRC-approved scenario shocks                       │
│  • Calculation: Stress P&L per scenario → Hierarchy Aggregation                         │
│  • Output: Stress P&L by scenario and hierarchy level, limit utilisation                │
│  • Frequency: Daily (overnight batch, can also run weekly for full suite)               │
│                                                                                         │
│  ════════════════════════════════════════════════════════════════════════════════════   │
│                                                                                         │
│  KEY BENEFITS OF UNIFIED RISK ENGINE ORCHESTRATION:                                     │
│  • Consistent data sourcing (same valuations, same hierarchy)                           │
│  • Comparable results (VaR vs Stress P&L using same positions)                          │
│  • Single point of control for batch scheduling and monitoring                          │
│  • Unified audit trail across all risk metrics                                          │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 11.2 Stress P&L Calculation Methods

Similar to VaR, stress P&L uses two calculation methods based on product complexity:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     STRESS P&L CALCULATION METHODS                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  METHOD 1: SENSITIVITY-BASED (Linear/Near-Linear Products)                              │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  For each scenario s and each position p:                                               │
│                                                                                         │
│  Stress_P&L(p, s) = Σ [Sensitivity(p, rf) × Shock(s, rf)]                               │
│                     for all risk factors rf                                             │
│                                                                                         │
│  EXAMPLE: EUR 5Y Swap under "Global Recession" scenario                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Risk Factor      │ Sensitivity │ Scenario Shock │ Contribution              │    │
│  │──────────────────────────────────────────────────────────────────────────────│    │
│  │  EUR-ESTER-2Y     │ DV01: -€50k │ -50 bps        │ +€2,500,000               │    │
│  │  EUR-ESTER-5Y     │ DV01: -€80k │ -75 bps        │ +€6,000,000               │    │
│  │  EUR-ESTER-10Y    │ DV01: -€30k │ -60 bps        │ +€1,800,000               │    │
│  │  EUR-USD FX       │ Delta: €2M  │ -10%           │ -€200,000                 │    │
│  │──────────────────────────────────────────────────────────────────────────────│    │
│  │  TOTAL STRESS P&L                                │ +€10,100,000              │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  USED FOR: Vanilla swaps, FX spot/forwards, cash bonds, linear derivatives, CDS         │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  METHOD 2: FULL REVALUATION (Complex/Non-Linear Products)                               │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  For complex positions where sensitivity-based approximation is inadequate:             │
│                                                                                         │
│  Stress_P&L(p, s) = MTM(p, shocked_prices) - MTM(p, current_prices)                     │
│                                                                                         │
│  Process:                                                                               │
│  1. Apply scenario shocks to all relevant market data (rates, vols, spots)              │
│  2. Fully reprice position using valuation model with shocked market data               │
│  3. Calculate difference from current MTM                                               │
│                                                                                         │
│  EXAMPLE: EUR/USD FX Option under "Global Recession" scenario                           │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Current MTM:     €1,500,000                                                    │    │
│  │                                                                                 │    │
│  │  Shocked Market Data:                                                           │    │
│  │  • EUR/USD Spot: 1.10 → 0.99 (-10%)                                             │    │
│  │  • EUR/USD Vol 3M: 8% → 18% (+10 vol pts)                                       │    │
│  │  • EUR rates: -75 bps                                                           │    │
│  │  • USD rates: -50 bps                                                           │    │
│  │                                                                                 │    │
│  │  Shocked MTM:     €2,800,000 (full revaluation)                                 │    │
│  │  Stress P&L:      +€1,300,000                                                   │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  USED FOR: Options (FX, IR, Equity, Commodity), swaptions, structured products, exotics │
│                                                                                         │
│  NOTE: Captures gamma, vega, and cross-effects not captured by sensitivity-based method │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 11.3 Hybrid Approach - Product Classification

Meridian Global Bank uses a hybrid approach consistent with VaR calculation:

| Product Type | Stress P&L Method | Rationale |
|--------------|-------------------|-----------|
| **Vanilla swaps** | Sensitivity-based | Linear payoff; DV01/CS01 sufficient |
| **FX spot/forwards** | Sensitivity-based | Linear; Delta sufficient |
| **Cash bonds** | Sensitivity-based | Near-linear; DV01 + CS01 |
| **CDS** | Sensitivity-based | Linear in spread; CS01 sufficient |
| **FX options** | Full revaluation | Non-linear; significant vega/gamma effects |
| **IR swaptions** | Full revaluation | Non-linear; vega and convexity |
| **Equity options** | Full revaluation | Non-linear; vol smile effects |
| **Structured products** | Full revaluation | Path-dependent and complex payoffs |
| **Exotic options** | Full revaluation | Complex payoffs requiring full model |

### 11.4 Stress P&L Aggregation

After position-level calculation, stress P&L is aggregated up the hierarchy:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     STRESS P&L AGGREGATION                                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  For each scenario s and hierarchy node n:                                              │
│                                                                                         │
│  Aggregated_Stress_P&L(n, s) = Σ Stress_P&L(p, s)                                       │
│                                for all positions p in node n                            │
│                                                                                         │
│  NOTE: Unlike VaR, stress P&L for a scenario is additive (no diversification effect     │
│  within a single scenario - all positions experience same market shocks)                │
│                                                                                         │
│  EXAMPLE: "Global Recession" Scenario - Aggregation                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                                                                                 │    │
│  │  POSITION LEVEL:                                                                │    │
│  │  TRD-001 (EUR 5Y Swap):     +€10.1M                                             │    │
│  │  TRD-002 (USD 10Y Swap):    +€5.2M                                              │    │
│  │  TRD-003 (EUR/USD Option):  +€1.3M                                              │    │
│  │  TRD-004 (GBP Bond):        -€2.4M                                              │    │
│  │                                                                                 │    │
│  │  BOOK LEVEL:                                                                    │    │
│  │  EUR-RATES-LON-01: +€10.1M + €5.2M = +€15.3M                                    │    │
│  │  FX-OPTIONS-LON-01: +€1.3M                                                      │    │
│  │  GBP-CREDIT-LON-01: -€2.4M                                                      │    │
│  │                                                                                 │    │
│  │  DESK LEVEL:                                                                    │    │
│  │  EUR Rates London: +€15.3M                                                      │    │
│  │  FX Options London: +€1.3M                                                      │    │
│  │  GBP Credit London: -€2.4M                                                      │    │
│  │                                                                                 │    │
│  │  ENTITY LEVEL:                                                                  │    │
│  │  Meridian Bank UK: +€15.3M + €1.3M - €2.4M = +€14.2M                            │    │
│  │                                                                                 │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 11.5 Daily Stress P&L Production

Daily stress P&L is produced as part of the Risk Engine overnight batch:

| Stage | Timing | Activities |
|-------|--------|------------|
| **Input validation** | 22:00-22:15 GMT | Verify valuations, hierarchy, scenario parameters |
| **Stress calculation** | 01:00-02:00 GMT+1 | Calculate stress P&L for all scenarios (parallel to VaR) |
| **Aggregation** | 02:00-02:30 GMT+1 | Aggregate up hierarchy for all scenarios |
| **Output validation** | 02:30-03:00 GMT+1 | Compare vs. T-1, verify limit calculations |
| **Write to Risk ODS** | 03:00-03:30 GMT+1 | Store results for reporting and analysis |

### 11.6 Stress P&L Outputs

| Output | Hierarchy | Frequency | Consumer |
|--------|-----------|-----------|----------|
| **Stress P&L by Scenario** | Entity, Division, Business, Desk | Daily | Market Risk, FO |
| **Stress P&L by Risk Factor** | Contribution within scenario | Daily | Market Risk, RMA |
| **Stress Limit Utilisation** | Entity, Division | Daily | Market Risk, MLRC |
| **Stress vs. VaR Ratio** | Entity, by scenario | Daily | Market Risk |
| **Worst Scenario Identifier** | Entity | Daily | Market Risk, MLRC |
| **Stress P&L Attribution** | By desk/asset class within scenario | Weekly | MLRC Pack |

### 11.7 Relationship to VaR Calculation

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     STRESS P&L vs VaR COMPARISON                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ASPECT              │  VaR CALCULATION           │  STRESS P&L CALCULATION             │
│  ───────────────────────────────────────────────────────────────────────────────────    │
│  SCENARIOS           │  500+ historical days      │  ~20 predefined scenarios           │
│                      │  (actual market moves)     │  (designed scenarios)               │
│                                                                                         │
│  SHOCK SOURCE        │  Time Series ODS           │  MLRC-approved Golden Source        │
│                      │  (historical returns)      │  (scenario parameters)              │
│                                                                                         │
│  OUTPUT              │  99th percentile loss      │  P&L for each scenario              │
│                      │  (single number)           │  (vector of ~20 numbers)            │
│                                                                                         │
│  AGGREGATION         │  P&L strips summed, then   │  P&L summed directly                │
│                      │  percentile extracted      │  (additive per scenario)            │
│                                                                                         │
│  DIVERSIFICATION     │  Captured (percentile of   │  Not applicable within scenario     │
│                      │  portfolio distribution)   │  (all positions same shock)         │
│                                                                                         │
│  USE CASE            │  Day-to-day risk limit     │  Tail risk, capital planning,       │
│                      │  monitoring                │  recovery planning                  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 12. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [Risk Engine Calculation](./risk-engine-calculation.md) | Stress P&L calculation engine |
| [Stress Limits Controls](../L5-Controls/market-risk/stress-limits-controls.md) | Limit monitoring for stress scenarios |
| [Market Risk Policy](../L3-Governance/policies/market-risk-policy.md) | Governance framework |
| [MLRC Terms of Reference](../L3-Governance/committees/mlrc-terms-of-reference.md) | Approval authority |
| [Pillar Stress Generator Skill](/.claude/skills/pillar-stress-generator/) | AI-assisted scenario parameterisation |

---

## 13. Document Control

### 13.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-16 | Initial version | MLRC |
| 1.1 | 2025-01-16 | Enhanced with ICBCS learnings: Pillar vs PoW distinction, Top Risk Analysis, Golden Source concept, reconciliation control | MLRC |
| 1.2 | 2025-01-16 | Expanded Section 11 (Stress P&L Calculation) to show Risk Engine orchestration with three parallel streams (Sensitivities, VaR/SVaR, Stress), added hybrid calculation methods (sensitivity-based vs full revaluation), detailed aggregation process | MLRC |

---

*End of Document*
