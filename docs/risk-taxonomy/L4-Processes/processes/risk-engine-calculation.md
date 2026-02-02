---
# Process Metadata
process_id: MR-L4-006
process_name: Risk Engine Calculation
version: 1.9
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Risk Engine Operations
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-001  # Market Risk Process Orchestration (orchestration)
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-003  # FRTB
  - REQ-L1-022  # BCBS 239
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-003   # VaR Limit Framework
  - GOV-L3-010  # Risk Appetite Statement (EaR/ECAP limits)
  - GOV-L3-011  # Risk Appetite Framework
l5_controls:
  - MR-L5-001   # VaR Limits
  - MR-L5-004   # Backtesting Exception Limits
l6_models:
  - MR-L6-001   # Historical Simulation VaR
  - MR-L6-002   # Stressed VaR
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-007  # Valuations ODS
  - SYS-MR-008  # Risk ODS
  - SYS-MR-010  # Time Series ODS
  - SYS-MR-011  # Hierarchy ODS
---

# Risk Engine Calculation Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-006 |
| **Version** | 1.9 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Market Risk Process Orchestration (MR-L4-001) |
| **Owner** | Head of Risk Engine Operations |

---

## 1. Purpose

The Risk Engine is the central calculation platform for all market risk metrics. It orchestrates **three parallel calculation streams** that share common inputs (valuations, hierarchy, time series) to ensure consistency across all risk measures:

1. **Sensitivities & Position Reporting** - Aggregated Greeks for intraday limit monitoring
2. **VaR/SVaR/ECAP/EaR Calculation** - Historical simulation VaR for daily risk limits, regulatory capital, economic capital (ICAAP), and earnings at risk (Risk Appetite)
3. **Stress Testing** - Scenario-based P&L for tail risk and capital planning

This document focuses primarily on the **VaR/SVaR/ECAP/EaR Calculation** stream, detailing the **3-Step VaR Calculation Chain**:

1. **P&L Strip Calculation** - Calculate hypothetical P&L for each position under each historical scenario
2. **Hierarchy Aggregation** - Sum P&L strips up the book hierarchy to desk, business, and entity level
3. **Percentile Calculation** - Extract VaR as the 99th percentile loss from the aggregated distribution

Economic Capital (ECAP) and Earnings at Risk (EaR) extend this calculation with different parameters - see Section 6.7 (ECAP: 99.9% confidence, asset-class liquidity horizons) and Section 6.8 (EaR: 90% confidence, 1-year horizon for Risk Appetite monitoring).

> **Note**:
> - Stress Testing is covered in detail in [Stress Testing (MR-L4-011)](./stress-testing.md)
> - Incremental Risk Charge (IRC) is covered in [IRC Calculation (MR-L4-010)](./irc-calculation.md)

---

## 1A. Three Parallel Calculation Streams

The Risk Engine processes three distinct but related calculation streams each day, all drawing from common data sources to ensure consistency:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                     RISK ENGINE - THREE PARALLEL CALCULATION STREAMS                        │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────┐│
│  │                            COMMON INPUTS (ODS Layer)                                    ││
│  │                                                                                         ││
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     ││
│  │  │  Valuations ODS │  │  Hierarchy ODS  │  │ Time Series ODS │  │ Scenario Params │     ││
│  │  │  • MTM          │  │  • Book→Entity  │  │  • 500+ days    │  │  • MLRC approved│     ││
│  │  │  • Sensitivities│  │  • COB valid    │  │  • Stressed     │  │  • Golden Source│     ││
│  │  │  • Greeks       │  │  • Desk mandates│  │  • All RF types │  │  • ~20 scenarios│     ││
│  │  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘     ││
│  │           │                    │                    │                    │              ││
│  └───────────┼────────────────────┼────────────────────┼────────────────────┼──────────────┘│
│              │                    │                    │                    │               │
│              └────────────────────┴────────────────────┴────────────────────┘               │
│                                          │                                                  │
│              ┌───────────────────────────┼───────────────────────────┐                      │
│              │                           │                           │                      │
│              ▼                           ▼                           ▼                      │
│  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐            │
│  │      STREAM 1         │  │      STREAM 2         │  │      STREAM 3         │            │
│  │   SENSITIVITIES &     │  │ VaR/SVaR/ECAP/EaR     │  │   STRESS TESTING      │            │
│  │ POSITION REPORTING    │  │   CALCULATION         │  │                       │            │
│  ├───────────────────────┤  ├───────────────────────┤  ├───────────────────────┤            │
│  │                       │  │                       │  │                       │            │
│  │ CALCULATION:          │  │ CALCULATION:          │  │ CALCULATION:          │            │
│  │ • Aggregate Greeks    │  │ • P&L Strip per pos   │  │ • Stress P&L per pos  │            │
│  │   up hierarchy        │  │ • Hierarchy aggreg    │  │   per scenario        │            │
│  │ • DV01, CS01, Vega    │  │ • 99th percentile     │  │ • Hierarchy aggreg    │            │
│  │   by desk/entity      │  │   extraction          │  │ • Limit utilisation   │            │
│  │                       │  │                       │  │                       │            │
│  │ METHOD:               │  │ METHOD:               │  │ METHOD:               │            │
│  │ • Direct aggregation  │  │ • Sensitivity-based   │  │ • Sensitivity-based   │            │
│  │   of sensitivities    │  │   (linear products)   │  │   (linear products)   │            │
│  │                       │  │ • Full revaluation    │  │ • Full revaluation    │            │
│  │                       │  │   (non-linear)        │  │   (non-linear)        │            │
│  │                       │  │                       │  │                       │            │
│  │ FREQUENCY:            │  │ FREQUENCY:            │  │ FREQUENCY:            │            │
│  │ • Intraday (hourly)   │  │ • Daily (T+1 batch)   │  │ • Daily (T+1 batch)   │            │
│  │                       │  │                       │  │ • Weekly (full suite) │            │
│  │                       │  │                       │  │                       │            │
│  │ TIMING:               │  │ TIMING:               │  │ TIMING:               │            │
│  │ • 08:00-18:00 each    │  │ • 22:00-03:30 GMT+1   │  │ • 22:00-03:30 GMT+1   │            │
│  │   regional COB        │  │                       │  │   (parallel to VaR)   │            │
│  │                       │  │                       │  │                       │            │
│  └───────────┬───────────┘  └───────────┬───────────┘  └───────────┬───────────┘            │
│              │                          │                          │                        │
│              ▼                          ▼                          ▼                        │
│  ┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐            │
│  │      OUTPUTS          │  │      OUTPUTS          │  │      OUTPUTS          │            │
│  ├───────────────────────┤  ├───────────────────────┤  ├───────────────────────┤            │
│  │ • Aggregated DV01     │  │ • VaR by hierarchy    │  │ • Stress P&L by       │            │
│  │ • Aggregated CS01     │  │ • SVaR by hierarchy   │  │   scenario & hierarchy│            │
│  │ • Aggregated Vega     │  │ • ECAP by hierarchy   │  │ • Stress limit        │            │
│  │ • Position limits     │  │ • EaR by hierarchy    │  │   utilisation         │            │
│  │ • Concentration       │  │ • Risk factor contribs│  │ • Worst scenario ID   │            │
│  │   metrics             │  │ • Marginal VaR        │  │ • Risk factor         │            │
│  │                       │  │ • Concentration VaR   │  │   contributions       │            │
│  │                       │  │                       │  │                       │            │
│  │ CONSUMERS:            │  │ CONSUMERS:            │  │ CONSUMERS:            │            │
│  │ • FO (real-time)      │  │ • Daily VaR Report    │  │ • Stress Report       │            │
│  │ • Market Risk (limits)│  │ • MLRC Pack           │  │ • MLRC Pack           │            │
│  │ • Regulatory (FRTB)   │  │ • Regulatory Capital  │  │ • ICAAP/Capital Plan  │            │
│  │                       │  │ • ICAAP (ECAP)        │  │ • Recovery Planning   │            │
│  │                       │  │ • Risk Appetite (EaR) │  │                       │            │
│  └───────────────────────┘  └───────────────────────┘  └───────────────────────┘            │
│                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1A.1 Stream Comparison

| Aspect | Stream 1: Sensitivities | Stream 2: VaR/SVaR/ECAP/EaR | Stream 3: Stress Testing |
|--------|-------------------------|------------------------------|--------------------------|
| **Purpose** | Position limits, intraday monitoring | Daily risk limits, regulatory & economic capital, Risk Appetite | Tail risk, capital planning, recovery |
| **Calculation** | Direct aggregation of Greeks | Historical simulation (500+ scenarios) | Scenario-based (20+ scenarios) |
| **Shock Source** | N/A (point-in-time sensitivities) | Time Series ODS (historical returns) | MLRC-approved Golden Source |
| **Output** | Aggregated sensitivities by hierarchy | VaR/SVaR at 99%, ECAP at 99.9%, EaR at 90% | Stress P&L per scenario |
| **Diversification** | Not applicable | Captured via percentile of portfolio | Not applicable (additive per scenario) |
| **Frequency** | Intraday (hourly) | Daily T+1 batch | Daily batch + weekly full suite |
| **Primary Consumer** | FO traders, intraday limits | VaR Limits, IMA Capital, ICAAP (ECAP), Risk Appetite (EaR) | Stress Limits, ICAAP, Board |

### 1A.2 Benefits of Unified Architecture

The three-stream architecture provides:

1. **Consistency** - All streams use same valuations, same hierarchy, same COB date
2. **Comparability** - VaR and Stress P&L calculated on identical positions
3. **Efficiency** - Common input validation, shared calculation grid
4. **Auditability** - Single source of truth for all market risk metrics
5. **Flexibility** - Can run streams independently (e.g., ad-hoc stress re-run)

---

## 2. Scope

### 2.1 Metrics Calculated

| Metric | Description | Use |
|--------|-------------|-----|
| **VaR (99%, 1-day)** | 99th percentile loss over 1-day horizon | IMA capital (scaled) |
| **VaR (99%, 10-day)** | VaR scaled by √10 for regulatory purposes | IMA capital |
| **Stressed VaR** | VaR using stressed market period | IMA capital |
| **ECAP (99.9%, liquidity-adjusted)** | Economic capital at 99.9% with asset-class liquidity horizons | ICAAP, internal capital |
| **EaR (90%, 1-year)** | Earnings at Risk scaled to 1-year horizon | Risk Appetite monitoring |
| **Risk Factor Contributions** | VaR attribution by risk factor | Risk management |
| **Marginal VaR** | Incremental VaR contribution per position | Risk management |

### 2.2 Hierarchy Levels

VaR is calculated at each level of the book hierarchy:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           BOOK HIERARCHY STRUCTURE                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Level 1: ENTERPRISE                                                                    │
│  └── Meridian Global Bank Group                                                         │
│                                                                                         │
│  Level 2: LEGAL ENTITY                                                                  │
│  ├── Meridian Bank UK (London)                                                          │
│  ├── Meridian Securities Asia (HK)                                                      │
│  └── Meridian Capital Markets (NY)                                                      │
│                                                                                         │
│  Level 3: DIVISION                                                                      │
│  ├── Global Markets                                                                     │
│  ├── Treasury                                                                           │
│  └── Principal Investments                                                              │
│                                                                                         │
│  Level 4: BUSINESS UNIT                                                                 │
│  ├── Rates Trading                                                                      │
│  ├── FX Trading                                                                         │
│  ├── Credit Trading                                                                     │
│  ├── Equities                                                                           │
│  └── Commodities                                                                        │
│                                                                                         │
│  Level 5: DESK                                                                          │
│  ├── EUR Rates London                                                                   │
│  ├── USD Rates NY                                                                       │
│  ├── G10 FX London                                                                      │
│  ├── Asia FX HK                                                                         │
│  └── ... (50+ desks)                                                                    │
│                                                                                         │
│  Level 6: BOOK (Lowest level with limit)                                                │
│  └── Individual trading books (e.g., EUR-RATES-LON-01, G10FX-LON-MM-01)                 │
│                                                                                         │
│  Level 7: POSITION / TRADE (Calculation level - no limit)                               │
│  └── Individual positions within books                                                  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Out of Scope

| Item | Reason |
|------|--------|
| **Valuation calculation** | Handled by Valuation Engine (upstream) |
| **Market data sourcing** | Handled by EOD Market Data Snapshot (MR-L4-003) |
| **Time series preparation** | Handled by Time Series Management (MR-L4-005) |
| **Reporting and sign-off** | Handled by VaR Reporting (MR-L4-007) |

---

## 3. Process Flow

### 3.1 High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     RISK ENGINE CALCULATION PROCESS                                     │
│                     (Daily 22:00 GMT - 04:00 GMT+1)                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [From Upstream Processes]
              │
              │   ┌─────────────────────────────────────────────────────────────────────┐
              │   │  INPUTS                                                             │
              │   │                                                                     │
              │   │  From Valuations ODS:                                               │
              │   │  • Mark-to-Market (MTM) by position                                 │
              │   │  • Sensitivities (DV01, CS01, Vega, Delta, Gamma)                   │
              │   │                                                                     │
              │   │  From Time Series ODS:                                              │
              │   │  • Historical returns for all risk factors (500+ days)              │
              │   │  • Stressed period returns (separate series)                        │
              │   │                                                                     │
              │   │  From Hierarchy ODS:                                                │
              │   │  • Book structure (position → book → desk → ... → entity)           │
              │   │  • Valid as-of COB date                                             │
              │   │                                                                     │
              │   │  From Risk Factor Setup:                                            │
              │   │  • Risk factor definitions                                          │
              │   │  • Position → Risk factor mappings                                  │
              │   └─────────────────────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         1. PRE-CALCULATION VALIDATION                                    │
│                         (22:00 - 22:15 GMT)                                              │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  INPUT VALIDATION                                                                   │ │
│  │                                                                                     │ │
│  │  • Valuations ODS: All desks populated (completeness check)                         │ │
│  │  • Time Series ODS: 500+ observations available for all required risk factors       │ │
│  │  • Hierarchy ODS: Valid structure as of COB date                                    │ │
│  │  • Risk Factor Mappings: No orphan positions (all positions mapped)                 │ │
│  │                                                                                     │ │
│  │  If validation fails → Alert Risk Engine Ops → Investigate/Fallback                 │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         2. P&L STRIP CALCULATION (STEP 1)                                │
│                         (22:15 - 01:00 GMT+1)                                            │
│                                                                                          │
│  See Section 4 for detailed methodology                                                  │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         3. HIERARCHY AGGREGATION (STEP 2)                                │
│                         (01:00 - 02:30 GMT+1)                                            │
│                                                                                          │
│  See Section 5 for detailed methodology                                                  │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         4. PERCENTILE CALCULATION (STEP 3)                               │
│                         (02:30 - 03:30 GMT+1)                                            │
│                                                                                          │
│  See Section 6 for detailed methodology                                                  │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         5. OUTPUT AND VALIDATION                                         │
│                         (03:30 - 04:00 GMT+1)                                            │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  OUTPUT VALIDATION                                                                  │ │
│  │                                                                                     │ │
│  │  • VaR calculated for all desks in hierarchy                                        │ │
│  │  • No calculation errors in batch log                                               │ │
│  │  • VaR within reasonable bounds vs. T-1 (>50% spike flagged)                        │ │
│  │  • Aggregation integrity: Sum of children ≠ parent (diversification expected)       │ │
│  │                                                                                     │ │
│  │  Outputs written to Risk ODS:                                                       │ │
│  │  • P&L strips (for audit)                                                           │ │
│  │  • Aggregated P&L distributions                                                     │ │
│  │  • VaR by hierarchy level                                                           │ │
│  │  • SVaR by hierarchy level                                                          │ │
│  │  • Risk factor contributions                                                        │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                                 [To VaR Reporting (MR-L4-007)]
```

---

## 4. Step 1: P&L Strip Calculation

### 4.1 Concept

A **P&L Strip** is a vector of hypothetical P&L outcomes for a single position, calculated by applying historical market shocks to today's position.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     P&L STRIP CALCULATION CONCEPT                                        │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  For each position and each historical scenario date (d), calculate:                     │
│                                                                                          │
│  P&L_strip(position, d) = MTM(position, shocked_prices) - MTM(position, today's_prices)  │
│                                                                                          │
│  Where:                                                                                  │
│  - shocked_prices = today's prices × (1 + return from date d)                            │
│  - return from date d = price change observed on historical date d                       │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                     │ │
│  │   TODAY'S POSITION        HISTORICAL RETURNS           P&L STRIP                    │ │
│  │   ─────────────────       ──────────────────           ─────────                    │ │
│  │                                                                                     │ │
│  │   EUR 10Y Swap            d1: EUR 10Y +2bps             d1: -$50,000                │ │
│  │   DV01 = -$25,000/bp      d2: EUR 10Y -5bps             d2: +$125,000               │ │
│  │                           d3: EUR 10Y +1bp              d3: -$25,000                │ │
│  │                           ...                           ...                         │ │
│  │                           d500: EUR 10Y -3bps           d500: +$75,000              │ │
│  │                                                                                     │ │
│  │   OUTPUT: P&L Strip = [-50k, +125k, -25k, ..., +75k]   (500+ values)                │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Calculation Methods

Two approaches are supported based on product complexity:

#### 4.2.1 Full Revaluation (Complex Products)

For positions with non-linear payoffs (options, structured products):

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     FULL REVALUATION METHOD                                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  For each position P and each scenario date d:                                          │
│                                                                                         │
│  1. Get today's prices: P_today = {S, σ, r, ...}                                        │
│  2. Get returns from date d: R_d = {ΔS/S, Δσ, Δr, ...}                                  │
│  3. Apply shocks: P_shocked = P_today × (1 + R_d)                                       │
│  4. Revalue position: MTM_shocked = Valuation_Model(P, P_shocked)                       │
│  5. Calculate P&L: P&L_strip(P, d) = MTM_shocked - MTM_today                            │
│                                                                                         │
│  Used for:                                                                              │
│  • Options (FX, IR, Equity, Commodity)                                                  │
│  • Structured products                                                                  │
│  • Exotics                                                                              │
│  • Any position where Greeks-based approximation is inadequate                          │
│                                                                                         │
│  Note: Computationally intensive - requires parallel processing                         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.2.2 Sensitivity-Based (Linear/Near-Linear Products)

For positions with linear or near-linear payoffs:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     SENSITIVITY-BASED METHOD (Taylor Expansion)                          │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  For each position P and each scenario date d:                                           │
│                                                                                          │
│  P&L_strip(P, d) ≈ Σ_i [Sensitivity_i × Shock_i(d)]                                      │
│                                                                                          │
│  Where:                                                                                  │
│  • Sensitivity_i = position sensitivity to risk factor i (DV01, CS01, Delta, etc.)       │
│  • Shock_i(d) = historical return of risk factor i on date d                             │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  EXAMPLE: Bond Position                                                             │ │
│  │                                                                                     │ │
│  │  Sensitivities:                     Shocks (scenario d = 15-Mar-2024):              │ │
│  │  • DV01 (10Y USD rate): -$50,000    • 10Y USD rate: +3.5 bps                        │ │
│  │  • CS01 (Credit spread): -$20,000   • Credit spread: +5 bps                         │ │
│  │                                                                                     │ │
│  │  P&L_strip = (-$50,000 × 3.5) + (-$20,000 × 5)                                      │ │
│  │           = -$175,000 + -$100,000                                                   │ │
│  │           = -$275,000                                                               │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  Used for:                                                                               │
│  • Cash bonds                                                                            │
│  • Interest rate swaps (vanilla)                                                         │
│  • FX spot/forwards                                                                      │
│  • Linear derivatives                                                                    │
│                                                                                          │
│  Advantage: Much faster than full revaluation                                            │
│  Limitation: May understate risk for positions with significant gamma/convexity          │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Hybrid Approach

In practice, Meridian Global Bank uses a **hybrid approach**:

| Product Type | Method | Justification |
|--------------|--------|---------------|
| **Vanilla swaps** | Sensitivity-based | Linear payoff; DV01 sufficient |
| **FX spot/forwards** | Sensitivity-based | Linear; Delta sufficient |
| **Cash bonds** | Sensitivity-based | Near-linear; DV01 + CS01 |
| **FX options** | Full revaluation | Non-linear; significant vega/gamma |
| **IR swaptions** | Full revaluation | Non-linear; vega risk |
| **Structured products** | Full revaluation | Path-dependent features |
| **CDS** | Sensitivity-based | Linear in spread; CS01 sufficient |
| **Exotic options** | Full revaluation | Complex payoffs |

### 4.4 Risk Factor Mapping

Each position is mapped to one or more risk factors for shock application:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     RISK FACTOR MAPPING                                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  POSITION: EUR 5Y Interest Rate Swap (€50M notional, pay fixed)                         │
│                                                                                         │
│  MAPPED RISK FACTORS:                                                                   │
│  ┌──────────────────────────┬─────────────────┬─────────────────────┬──────────────┐    │
│  │ Risk Factor              │ Type            │ Sensitivity         │ Weight       │    │
│  ├──────────────────────────┼─────────────────┼─────────────────────┼──────────────┤    │
│  │ EUR-ESTER-1Y             │ Interest Rate   │ DV01: -€1,200       │ 10%          │    │
│  │ EUR-ESTER-2Y             │ Interest Rate   │ DV01: -€4,800       │ 20%          │    │
│  │ EUR-ESTER-3Y             │ Interest Rate   │ DV01: -€6,000       │ 25%          │    │
│  │ EUR-ESTER-5Y             │ Interest Rate   │ DV01: -€8,000       │ 35%          │    │
│  │ EUR-ESTER-7Y             │ Interest Rate   │ DV01: -€2,000       │ 10%          │    │
│  │ EUR-ESTER-BASIS-3M6M     │ Basis           │ DV01: -€500         │ (residual)   │    │
│  └──────────────────────────┴─────────────────┴─────────────────────┴──────────────┘    │
│                                                                                         │
│  TOTAL DV01: -€22,500 per basis point                                                   │
│                                                                                         │
│  P&L Strip for this position aggregates shocks across all mapped risk factors           │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.5 Output: P&L Strip Matrix

The output of Step 1 is a matrix of P&L strips:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     P&L STRIP MATRIX (OUTPUT)                                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│                     Scenario Dates (500+ columns)                                       │
│                     d1      d2      d3      ...     d500                                │
│  ┌──────────────┬─────────────────────────────────────────┐                             │
│  │ Trade ID     │                                         │                             │
│  ├──────────────┼─────────────────────────────────────────┤                             │
│  │ TRD-001      │ -50k   +125k   -25k   ...   +75k        │                             │
│  │ TRD-002      │ +10k   -15k    +25k   ...   -40k        │                             │
│  │ TRD-003      │ -25k   +35k    -10k   ...   +5k         │                             │
│  │ ...          │  ...    ...     ...   ...    ...        │                             │
│  │ TRD-50000    │ +5k    -8k     +12k   ...   -3k         │                             │
│  └──────────────┴─────────────────────────────────────────┘                             │
│                                                                                         │
│  Stored in Risk ODS for:                                                                │
│  • Aggregation in Step 2                                                                │
│  • Audit trail                                                                          │
│  • Risk factor contribution analysis                                                    │
│  • Ad-hoc investigation                                                                 │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Step 2: Hierarchy Aggregation

### 5.1 Concept

Hierarchy aggregation sums the P&L strips from individual positions up through the book hierarchy. This produces a P&L distribution at each level.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     HIERARCHY AGGREGATION CONCEPT                                        │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  For each hierarchy node and each scenario date d:                                       │
│                                                                                          │
│  Aggregated_P&L(node, d) = Σ P&L_strip(position, d)                                      │
│                            for all positions within node                                 │
│                                                                                          │
│  This is a SIMPLE SUM - no diversification adjustment at this stage                      │
│  Diversification is captured naturally in the percentile calculation (Step 3)            │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                     │ │
│  │   BOOK: EUR-RATES-LON-01                                                            │ │
│  │   Positions in book:                                                                │ │
│  │   • TRD-001: [-50k, +125k, -25k, ...]                                               │ │
│  │   • TRD-002: [+30k, -40k, +60k, ...]                                                │ │
│  │   • TRD-003: [-10k, +15k, -5k, ...]                                                 │ │
│  │                                                                                     │ │
│  │   AGGREGATED P&L (Book level):                                                      │ │
│  │   Book P&L(d1) = -50k + 30k + (-10k) = -30k                                         │ │
│  │   Book P&L(d2) = +125k + (-40k) + 15k = +100k                                       │ │
│  │   Book P&L(d3) = -25k + 60k + (-5k) = +30k                                          │ │
│  │   ...                                                                               │ │
│  │                                                                                     │ │
│  │   Output: Book P&L Strip = [-30k, +100k, +30k, ...]                                 │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Aggregation Path

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     AGGREGATION PATH                                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Level 7: POSITIONS     Level 6: BOOKS        Level 5: DESKS        Level 4: BUSINESS   │
│  ─────────────────     ────────────────      ──────────────        ────────────────     │
│                                                                                         │
│  TRD-001 ─────┐                                                                         │
│  TRD-002 ─────┼──────▶ EUR-RATES-LON-01 ──┐                                             │
│  TRD-003 ─────┘                           │                                             │
│                                           ├───▶ EUR RATES        ──┐                    │
│  TRD-004 ─────┐                           │      LONDON DESK       │                    │
│  TRD-005 ─────┼──────▶ EUR-RATES-LON-02 ──┘                        │                    │
│  TRD-006 ─────┘                                                    ├───▶ RATES          │
│                                                                    │     TRADING        │
│  TRD-007 ─────┐                                                    │                    │
│  TRD-008 ─────┼──────▶ USD-RATES-NY-01 ───┐                        │                    │
│  TRD-009 ─────┘                           ├───▶ USD RATES    ──────┘                    │
│                                           │      NY DESK                                │
│  TRD-010 ─────┐                           │                                             │
│  TRD-011 ─────┼──────▶ USD-RATES-NY-02 ───┘                                             │
│                                                                                         │
│  At each aggregation level:                                                             │
│  Aggregated_P&L(parent, d) = Σ Aggregated_P&L(child, d)                                 │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Diversification Benefit

Note that VaR at a parent level is typically **less** than the sum of VaR of children:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     DIVERSIFICATION BENEFIT                                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  EXAMPLE: Two Books with Partially Offsetting Risks                                     │
│                                                                                         │
│  Book A (Long EUR rates):  P&L Strip = [-100k, +80k, -50k, +60k, -120k]                 │
│  Book B (Short EUR rates): P&L Strip = [+90k, -70k, +40k, -50k, +100k]                  │
│                                                                                         │
│  Desk (A + B):             P&L Strip = [-10k, +10k, -10k, +10k, -20k]                   │
│                                                                                         │
│  Individual Book VaRs:                                                                  │
│  • Book A VaR (99%): $120k (worst: -120k)                                               │
│  • Book B VaR (99%): $70k (worst: -70k)                                                 │
│  • Sum: $190k                                                                           │
│                                                                                         │
│  Aggregated Desk VaR:                                                                   │
│  • Desk VaR (99%): $20k (worst: -20k)                                                   │
│                                                                                         │
│  DIVERSIFICATION BENEFIT: $190k - $20k = $170k (89% reduction)                          │
│                                                                                         │
│  This is captured naturally by aggregating P&L strips before percentile calculation     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.4 Hierarchy ODS Integration

The Hierarchy ODS provides the book structure used for aggregation:

| Field | Description | Example |
|-------|-------------|---------|
| `position_id` | Unique position identifier | TRD-001 |
| `book_id` | Lowest hierarchy level | EUR-RATES-LON-01 |
| `desk_id` | Trading desk | EUR-RATES-LON |
| `business_unit_id` | Business unit | RATES-TRADING |
| `division_id` | Division | GLOBAL-MARKETS |
| `entity_id` | Legal entity | MERIDIAN-UK |
| `enterprise_id` | Group | MERIDIAN-GROUP |
| `effective_date` | As-of date | 2025-01-15 |

---

## 6. Step 3: Percentile Calculation

### 6.1 Concept

VaR is extracted from the aggregated P&L distribution as the **99th percentile loss** (or 1st percentile of P&L):

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     PERCENTILE CALCULATION CONCEPT                                       │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  For each hierarchy node:                                                                │
│                                                                                          │
│  1. Take the aggregated P&L strip: [-800k, -750k, +600k, -300k, ...]  (500+ values)      │
│  2. Sort in ascending order: [-800k, -750k, -450k, -300k, ..., +600k]                    │
│  3. Find 99th percentile loss = 1st percentile of sorted values                          │
│     With 500 observations: 99th percentile ≈ 5th worst observation                       │
│  4. VaR (99%, 1-day) = |5th worst observation|                                           │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                     │ │
│  │   Sorted P&L Distribution (500 observations):                                       │ │
│  │                                                                                     │ │
│  │   Position  |  Value      |  Notes                                                  │ │
│  │   ─────────────────────────────────────────────────────────────────────────────     │ │
│  │   1st       |  -$800k     |  Worst loss                                             │ │
│  │   2nd       |  -$750k     |                                                         │ │
│  │   3rd       |  -$680k     |                                                         │ │
│  │   4th       |  -$620k     |                                                         │ │
│  │   5th       |  -$580k     |  ← 99th PERCENTILE (5 out of 500 = 1%)                  │ │
│  │   6th       |  -$550k     |                                                         │ │
│  │   ...       |  ...        |                                                         │ │
│  │   250th     |  +$10k      |  Median                                                 │ │
│  │   ...       |  ...        |                                                         │ │
│  │   500th     |  +$650k     |  Best P&L                                               │ │
│  │                                                                                     │ │
│  │   VaR (99%, 1-day) = $580,000                                                       │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Scaling to 10-day VaR

For regulatory capital purposes, 1-day VaR must be converted to a 10-day horizon. Two approaches are available:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     10-DAY VaR CALCULATION METHODS                                       │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  METHOD 1: SQUARE ROOT OF TIME SCALING (Simpler)                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                          │
│  VaR(10-day) = VaR(1-day) × √10 ≈ VaR(1-day) × 3.162                                     │
│                                                                                          │
│  ASSUMPTIONS:                                                                            │
│  • Returns are independently and identically distributed (i.i.d.)                        │
│  • Volatility scales with square root of time                                            │
│  • No mean reversion or serial correlation in returns                                    │
│                                                                                          │
│  ADVANTAGES:                                                                             │
│  • Computationally simple and fast                                                       │
│  • Widely accepted by regulators                                                         │
│  • Consistent with standard Basel framework                                              │
│                                                                                          │
│  LIMITATIONS:                                                                            │
│  • Overstates risk if returns exhibit mean reversion                                     │
│  • Understates risk if returns exhibit autocorrelation (trending)                        │
│  • Does not capture liquidity horizon differences by asset class                         │
│                                                                                          │
│  ──────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                          │
│  METHOD 2: ACTUAL 10-DAY RETURNS FROM TIME SERIES (More Accurate)                        │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                          │
│  Calculate VaR using actual overlapping 10-day returns from historical time series:      │
│                                                                                          │
│  For each risk factor:                                                                   │
│  Return_10day(t) = Price(t) / Price(t-10) - 1                                            │
│                                                                                          │
│  Then apply these 10-day shocks directly in P&L strip calculation.                       │
│                                                                                          │
│  ADVANTAGES:                                                                             │
│  • Captures actual 10-day return dynamics (autocorrelation, mean reversion)              │
│  • More accurate for assets with non-standard return distributions                       │
│  • Aligns with FRTB liquidity horizon requirements                                       │
│  • Naturally incorporates historical volatility clustering                               │
│                                                                                          │
│  LIMITATIONS:                                                                            │
│  • Requires more historical data (500 × 10-day returns = longer lookback)                │
│  • More computationally intensive (separate time series)                                 │
│  • Overlapping returns create statistical complexity                                     │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  EXAMPLE: Comparison of Methods                                                     │ │
│  │                                                                                     │ │
│  │  EUR 10Y Swap Portfolio                                                             │ │
│  │                                                                                     │ │
│  │  VaR (99%, 1-day):                          $580k                                   │ │
│  │                                                                                     │ │
│  │  Method 1: VaR (10-day) = $580k × √10   =   $1,834k                                 │ │
│  │  Method 2: VaR (10-day) actual returns  =   $1,720k                                 │ │
│  │                                                                                     │ │
│  │  Difference: $114k (6.2% lower using actual returns)                                │ │
│  │  Reason: EUR rates exhibit slight mean reversion over 10-day periods                │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 6.2.1 Meridian Global Bank Approach

| VaR Metric | Method Used | Rationale |
|------------|-------------|-----------|
| **Regulatory IMA VaR** | √10 scaling | Regulatory acceptance; conservative |
| **Internal Risk Management** | Actual 10-day returns | More accurate; used for limit monitoring |
| **FRTB ES (future)** | Actual liquidity horizon returns | Required by regulation |

**Reconciliation**: Both methods are calculated daily. Material differences (>10%) are investigated and reported to RMA quarterly.

| Metric | Calculation | Example |
|--------|-------------|---------|
| VaR (99%, 1-day) | 99th percentile from 1-day distribution | $580k |
| VaR (99%, 10-day) - Scaled | VaR(1-day) × √10 | $1,834k |
| VaR (99%, 10-day) - Actual | 99th percentile from 10-day distribution | $1,720k |

### 6.3 Stressed VaR (SVaR)

SVaR uses the same methodology but with returns from a **stressed market period**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     STRESSED VaR (SVaR) CALCULATION                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  METHODOLOGY:                                                                           │
│  1. Identify stressed period: 250-day window with maximum VaR for current portfolio     │
│  2. Use returns from stressed period for P&L strip calculation                          │
│  3. Aggregate and calculate percentile as per standard VaR                              │
│                                                                                         │
│  STRESSED PERIOD SELECTION (Dynamic):                                                   │
│  • Review period candidates: 2008 GFC, 2010 Euro Crisis, 2020 COVID, 2022 Rate Shock    │
│  • Select period that produces highest VaR for current portfolio composition            │
│  • Review and update stressed period quarterly (or after significant portfolio change)  │
│                                                                                         │
│  CURRENT STRESSED PERIOD: 15-Sep-2008 to 15-Sep-2009 (Lehman/GFC)                       │
│                                                                                         │
│  EXAMPLE:                                                                               │
│  • VaR (normal period, 99%, 10-day):    $1,834k                                         │
│  • SVaR (stressed period, 99%, 10-day): $4,250k                                         │
│                                                                                         │
│  Note: SVaR is typically 2-3x VaR due to higher volatility in stressed period           │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.4 Incremental Risk Charge (IRC)

> **Note**: IRC calculation has been extracted to a standalone process due to its distinct methodology (Monte Carlo simulation) and regulatory requirements. See [IRC Calculation (MR-L4-010)](./irc-calculation.md) for full details.

IRC captures default and migration risk for credit positions in the trading book. Key characteristics:
- 99.9% confidence level, 1-year horizon
- Monte Carlo simulation of credit events (default and migration)
- Calculated weekly (separate from daily VaR/SVaR)
- Results aggregated with VaR and SVaR for IMA capital calculation

### 6.5 Risk Factor Contributions

The Risk Engine calculates contribution of each risk factor to total VaR:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     RISK FACTOR CONTRIBUTION ANALYSIS                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  METHODOLOGY: Component VaR / Marginal VaR                                              │
│                                                                                         │
│  For each risk factor i:                                                                │
│  Marginal_VaR(i) = VaR(portfolio) - VaR(portfolio excl. risk factor i)                  │
│                                                                                         │
│  Component_VaR(i) = weight(i) × marginal_VaR(i)                                         │
│                                                                                         │
│  EXAMPLE OUTPUT:                                                                        │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  Entity: Meridian Bank UK                                                          │ │
│  │  Total VaR: $8.5M                                                                  │ │
│  │                                                                                    │ │
│  │  Risk Factor             │ Component VaR │  % of Total │ Direction                 │ │
│  │  ─────────────────────────────────────────────────────────────────────────────     │ │
│  │  EUR Interest Rates      │    $3.2M      │    38%      │ ↑ Rates hurt              │ │
│  │  USD Interest Rates      │    $1.8M      │    21%      │ ↑ Rates hurt              │ │
│  │  EUR/USD FX              │    $1.5M      │    18%      │ ↓ EUR weaker hurts        │ │
│  │  Credit Spreads          │    $1.2M      │    14%      │ Wider spreads hurt        │ │
│  │  Equity                  │    $0.5M      │     6%      │ ↓ Equities hurt           │ │
│  │  Other                   │    $0.3M      │     3%      │ -                         │ │
│  │  ─────────────────────────────────────────────────────────────────────────────     │ │
│  │  TOTAL                   │    $8.5M      │   100%      │                           │ │
│  │                                                                                    │ │
│  │  Note: Components may not sum exactly due to diversification                       │ │
│  └────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.6 Concentration VaR Decomposition

In addition to risk factor contributions, the Risk Engine calculates VaR decompositions required for **concentration limit monitoring** (see MR-L5-005: Concentration Limits Controls). These decompositions attribute VaR to specific dimensions used for concentration analysis.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     CONCENTRATION VaR DECOMPOSITION                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  The Risk Engine produces VaR decompositions across multiple concentration dimensions:  │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │  DECOMPOSITION     │  METHODOLOGY         │  USE CASE                             │  │
│  ├────────────────────┼──────────────────────┼───────────────────────────────────────┤  │
│  │  BY ISSUER         │  Component VaR by    │  Single issuer concentration          │  │
│  │                    │  issuer_id           │  limit (15% of Trading Book VaR)      │  │
│  ├────────────────────┼──────────────────────┼───────────────────────────────────────┤  │
│  │  BY CURRENCY       │  Component VaR by    │  Single currency concentration        │  │
│  │                    │  currency_code       │  limit (30% of FX VaR)                │  │
│  ├────────────────────┼──────────────────────┼───────────────────────────────────────┤  │
│  │  BY CURVE          │  Component VaR by    │  Single curve concentration           │  │
│  │                    │  curve_id            │  limit (25% of IR VaR)                │  │
│  ├────────────────────┼──────────────────────┼───────────────────────────────────────┤  │
│  │  BY SECTOR         │  Component VaR by    │  Sector concentration                 │  │
│  │                    │  gics_sector         │  limit (25% of Credit VaR)            │  │
│  ├────────────────────┼──────────────────────┼───────────────────────────────────────┤  │
│  │  BY COUNTRY        │  Component VaR by    │  Country (EM) concentration           │  │
│  │                    │  country_code        │  limit (20% of EM VaR)                │  │
│  └────────────────────┴──────────────────────┴───────────────────────────────────────┘  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 6.6.1 Component VaR Calculation Method

For concentration monitoring, the Risk Engine uses the **Component VaR** method, which attributes portfolio VaR to individual positions or groupings:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     COMPONENT VaR METHODOLOGY                                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  FORMULA:                                                                               │
│                                                                                         │
│  Component_VaR(i) = ρ(i, Portfolio) × σ(i) × Position(i)                                │
│                     ─────────────────────────────────────── × Portfolio_VaR             │
│                                Portfolio_σ                                              │
│                                                                                         │
│  Where:                                                                                 │
│  • ρ(i, Portfolio) = Correlation of position i returns with portfolio returns           │
│  • σ(i) = Volatility of position i returns                                              │
│  • Position(i) = Market value of position i                                             │
│  • Portfolio_σ = Volatility of portfolio returns                                        │
│  • Portfolio_VaR = Total portfolio VaR                                                  │
│                                                                                         │
│  KEY PROPERTY:                                                                          │
│  Σ Component_VaR(i) = Portfolio_VaR  (sum to portfolio VaR)                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ALTERNATIVE: MARGINAL VaR METHOD (for ad-hoc analysis)                                 │
│                                                                                         │
│  Marginal_VaR(i) = VaR(Portfolio) - VaR(Portfolio excl. position i)                     │
│                                                                                         │
│  Note: Marginal VaR does NOT sum to portfolio VaR (captures diversification effect)     │
│  Used for: What-if analysis, position sizing decisions, trader incentive calculations   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 6.6.2 Issuer VaR Decomposition

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     ISSUER VaR DECOMPOSITION (Example Output)                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Entity: Meridian Bank UK                    As-of: 15-Jan-2025                         │
│  Total Trading Book VaR: $20.0M                                                         │
│                                                                                         │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  Rank │ Issuer              │ Component VaR │  % of TB VaR │ Limit │ Status        │ │
│  ├───────┼─────────────────────┼───────────────┼──────────────┼───────┼───────────────┤ │
│  │   1   │ UK Government       │    $2.4M      │    12.0%     │  15%  │ 🟡 Amber      │ │
│  │   2   │ Deutsche Bank AG    │    $2.0M      │    10.0%     │  15%  │ 🟢 Green      │ │
│  │   3   │ Vodafone Group      │    $1.8M      │     9.0%     │  15%  │ 🟢 Green      │ │
│  │   4   │ BP plc              │    $1.5M      │     7.5%     │  15%  │ 🟢 Green      │ │
│  │   5   │ HSBC Holdings       │    $1.4M      │     7.0%     │  15%  │ 🟢 Green      │ │
│  │   6   │ Shell plc           │    $1.3M      │     6.5%     │  15%  │ 🟢 Green      │ │
│  │   7   │ Barclays plc        │    $1.1M      │     5.5%     │  15%  │ 🟢 Green      │ │
│  │   8   │ GlaxoSmithKline     │    $1.0M      │     5.0%     │  15%  │ 🟢 Green      │ │
│  │   9   │ Rio Tinto           │    $0.9M      │     4.5%     │  15%  │ 🟢 Green      │ │
│  │  10   │ BT Group            │    $0.8M      │     4.0%     │  15%  │ 🟢 Green      │ │
│  │  ...  │ Other (500+ issuers)│    $5.8M      │    29.0%     │  N/A  │               │ │
│  ├───────┼─────────────────────┼───────────────┼──────────────┼───────┼───────────────┤ │
│  │ TOTAL │                     │   $20.0M      │   100.0%     │       │               │ │
│  └───────┴─────────────────────┴───────────────┴──────────────┴───────┴───────────────┘ │
│                                                                                         │
│  OUTPUT: Written to RISK_CONC_ISSUER table in Risk ODS                                  │
│  CONSUMER: Concentration Limits Controls (MR-L5-005), CN-C01                            │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 6.6.3 Currency and Curve VaR Decomposition

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     CURRENCY VaR DECOMPOSITION (Example)                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Total FX VaR: $5.0M                                                                    │
│                                                                                         │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  Currency │ Component VaR │  % of FX VaR │ Limit │ Status                          │ │
│  ├───────────┼───────────────┼──────────────┼───────┼─────────────────────────────────┤ │
│  │  USD      │    $1.4M      │    28.0%     │  30%  │ 🟡 Amber (approaching)          │ │
│  │  EUR      │    $1.25M     │    25.0%     │  30%  │ 🟡 Amber (approaching)          │ │
│  │  JPY      │    $0.75M     │    15.0%     │  30%  │ 🟢 Green                        │ │
│  │  GBP      │    $0.6M      │    12.0%     │  30%  │ 🟢 Green                        │ │
│  │  AUD      │    $0.4M      │     8.0%     │  30%  │ 🟢 Green                        │ │
│  │  Other    │    $0.6M      │    12.0%     │  N/A  │                                 │ │
│  └───────────┴───────────────┴──────────────┴───────┴─────────────────────────────────┘ │
│                                                                                         │
│  OUTPUT: Written to RISK_CONC_CURRENCY table in Risk ODS                                │
│  CONSUMER: Concentration Limits Controls (MR-L5-005), CN-C02                            │
│                                                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                     CURVE VaR DECOMPOSITION (Example)                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Total IR VaR: $12.0M                                                                   │
│                                                                                         │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  Curve        │ Component VaR │  % of IR VaR │ Limit │ Status                      │ │
│  ├───────────────┼───────────────┼──────────────┼───────┼─────────────────────────────┤ │
│  │  EUR-ESTER    │    $2.8M      │    23.3%     │  25%  │ 🟡 Amber (approaching)      │ │
│  │  USD-SOFR     │    $2.5M      │    20.8%     │  25%  │ 🟢 Green                    │ │
│  │  GBP-SONIA    │    $2.0M      │    16.7%     │  25%  │ 🟢 Green                    │ │
│  │  EUR-EURIBOR  │    $1.5M      │    12.5%     │  25%  │ 🟢 Green                    │ │
│  │  USD-GOVT     │    $1.2M      │    10.0%     │  25%  │ 🟢 Green                    │ │
│  │  Other        │    $2.0M      │    16.7%     │  N/A  │                             │ │
│  └───────────────┴───────────────┴──────────────┴───────┴─────────────────────────────┘ │
│                                                                                         │
│  OUTPUT: Written to RISK_CONC_CURVE table in Risk ODS                                   │
│  CONSUMER: Concentration Limits Controls (MR-L5-005), CN-C03                            │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 6.6.4 Sector and Country VaR Decomposition

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     SECTOR VaR DECOMPOSITION (Credit Book)                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Total Credit VaR: $8.0M                                                                │
│                                                                                         │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  GICS Sector               │ Component VaR │  % of Credit │ Limit │ Status         │ │
│  ├────────────────────────────┼───────────────┼──────────────┼───────┼────────────────┤ │
│  │  Financials                │    $1.8M      │    22.5%     │  25%  │ 🟡 Amber       │ │
│  │  Energy                    │    $1.4M      │    17.5%     │  25%  │ 🟢 Green       │ │
│  │  Industrials               │    $1.2M      │    15.0%     │  25%  │ 🟢 Green       │ │
│  │  Health Care               │    $1.0M      │    12.5%     │  25%  │ 🟢 Green       │ │
│  │  Consumer Discretionary    │    $0.9M      │    11.3%     │  25%  │ 🟢 Green       │ │
│  │  Information Technology    │    $0.7M      │     8.7%     │  25%  │ 🟢 Green       │ │
│  │  Other                     │    $1.0M      │    12.5%     │  N/A  │                │ │
│  └────────────────────────────┴───────────────┴──────────────┴───────┴────────────────┘ │
│                                                                                         │
│  OUTPUT: Written to RISK_CONC_SECTOR table in Risk ODS                                  │
│  CONSUMER: Concentration Limits Controls (MR-L5-005), CN-C05                            │
│                                                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                     COUNTRY VaR DECOMPOSITION (EM Exposures)                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Total EM VaR: $3.0M                                                                    │
│                                                                                         │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  Country       │ Component VaR │  % of EM VaR │ Limit │ Status                     │ │
│  ├────────────────┼───────────────┼──────────────┼───────┼────────────────────────────┤ │
│  │  Brazil        │    $0.55M     │    18.3%     │  20%  │ 🟡 Amber                   │ │
│  │  Mexico        │    $0.45M     │    15.0%     │  20%  │ 🟢 Green                   │ │
│  │  South Africa  │    $0.40M     │    13.3%     │  20%  │ 🟢 Green                   │ │
│  │  Indonesia     │    $0.35M     │    11.7%     │  20%  │ 🟢 Green                   │ │
│  │  India         │    $0.30M     │    10.0%     │  20%  │ 🟢 Green                   │ │
│  │  Other EM      │    $0.95M     │    31.7%     │  N/A  │                            │ │
│  └────────────────┴───────────────┴──────────────┴───────┴────────────────────────────┘ │
│                                                                                         │
│  OUTPUT: Written to RISK_CONC_COUNTRY table in Risk ODS                                 │
│  CONSUMER: Concentration Limits Controls (MR-L5-005), CN-C06                            │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 6.6.5 Concentration Output Tables

The following tables are written to the Risk ODS for concentration monitoring:

| Table Name | Description | Key Columns | Refresh |
|------------|-------------|-------------|---------|
| **RISK_CONC_ISSUER** | VaR by issuer | cob_date, entity_id, issuer_id, component_var, pct_of_total | Daily |
| **RISK_CONC_CURRENCY** | VaR by currency | cob_date, entity_id, currency_code, component_var, pct_of_fx_var | Daily |
| **RISK_CONC_CURVE** | VaR by IR curve | cob_date, entity_id, curve_id, component_var, pct_of_ir_var | Daily |
| **RISK_CONC_SECTOR** | VaR by GICS sector | cob_date, entity_id, gics_sector, component_var, pct_of_credit_var | Daily |
| **RISK_CONC_COUNTRY** | VaR by country (EM) | cob_date, entity_id, country_code, component_var, pct_of_em_var | Daily |
| **RISK_CONC_SUMMARY** | Summary with breach flags | cob_date, entity_id, dimension, top_concentration, breach_flag | Daily |

---

## 6.7 Economic Capital (ECAP) Calculation

In addition to regulatory VaR/SVaR, the Risk Engine calculates **Economic Capital (ECAP)** for internal management purposes. ECAP provides a more complete view of risk than regulatory capital by using different parameters aligned to the Bank's internal risk appetite.

### 6.7.1 ECAP vs Regulatory Capital

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     ECAP vs REGULATORY CAPITAL COMPARISON                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  Parameter           │ Economic Capital (ECAP) │ Regulatory Capital (IMA)          │ │
│  ├──────────────────────┼─────────────────────────┼───────────────────────────────────┤ │
│  │  Confidence Interval │ 99.9%                   │ 99%                               │ │
│  │  Purpose             │ Internal management     │ Regulatory compliance             │ │
│  │  Horizon             │ 10-25 days (by asset)   │ 10 days                           │ │
│  │  SVaR Treatment      │ Worst-of VaR/SVaR       │ VaR + SVaR (additive)             │ │
│  │  Multiplier          │ 1.0                     │ 3.0-4.0 (regulatory buffer)       │ │
│  │  Diversification     │ Full portfolio benefit  │ Per regulatory rules              │ │
│  │  Illiquidity Add-on  │ Yes (by asset class)    │ Partial (FRTB liquidity horizons) │ │
│  └──────────────────────┴─────────────────────────┴───────────────────────────────────┘ │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.7.2 ECAP Calculation Methodology

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     ECAP CALCULATION PROCESS                                             │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  STEP 1: CALCULATE BASE VaR AT 99.9% CONFIDENCE                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│  • Use same P&L strips from Step 1 (already calculated)                                  │
│  • Extract 99.9th percentile (instead of 99th)                                           │
│  • With 500 scenarios: 99.9% ≈ worst observation                                         │
│                                                                                          │
│  STEP 2: APPLY ASSET-CLASS SPECIFIC LIQUIDITY HORIZONS                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  Asset Class               │ Liquidity Horizon │ Scaling Factor │ Rationale         │ │
│  ├────────────────────────────┼───────────────────┼────────────────┼───────────────────┤ │
│  │  G10 FX Spot/Fwd           │ 10 days           │ √10 = 3.16     │ Highly liquid     │ │
│  │  Major Govt Bonds          │ 10 days           │ √10 = 3.16     │ Deep markets      │ │
│  │  Vanilla IR Swaps          │ 10 days           │ √10 = 3.16     │ Active IDB        │ │
│  │  IG Credit (liquid)        │ 15 days           │ √15 = 3.87     │ Moderate liquidity│ │
│  │  HY Credit / EM Debt       │ 20 days           │ √20 = 4.47     │ Lower liquidity   │ │
│  │  Equity Options            │ 15 days           │ √15 = 3.87     │ Exchange-traded   │ │
│  │  FX Options                │ 15 days           │ √15 = 3.87     │ OTC but liquid    │ │
│  │  Structured Products       │ 25 days           │ √25 = 5.00     │ Illiquid          │ │
│  │  Distressed Credit         │ 25 days           │ √25 = 5.00     │ Very illiquid     │ │
│  └────────────────────────────┴───────────────────┴────────────────┴───────────────────┘ │
│                                                                                          │
│  STEP 3: APPLY WORST-OF VaR/SVaR (NOT ADDITIVE)                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│  ECAP = Max(VaR_99.9_scaled, SVaR_99.9_scaled)                                           │
│                                                                                          │
│  (Regulatory uses: IMA Capital = 3×VaR + 3×SVaR - additive)                              │
│                                                                                          │
│  STEP 4: ADD ECAP-SPECIFIC COMPONENTS                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│  ECAP_Total = ECAP_Market + IRC + Concentration_Add-on + Illiquidity_Reserve             │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.7.3 ECAP Output and Sign-off

| Output | Description | Consumer |
|--------|-------------|----------|
| **ECAP by Entity** | Total economic capital by legal entity | ALCO, Board |
| **ECAP by Business** | Capital allocated to business units | Trading, Finance |
| **ECAP vs Regulatory** | Comparison and reconciliation | RMA, MLRC |
| **ECAP Utilisation** | ECAP usage vs. allocated capital | Capital Management |

**Daily Sign-off**: RAV signs off ECAP alongside VaR/SVaR as part of the morning Market Risk Report (see MR-L4-007).

### 6.7.4 ICAAP Contribution

ECAP feeds directly into the Bank's Internal Capital Adequacy Assessment Process (ICAAP):

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     ECAP → ICAAP FLOW                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  DAILY ECAP                  QUARTERLY ICAAP              ANNUAL SUBMISSION             │
│  (Risk Engine)               (Capital Planning)           (PRA)                         │
│                                                                                         │
│  ┌─────────────┐            ┌─────────────────┐          ┌─────────────────┐            │
│  │ Market Risk │───────────▶│ Pillar 2A       │─────────▶│ ICAAP Document  │            │
│  │ ECAP        │            │ Market Risk     │          │                 │            │
│  │             │            │ Capital Add-on  │          │ Submitted to    │            │
│  │ $85M        │            │                 │          │ PRA annually    │            │
│  └─────────────┘            │ Stressed ECAP   │          │                 │            │
│                             │ + Buffer        │          │ Reviewed in     │            │
│                             │ = $95M          │          │ SREP process    │            │
│                             └─────────────────┘          └─────────────────┘            │
│                                                                                         │
│  ECAP provides:                                                                         │
│  • Base case internal capital requirement                                               │
│  • Stressed capital (using ECAP under stress scenarios)                                 │
│  • Evidence of internal risk measurement capability                                     │
│  • Input to capital allocation and RAROC                                                │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

> **Regulatory Drivers**: For ECAP regulatory requirements (CRD VI, CRR, PRA SS13/13, BCBS Pillar 2), see [Market Risk Policy Section 8.6.1](../../L3-Governance/policies/market-risk-policy.md#861-ecap-regulatory-drivers).

---

## 6.8 Earnings at Risk (EaR) Calculation

In addition to ECAP, the Risk Engine calculates **Earnings at Risk (EaR)** for Risk Appetite monitoring. EaR provides a lower-confidence measure focused on earnings volatility rather than solvency.

### 6.8.1 EaR vs ECAP vs VaR

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     EaR vs ECAP vs VaR COMPARISON                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  Parameter           │ EaR                │ ECAP               │ VaR               │ │
│  ├──────────────────────┼────────────────────┼────────────────────┼───────────────────┤ │
│  │  Confidence Interval │ 90%                │ 99.9%              │ 99%               │ │
│  │  Horizon             │ 1 year (scaled)    │ 10-25 days (asset) │ 10 days           │ │
│  │  Interpretation      │ "1-in-10 year"     │ "1-in-1000 year"   │ "1-in-100 day"    │ │
│  │  Purpose             │ Earnings volatility│ Solvency/capital   │ Daily risk limits │ │
│  │  Consumer            │ Risk Appetite/RAS  │ ICAAP/Capital Mgmt │ Regulatory/IMA    │ │
│  │  Threshold Source    │ GOV-L3-010 (RAS)   │ Internal policy    │ MR-L3-003 (Limits)│ │
│  └──────────────────────┴────────────────────┴────────────────────┴───────────────────┘ │
│                                                                                         │
│  RELATIONSHIP:  VaR (10d, 99%) < EaR (1y, 90%) < ECAP (99.9%)                           │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.8.2 EaR Calculation Methodology

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     EaR CALCULATION PROCESS                                              │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  STEP 1: TAKE VaR (99%, 1-day) FROM STREAM 2 OUTPUT                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│  • Use VaR already calculated in Step 3 (Percentile Calculation)                         │
│  • Same P&L strips, same aggregation - just different confidence/horizon                 │
│                                                                                          │
│  STEP 2: APPLY CONFIDENCE LEVEL SCALING (99% → 90%)                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                          │
│  Scaling Factor = NORMSINV(0.90) / NORMSINV(0.99)                                        │
│                 = 1.282 / 2.326                                                          │
│                 = 0.551                                                                  │
│                                                                                          │
│  STEP 3: APPLY TIME HORIZON SCALING (1-day → 1-year)                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                          │
│  Time Scaling = √250 = 15.81                                                             │
│                                                                                          │
│  STEP 4: CALCULATE EaR                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                          │
│  EaR = VaR(1d, 99%) × Confidence Scaling × Time Scaling                                  │
│      = VaR(1d, 99%) × 0.551 × 15.81                                                      │
│      = VaR(1d, 99%) × 8.71                                                               │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  EXAMPLE CALCULATION                                                                │ │
│  │                                                                                     │ │
│  │  Entity VaR (1d, 99%):        $4.5m                                                 │ │
│  │  EaR Scaling Factor:          × 8.71                                                │ │
│  │  ─────────────────────────────────────                                              │ │
│  │  Entity EaR (1y, 90%):        $39.2m                                                │ │
│  │                                                                                     │ │
│  │  Risk Appetite (RAS L2):      $85m (Green threshold)                                │ │
│  │  Headroom:                    $45.8m (54% utilisation)                              │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.8.3 EaR Aggregation and Diversification

EaR is calculated at each hierarchy level using the same aggregation as VaR:

| Level | Aggregation Method | Diversification |
|-------|-------------------|-----------------|
| **Position → Book** | Direct sum of P&L strips | Captured in percentile |
| **Book → Desk** | Direct sum of P&L strips | Captured in percentile |
| **Desk → Business** | Direct sum of P&L strips | Captured in percentile |
| **Business → Entity** | Direct sum of P&L strips | Captured in percentile |
| **Entity → Group** | Sum with 40% correlation factor (per RAS) | Partial |

> **Note**: For Group-level EaR, a 40% correlation factor is applied across entities per the Risk Appetite Statement (GOV-L3-010) to reflect imperfect correlation of losses.

### 6.8.4 EaR Risk Appetite Thresholds

EaR is monitored against thresholds defined in the Risk Appetite Statement (GOV-L3-010):

| Level | Metric | Green | Amber | Red |
|-------|--------|-------|-------|-----|
| **Level 1 (Entity)** | Total EaR | < $175m | $175m - $195m | > $195m |
| **Level 2 (Market Risk)** | Market Risk EaR | < $85m | $85m - $95m | > $95m |

Breach escalation follows the Risk Appetite Framework (GOV-L3-011):
- **Amber**: Management action plan within 5 business days
- **Red**: Immediate escalation to CRO and remediation within 24 hours

### 6.8.5 EaR Output and Sign-off

| Output | Description | Consumer |
|--------|-------------|----------|
| **EaR by Entity** | Total EaR by legal entity | ExCo, ALCO, BRMC |
| **EaR by Business** | EaR allocated to business units | Trading, Risk Management |
| **EaR vs Risk Appetite** | RAG status against RAS thresholds | RMC, BRMC (via Dashboard) |
| **EaR Trend** | 30-day rolling EaR trend | Risk Management |

**Daily Sign-off**: RAV signs off EaR alongside VaR/SVaR/ECAP as part of the morning Market Risk Report (see MR-L4-007).

> **Risk Appetite Linkage**: For EaR threshold definitions and breach escalation procedures, see [Risk Appetite Statement (GOV-L3-010)](../../L3-Governance/risk-appetite-statement.md) and [Risk Appetite Framework (GOV-L3-011)](../../L3-Governance/risk-appetite-framework.md).

---

## 7. System Architecture

### 7.1 Risk Engine Components

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     RISK ENGINE ARCHITECTURE                                             │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                            RISK ENGINE (SYS-MR-003)                                 │ │
│  │                                                                                     │ │
│  │  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐                │ │
│  │  │  INPUT MANAGER    │  │  CALCULATION      │  │  OUTPUT MANAGER   │                │ │
│  │  │                   │  │  ORCHESTRATOR     │  │                   │                │ │
│  │  │  • Load positions │  │                   │  │  • Write to       │                │ │
│  │  │  • Load time      │  │  • Schedule jobs  │  │    Risk ODS       │                │ │
│  │  │    series         │  │  • Parallel       │  │  • Generate       │                │ │
│  │  │  • Load hierarchy │  │    execution      │  │    reports        │                │ │
│  │  │  • Validate       │  │  • Monitor        │  │  • Publish        │                │ │
│  │  │    inputs         │  │    progress       │  │    alerts         │                │ │
│  │  └─────────┬─────────┘  └─────────┬─────────┘  └─────────┬─────────┘                │ │
│  │            │                      │                      │                          │ │
│  │            └──────────────────────┼──────────────────────┘                          │ │
│  │                                   │                                                 │ │
│  │  ┌────────────────────────────────┴────────────────────────────────────────────┐    │ │
│  │  │                        CALCULATION GRID                                     │    │ │
│  │  │                                                                             │    │ │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │    │ │
│  │  │  │ P&L Strip   │  │ P&L Strip   │  │ P&L Strip   │  │ P&L Strip   │         │    │ │
│  │  │  │ Calculator  │  │ Calculator  │  │ Calculator  │  │ Calculator  │         │    │ │
│  │  │  │ (Node 1)    │  │ (Node 2)    │  │ (Node 3)    │  │ (Node N)    │         │    │ │
│  │  │  │             │  │             │  │             │  │             │         │    │ │
│  │  │  │ Desk A      │  │ Desk B      │  │ Desk C      │  │ Desk N      │         │    │ │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘         │    │ │
│  │  │                                                                             │    │ │
│  │  │  PARALLEL PROCESSING: Each desk calculated on separate compute node         │    │ │
│  │  └─────────────────────────────────────────────────────────────────────────────┘    │ │
│  │                                                                                     │ │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐    │ │
│  │  │                        AGGREGATION ENGINE                                   │    │ │
│  │  │                                                                             │    │ │
│  │  │  • Collects P&L strips from calculation nodes                               │    │ │
│  │  │  • Performs hierarchy aggregation (Step 2)                                  │    │ │
│  │  │  • Calculates percentiles (Step 3)                                          │    │ │
│  │  │  • Runs in sequence after all P&L strips complete                           │    │ │
│  │  └─────────────────────────────────────────────────────────────────────────────┘    │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Data Stores

| ODS | Role in Risk Engine | Data Volume |
|-----|---------------------|-------------|
| **Valuations ODS** | Input: MTM, sensitivities | ~50,000 positions/day |
| **Time Series ODS** | Input: Historical returns | ~5,000 risk factors × 500 days |
| **Hierarchy ODS** | Input: Book structure | ~50,000 positions mapped |
| **Risk ODS** | Output: VaR, P&L strips | ~50 desks × 500 scenarios |

### 7.3 Performance Requirements

| Metric | Target | Current Capacity |
|--------|--------|------------------|
| P&L Strip calculation | 2 hours | 50,000 positions × 500 scenarios |
| Aggregation | 1 hour | 6 hierarchy levels × 500 scenarios |
| Percentile calculation | 30 minutes | All hierarchy nodes |
| **Total batch time** | **5 hours** | 22:00 GMT - 03:00 GMT+1 |
| Grid nodes | 50 | Scalable to 100 |

---

## 8. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| REC-C01 | All inputs validated before calculation starts | Preventive | Risk Engine Ops |
| REC-C02 | P&L strips calculated for all positions in scope | Detective | Risk Engine Ops |
| REC-C03 | Hierarchy aggregation uses valid COB structure | Preventive | Risk Engine Ops |
| REC-C04 | VaR calculated for all desks in hierarchy | Detective | Risk Engine Ops |
| REC-C05 | VaR spike >50% vs. T-1 flagged for investigation | Detective | RAV |
| REC-C06 | Calculation errors logged and investigated | Detective | Risk Engine Ops |
| REC-C07 | Batch completion by SLA (04:00 GMT+1) monitored | Detective | Risk Engine Ops |
| REC-C08 | Aggregation integrity: Children VaR > Parent VaR (diversification) | Detective | RAV |
| REC-C09 | SVaR uses approved stressed period | Preventive | RMA |

---

## 9. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| Input validation complete | 22:15 GMT | 22:30 GMT | Risk Engine Ops Manager |
| P&L strip calculation complete | 01:00 GMT+1 | 01:30 GMT+1 | Risk Engine Ops Manager |
| Aggregation complete | 02:30 GMT+1 | 03:00 GMT+1 | Risk Engine Ops Manager |
| VaR calculation complete | 03:30 GMT+1 | 04:00 GMT+1 | Head of Market Risk Analytics |
| **Full batch complete** | **04:00 GMT+1** | **04:30 GMT+1** | **Head of Market Risk Analytics** |
| Calculation success rate | 100% | 99% | Risk Engine Ops Manager |
| Average batch duration | 5 hours | 6 hours | Risk Engine Ops |

---

## 10. Exception Handling

### 10.1 Calculation Failures

| Failure Type | Cause | Resolution | Escalation |
|--------------|-------|------------|------------|
| **Position valuation error** | Missing market data; model error | Exclude position; flag for investigation | Risk Engine Ops → Quants |
| **Risk factor missing** | Time series gap; unmapped factor | Apply proxy; flag in report | Risk Engine Ops → RAV |
| **Aggregation error** | Hierarchy inconsistency | Fix hierarchy; re-run | Risk Engine Ops → Data Ops |
| **Grid node failure** | Infrastructure issue | Re-assign to other node | Risk Engine Ops → IT |
| **Full batch failure** | Systemic issue | BCP procedures | Head of MR Analytics → CRO |

### 10.2 Partial Run Authority

| Scenario | Authority | Conditions | Notification |
|----------|-----------|------------|--------------|
| Single desk excluded | Risk Engine Ops Manager | <5% of firm VaR | Market Risk |
| Multiple desks excluded | Head of MR Analytics | <15% of firm VaR | MLRC |
| Major exclusion | MLRC approval | >15% of firm VaR | CRO, Board Risk Committee |

---

## 11. Monitoring and Reporting

### 11.1 Real-Time Monitoring

| Dashboard | Content | Audience |
|-----------|---------|----------|
| **Batch Progress** | Job status, completion %, ETA | Risk Engine Ops |
| **Error Log** | Calculation failures, warnings | Risk Engine Ops, Quants |
| **Performance Metrics** | Processing time, grid utilisation | Risk Engine Ops, IT |

### 11.2 Post-Calculation Validation

| Check | Description | Threshold | Action |
|-------|-------------|-----------|--------|
| VaR completeness | VaR calculated for all desks | 100% | Investigate missing |
| VaR vs. T-1 | Day-on-day change | ±50% | Flag for RAV review |
| Diversification check | Entity VaR < Σ(Desk VaR) | Must hold | Investigate if not |
| SVaR vs. VaR ratio | SVaR typically 2-3x VaR | 1.5x - 4x | Flag outliers |

---

## 12. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [Hierarchy Management](./hierarchy-management.md) | Upstream - provides hierarchy and trading book scope (Finance-owned) |
| [Time Series Management](./time-series-management/time-series-overview.md) | Upstream - provides time series |
| [EOD Market Data Snapshot](./eod-market-data-snapshot.md) | Upstream - provides EOD prices |
| [VaR Backtesting](./backtesting.md) | Downstream - validates VaR model accuracy |
| [Market Risk Reporting and Sign-off](./market-risk-reporting-signoff.md) | Downstream - uses VaR output |
| [IRC Calculation](./irc-calculation.md) | Related - IRC process for credit positions |
| [VaR Limit Framework](../L3-Governance/policies/var-limit-framework.md) | Governance - limit structure |
| [Historical Simulation VaR Model](../L6-Models/var-methodology.md) | Methodology reference |

---

## 13. Document Control

### 13.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |
| 1.1 | 2025-01-15 | Added Section 7: Price Source Alignment and Backtesting Implications | MLRC |
| 1.2 | 2025-01-15 | Enhanced Section 6.2: Two methods for 10-day VaR calculation (sqrt scaling and actual 10-day returns) | MLRC |
| 1.3 | 2025-01-15 | Extracted Hierarchy Management to standalone Finance-owned process (FIN-L4-001) | MLRC |
| 1.4 | 2025-01-15 | Extracted Price Source Alignment and Backtesting content to standalone Backtesting process (MR-L4-008) | MLRC |
| 1.5 | 2025-01-15 | Added Section 6.6: Concentration VaR Decomposition - Component VaR outputs by issuer, currency, curve, sector, and country for concentration limit monitoring (MR-L5-005) | MLRC |
| 1.6 | 2025-01-16 | Extracted IRC to standalone process (MR-L4-010); updated Section 6.4 with cross-reference | MLRC |
| 1.7 | 2025-01-16 | Added Section 1A: Three Parallel Calculation Streams - comprehensive architecture showing Sensitivities/VaR/Stress as unified platform with common inputs; enhanced Purpose section to emphasize Risk Engine as central calculation platform | MLRC |
| 1.8 | 2025-01-16 | Added Section 6.7: Economic Capital (ECAP) Calculation - methodology, asset-class liquidity horizons, ICAAP contribution, regulatory drivers | MLRC |
| 1.9 | 2025-01-17 | Added Section 6.8: Earnings at Risk (EaR) Calculation - methodology, Risk Appetite thresholds, aggregation; updated Stream 2 to include EaR; added Risk Appetite linkages (GOV-L3-010/011) | MLRC |

---

*End of Document*
