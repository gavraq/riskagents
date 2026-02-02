---
# Model Metadata
model_id: MR-L6-002
model_name: Economic Capital (ECAP) and Earnings at Risk (EaR) Methodology
version: 1.1
effective_date: 2025-01-17
next_review_date: 2026-01-17
owner: Head of Risk Methodology and Analytics (RMA)
approving_committee: Model Risk Committee / MLRC
model_tier: Tier 1 (Pillar 2 Capital / Risk Appetite)

# Taxonomy Linkages
parent_framework: MR-L3-001  # Market Risk Policy
parent_model: MR-L6-001  # Historical Simulation VaR/SVaR (base methodology)
risk_appetite: GOV-L3-010  # Risk Appetite Statement (EaR/ECAP limits)
l1_requirements:
  - REQ-L1-001  # CRR/CRR III
  - REQ-L1-006  # CRD VI
  - REQ-L1-007  # PRA SS13/13
  - REQ-L1-008  # BCBS Pillar 2
l2_risk_types:
  - MR-L2-001   # Market Risk
  - MR-L2-008   # Illiquidity Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy (Section 8.6)
  - GOV-L3-010  # Risk Appetite Statement
  - GOV-L3-011  # Risk Appetite Framework
l4_processes:
  - MR-L4-006   # Risk Engine Calculation (Section 6.7)
  - MR-L4-007   # Market Risk Reporting & Sign-off
  - MR-L4-014   # Aged Inventory Monitoring
l5_controls:
  - MR-L5-007   # ECAP and EaR Controls
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-010  # Time Series ODS
  - SYS-MR-008  # Risk ODS
---

# Economic Capital (ECAP) and Earnings at Risk (EaR) Methodology

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Model ID** | MR-L6-002 |
| **Version** | 1.1 |
| **Effective Date** | 17 January 2025 |
| **Parent Model** | Historical Simulation VaR/SVaR (MR-L6-001) |
| **Owner** | Head of Risk Methodology and Analytics (RMA) |
| **Model Tier** | Tier 1 (Pillar 2 Capital / Risk Appetite) |

---

## 1. Executive Summary

### 1.1 Purpose

This document defines the methodology for calculating **Economic Capital (ECAP)** and **Earnings at Risk (EaR)** for Market Risk at Meridian Global Bank. Both measures extend the regulatory VaR/SVaR methodology (MR-L6-001) to provide internal risk measures that:

- **EaR**: Measures potential earnings volatility at 90% confidence (1-in-10 year loss)
- **ECAP**: Captures solvency risk at 99.9% confidence (1-in-1000 year loss)
- Incorporate asset-specific liquidity horizons (ECAP only)
- Provide input to ICAAP, Pillar 2 capital requirements, and Risk Appetite monitoring
- Support internal capital allocation and performance measurement

### 1.2 EaR vs ECAP: Two Perspectives on the Same Risk

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        EaR vs ECAP: RISK APPETITE HIERARCHY                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  SAME UNDERLYING METHODOLOGY (Historical Simulation VaR)                                │
│  DIFFERENT CONFIDENCE LEVELS FOR DIFFERENT PURPOSES                                     │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                                                                                 │    │
│  │  REGULATORY VaR/SVaR            EaR                        ECAP                 │    │
│  │  (Day-to-day Limit)        (Earnings Volatility)      (Capital Adequacy)        │    │
│  │                                                                                 │    │
│  │  ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐        │    │
│  │  │                 │       │                 │       │                 │        │    │
│  │  │   99% / 10-day  │   →   │   90% / 1-year  │   →   │  99.9% / 1-year │        │    │
│  │  │                 │       │                 │       │  + Liquidity    │        │    │
│  │  │   Position      │       │   Earnings      │       │                 │        │    │
│  │  │   Limits        │       │   Budgeting     │       │   Solvency      │        │    │
│  │  │                 │       │                 │       │                 │        │    │
│  │  └─────────────────┘       └─────────────────┘       └─────────────────┘        │    │
│  │           │                         │                         │                 │    │
│  │           ▼                         ▼                         ▼                 │    │
│  │       MLRC/Desk              ExCo/ALCO/BRMC             Board/ICAAP             │    │
│  │                                                                                 │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  RELATIONSHIP:  VaR < EaR < ECAP (by construction of confidence levels)                 │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

| Measure | Confidence | Horizon | Purpose | Governance |
|---------|------------|---------|---------|------------|
| **VaR/SVaR** | 99% | 10-day | Regulatory capital; desk limits | MLRC |
| **EaR** | 90% | 1-year | Earnings volatility; risk appetite | ExCo, ALCO, BRMC |
| **ECAP** | 99.9% | 1-year (liquidity-adjusted) | Capital adequacy; ICAAP | Board, PRA |

### 1.3 Relationship to Regulatory VaR/SVaR

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  EaR AND ECAP: EXTENSIONS OF REGULATORY VaR/SVaR                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                  HISTORICAL SIMULATION MODEL (MR-L6-001)                        │    │
│  │                                                                                 │    │
│  │  • Full revaluation / sensitivity-based calculation                             │    │
│  │  • 500-day observation window (VaR) / 250-day stressed period (SVaR)            │    │
│  │  • Absolute/relative returns by risk factor type                                │    │
│  │  • Hierarchy aggregation with diversification benefit                           │    │
│  │                                                                                 │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                              │                    │                    │              │
│                              │                    │                    │              │
│                              ▼                    ▼                    ▼              │
│        ┌──────────────────────────┐  ┌──────────────────────────┐  ┌──────────────────────────┐
│        │   REGULATORY VaR/SVaR    │  │  EARNINGS AT RISK (EaR)  │  │  ECONOMIC CAPITAL (ECAP) │
│        │                          │  │                          │  │                          │
│        │  Confidence: 99%         │  │  Confidence: 90%         │  │  Confidence: 99.9%       │
│        │  Horizon: 10-day         │  │  Horizon: 1-year         │  │  Horizon: 1-year (liq.)  │
│        │  Purpose: Pillar 1       │  │  Purpose: Risk Appetite  │  │  Purpose: Pillar 2/ICAAP │
│        │  Basis: VaR OR SVaR      │  │  Basis: Worst-of VaR/SVaR│  │  Basis: Worst-of VaR/SVaR│
│        │                          │  │                          │  │                          │
│        │  MODEL: MR-L6-001        │  │  MODEL: MR-L6-002        │  │  MODEL: MR-L6-002        │
│        └──────────────────────────┘  └──────────────────────────┘  └──────────────────────────┘
│                                                                                         │
│  KEY PRINCIPLE: EaR and ECAP build on the same Historical Simulation model              │
│  but apply different confidence scalings for earnings vs capital purposes               │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.4 Key Model Parameters

| Parameter | Regulatory VaR/SVaR | EaR | ECAP |
|-----------|---------------------|-----|------|
| **Confidence Level** | 99% | 90% | 99.9% |
| **Holding Period** | 10 days (uniform) | 1 year | 1 year (liquidity-adjusted) |
| **Observation Window** | 500 days / Stressed | Worst-of VaR/SVaR | Worst-of VaR/SVaR |
| **Purpose** | Pillar 1 regulatory capital | Risk Appetite (earnings) | Pillar 2 / ICAAP |
| **Frequency** | Daily | Daily / Monthly | Daily (reported quarterly) |
| **Governance** | MLRC | ExCo, ALCO, BRMC | MLRC → ALCO → Board |
| **Liquidity Adjustment** | No | No | Yes (10-25 days by asset) |
| **RAS Linkage** | N/A | Level 1 & 2 metrics | Level 1 metric (AFR/ECAP ratio) |

---

## 2. Regulatory Context

### 2.1 Applicable Regulations

| Regulation | Requirement | ECAP Implementation |
|------------|-------------|---------------------|
| **CRD VI Article 73** | Internal capital for all material risks | ECAP covers market risk capital |
| **CRR III Article 325** | Pillar 1 market risk capital | ECAP extends Pillar 1 methodology |
| **PRA SS13/13** | Pillar 2A market risk guidance | ECAP methodology follows PRA expectations |
| **BCBS Pillar 2** | ICAAP requirements | ECAP feeds into annual ICAAP |

### 2.2 Pillar 1 vs Pillar 2 Capital

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        PILLAR 1 vs PILLAR 2 CAPITAL                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  PILLAR 1 (Regulatory Minimum)                                                          │
│  ─────────────────────────────                                                          │
│  Capital = max(VaR_t-1, mc × VaR_avg) + max(SVaR_t-1, ms × SVaR_avg) + IRC              │
│                                                                                         │
│  • Prescribed formula (CRR Article 325)                                                 │
│  • 99% confidence, 10-day horizon                                                       │
│  • Same methodology for all banks                                                       │
│  • Minimum capital requirement                                                          │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  PILLAR 2 (Internal Assessment - ECAP)                                                  │
│  ─────────────────────────────────────                                                  │
│  ECAP = f(VaR/SVaR at 99.9%, liquidity-adjusted horizons, aged inventory add-on)        │
│                                                                                         │
│  • Bank-specific methodology (subject to PRA review)                                    │
│  • Higher confidence level (99.9%)                                                      │
│  • Asset-specific liquidity horizons                                                    │
│  • Captures risks not in Pillar 1 (illiquidity, concentration)                          │
│  • Feeds into ICAAP and Total Capital Requirement                                       │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  TOTAL CAPITAL REQUIREMENT                                                              │
│  ─────────────────────────                                                              │
│  TCR = Pillar 1 + Pillar 2A + Pillar 2B + Buffers                                       │
│                                                                                         │
│  Where Pillar 2A includes:                                                              │
│  • ECAP above Pillar 1 (if ECAP > Pillar 1)                                             │
│  • Additional risks not captured in Pillar 1                                            │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Earnings at Risk (EaR) Calculation Methodology

### 3.1 EaR Purpose and Role in Risk Appetite

Earnings at Risk (EaR) measures the potential loss to earnings over a one-year horizon at a 90% confidence level - i.e., a "1-in-10 year" loss. EaR serves as the primary metric for:

- **Risk Appetite Monitoring**: Level 1 and Level 2 Risk Appetite Statement thresholds
- **Earnings Budget**: Input to annual earnings volatility budgeting
- **Performance Measurement**: Risk-adjusted performance attribution
- **Capital Planning**: Link between trading risk and earnings impact

### 3.2 EaR Calculation Formula

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        EaR CALCULATION                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  FORMULA:                                                                               │
│                                                                                         │
│  EaR = VaR(1d, 99%) × (NORMSINV(0.90) / NORMSINV(0.99)) × √250                         │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  COMPONENTS:                                                                            │
│                                                                                         │
│  1. VaR(1d, 99%)              Base 1-day 99% VaR from Historical Simulation            │
│                                (Uses worst-of VaR/SVaR for conservatism)               │
│                                                                                         │
│  2. NORMSINV(0.90)            Standard normal inverse at 90% = 1.282                   │
│     NORMSINV(0.99)            Standard normal inverse at 99% = 2.326                   │
│     Ratio                     1.282 / 2.326 = 0.551                                    │
│                                                                                         │
│  3. √250                      Scaling from 1-day to 1-year (250 trading days)          │
│                               √250 = 15.81                                              │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  COMBINED SCALING FACTOR:                                                               │
│                                                                                         │
│  EaR = VaR(1d, 99%) × 0.551 × 15.81                                                    │
│      = VaR(1d, 99%) × 8.71                                                             │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  EXAMPLE:                                                                               │
│                                                                                         │
│  Entity VaR(1d, 99%) = $1.5M                                                           │
│  EaR = $1.5M × 8.71 = $13.1M (per trading day)                                         │
│                                                                                         │
│  With worst-of VaR/SVaR:                                                                │
│  VaR(1d, 99%) = $1.5M                                                                  │
│  SVaR(1d, 99%) = $2.2M                                                                 │
│  max(VaR, SVaR) = $2.2M                                                                │
│  EaR = $2.2M × 8.71 = $19.2M                                                           │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 EaR vs ECAP Scaling Comparison

| Measure | Confidence Scaling | Time Scaling | Combined Factor | From VaR(1d,99%) |
|---------|-------------------|--------------|-----------------|------------------|
| **VaR (10d, 99%)** | None | √10 = 3.16 | 3.16 | VaR × 3.16 |
| **EaR (1yr, 90%)** | 0.551 (90%/99%) | √250 = 15.81 | 8.71 | VaR × 8.71 |
| **ECAP (1yr, 99.9%)** | 1.33 (99.9%/99%) | √250 = 15.81 | 21.0 | VaR × 21.0 × Liq |

**Interpretation**: For the same underlying VaR:
- EaR ≈ 2.8x regulatory VaR (10-day)
- ECAP ≈ 6.6x regulatory VaR (10-day) before liquidity adjustment
- Relationship: VaR(10d) < EaR < ECAP

### 3.4 EaR Risk Appetite Thresholds

From the Risk Appetite Statement (GOV-L3-010):

| Level | EaR Metric | Green | Amber | Red | Owner |
|-------|------------|-------|-------|-----|-------|
| **Level 1** | Entity EaR | < $175m | $175m - $195m | > $195m | CRO |
| **Level 2** | Market Risk EaR (undiversified) | < $85m | $85m - $95m | > $95m | Head of Market Risk |

### 3.5 EaR Aggregation and Diversification

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        EaR AGGREGATION                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  LEVEL 2 (RISK TYPE) AGGREGATION:                                                       │
│                                                                                         │
│  At Level 2, EaR is reported UNDIVERSIFIED by risk type:                                │
│                                                                                         │
│  │ Risk Type       │ Undiversified EaR │ Correlation │ Diversified EaR │               │
│  ├─────────────────┼───────────────────┼─────────────┼─────────────────┤               │
│  │ Credit Risk     │ $95m              │ 40%         │ $38m            │               │
│  │ Market Risk     │ $85m              │ 40%         │ $34m            │               │
│  │ Operational Risk│ $50m              │ 40%         │ $20m            │               │
│  │ IRRBB           │ $40m              │ 40%         │ $16m            │               │
│  │ Business Risk   │ $75m              │ 40%         │ $30m            │               │
│  ├─────────────────┼───────────────────┼─────────────┼─────────────────┤               │
│  │ TOTAL UNDIV.    │ $345m             │ -           │ -               │               │
│  │ Diversification │ -                 │ -           │ ($107m)         │               │
│  │ TOTAL DIVERSIF. │ -                 │ -           │ $175m           │               │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  LEVEL 1 (ENTITY) AGGREGATION:                                                          │
│                                                                                         │
│  At Level 1, EaR is reported DIVERSIFIED across all risk types:                         │
│                                                                                         │
│  Diversified EaR = √(Σ EaR_i² + 2 × Σ ρ × EaR_i × EaR_j)                               │
│                                                                                         │
│  Where ρ = 40% correlation factor between risk types                                    │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  MARKET RISK EaR BREAKDOWN (LEVEL 3):                                                   │
│                                                                                         │
│  Within Market Risk, EaR can be decomposed by desk/asset class:                         │
│                                                                                         │
│  │ Portfolio       │ VaR (1d, 99%)  │ EaR Scaling │ EaR            │                    │
│  ├─────────────────┼────────────────┼─────────────┼────────────────┤                    │
│  │ Rates Trading   │ $0.8m          │ × 8.71      │ $7.0m          │                    │
│  │ FX Trading      │ $0.5m          │ × 8.71      │ $4.4m          │                    │
│  │ Credit Trading  │ $0.4m          │ × 8.71      │ $3.5m          │                    │
│  │ Equities        │ $0.3m          │ × 8.71      │ $2.6m          │                    │
│  │ Commodities     │ $0.2m          │ × 8.71      │ $1.7m          │                    │
│  ├─────────────────┼────────────────┼─────────────┼────────────────┤                    │
│  │ Entity Total    │ $1.5m          │ × 8.71      │ $13.1m         │                    │
│                                                                                         │
│  Note: Diversification benefit captured in entity VaR per MR-L6-001                     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.6 EaR Reporting and Governance

| Report | Frequency | Recipients | Content |
|--------|-----------|------------|---------|
| **Entity EaR Dashboard** | Daily | CRO, CFO, Business Heads | Level 1 EaR vs appetite |
| **Risk Type EaR** | Monthly | RMC, ALCO, ExCo | Level 2 breakdown |
| **EaR Trend Report** | Monthly | BRMC | Trend analysis, drivers |
| **ICAAP EaR Section** | Quarterly | Board, PRA | Earnings volatility assessment |

### 3.7 EaR Usage in Capital Planning

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        EaR IN CAPITAL AND EARNINGS PLANNING                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ANNUAL BUDGET CYCLE:                                                                   │
│                                                                                         │
│  1. Business submits revenue targets                                                    │
│  2. Risk calculates implied EaR for proposed positions                                  │
│  3. ALCO reviews EaR vs risk appetite allocation                                        │
│  4. Iterative process until EaR fits within appetite                                    │
│  5. Board approves budget with embedded risk appetite                                   │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  ONGOING MONITORING:                                                                    │
│                                                                                         │
│  │ EaR Status  │ Action Required                        │ Escalation     │             │
│  ├─────────────┼────────────────────────────────────────┼────────────────┤             │
│  │ GREEN       │ Continue BAU monitoring                │ None           │             │
│  │ AMBER       │ Management action plan within 5 days   │ RMC            │             │
│  │ RED         │ Immediate risk reduction required      │ ExCo → Board   │             │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  PERFORMANCE MEASUREMENT:                                                               │
│                                                                                         │
│  Risk-Adjusted Return = Actual P&L / Allocated EaR                                      │
│                                                                                         │
│  Used for:                                                                              │
│  • Desk performance comparison                                                          │
│  • Capital allocation decisions                                                         │
│  • Compensation benchmarking                                                            │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. ECAP Calculation Methodology

### 4.1 Calculation Overview

ECAP calculation extends the base Historical Simulation methodology (MR-L6-001) through five key transformations (confidence scaling, liquidity horizon adjustment, worst-of treatment, aggregation, and illiquidity add-on):

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        ECAP CALCULATION FLOW                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  STEP 1: BASE VaR/SVaR CALCULATION (per MR-L6-001)                                      │
│  ─────────────────────────────────────────────────                                      │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Historical Simulation Engine                                                   │    │
│  │  • Generate 500 P&L scenarios (VaR) / 250 scenarios (SVaR)                      │    │
│  │  • Apply shocks to current portfolio                                            │    │
│  │  • Aggregate through hierarchy                                                  │    │
│  │  • Calculate 99th percentile                                                    │    │
│  │  • Output: VaR(99%, 1-day), SVaR(99%, 1-day)                                    │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                              │                                                          │
│                              ▼                                                          │
│  STEP 2: CONFIDENCE LEVEL SCALING (99% → 99.9%)                                         │
│  ───────────────────────────────────────────────                                        │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Two approaches available:                                                      │    │
│  │                                                                                 │    │
│  │  APPROACH A: Empirical (Preferred)                                              │    │
│  │  • Use actual 99.9th percentile from P&L distribution                           │    │
│  │  • VaR: 1st worst of 500 (or average of 1st and 2nd worst)                      │    │
│  │  • SVaR: 1st worst of 250                                                       │    │
│  │                                                                                 │    │
│  │  APPROACH B: Parametric Scaling (Fallback)                                      │    │
│  │  • VaR(99.9%) ≈ VaR(99%) × 1.40                                                 │    │
│  │  • Based on normal distribution: z(99.9%)/z(99%) = 3.09/2.33 = 1.33             │    │
│  │  • Conservative adjustment: 1.40 (accounts for fat tails)                       │    │
│  │                                                                                 │    │
│  │  Output: VaR(99.9%, 1-day), SVaR(99.9%, 1-day)                                  │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                              │                                                          │
│                              ▼                                                          │
│  STEP 3: LIQUIDITY HORIZON SCALING                                                      │
│  ─────────────────────────────────                                                      │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Apply asset-class specific liquidity horizons:                                 │    │
│  │                                                                                 │    │
│  │  VaR(99.9%, T-day) = VaR(99.9%, 1-day) × √T                                     │    │
│  │                                                                                 │    │
│  │  Where T = liquidity horizon for each asset class                               │    │
│  │                                                                                 │    │
│  │  Output: Liquidity-adjusted VaR and SVaR by asset class                         │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                              │                                                          │
│                              ▼                                                          │
│  STEP 4: WORST-OF TREATMENT                                                             │
│  ──────────────────────────                                                             │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  For each asset class:                                                          │    │
│  │                                                                                 │    │
│  │  ECAP_asset = max(VaR_asset(99.9%, T), SVaR_asset(99.9%, T))                    │    │
│  │                                                                                 │    │
│  │  Conservative treatment ensures capital covers both current                     │    │
│  │  and stressed market conditions                                                 │    │
│  │                                                                                 │    │
│  │  Output: ECAP by asset class                                                    │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                              │                                                          │
│                              ▼                                                          │
│  STEP 5: AGGREGATION + ILLIQUIDITY ADD-ON                                               │
│  ─────────────────────────────────────────                                              │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Total ECAP = Σ ECAP_asset + Aged Inventory Illiquidity Add-on                  │    │
│  │                                                                                 │    │
│  │  Note: No diversification benefit applied at ECAP aggregation level             │    │
│  │  (conservative treatment for capital purposes)                                  │    │
│  │                                                                                 │    │
│  │  Illiquidity add-on from MR-L4-014 Aged Inventory Monitoring                    │    │
│  │                                                                                 │    │
│  │  Output: Total ECAP (Market Risk)                                               │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Confidence Level Scaling

#### 4.2.1 Empirical Approach (Primary Method)

For sufficient sample sizes, ECAP uses the empirical 99.9th percentile directly from the P&L distribution:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        EMPIRICAL 99.9% PERCENTILE                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  VaR (500 observations):                                                                │
│  • 99.9th percentile position = 500 × 0.001 = 0.5 → Round to 1st worst                  │
│  • Use average of 1st and 2nd worst for stability                                       │
│  • VaR(99.9%) = (P&L_rank1 + P&L_rank2) / 2                                             │
│                                                                                         │
│  SVaR (250 observations):                                                               │
│  • 99.9th percentile position = 250 × 0.001 = 0.25 → Round to 1st worst                 │
│  • SVaR(99.9%) = P&L_rank1                                                              │
│                                                                                         │
│  EXAMPLE:                                                                               │
│  VaR P&L distribution (sorted worst to best):                                           │
│  [-$2.1M, -$1.9M, -$1.7M, -$1.5M, -$1.3M, ...]                                          │
│                                                                                         │
│  VaR(99%, 1-day) = 5th worst = $1.3M                                                    │
│  VaR(99.9%, 1-day) = avg(1st, 2nd) = ($2.1M + $1.9M) / 2 = $2.0M                        │
│                                                                                         │
│  Implied scaling factor = $2.0M / $1.3M = 1.54                                          │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.2.2 Parametric Scaling (Fallback Method)

When empirical data is insufficient or for validation purposes:

| Distribution Assumption | Scaling Factor (99% → 99.9%) | Rationale |
|-------------------------|------------------------------|-----------|
| **Normal** | 1.33 | z(99.9%)/z(99%) = 3.09/2.33 |
| **Fat-tailed (t-dist, df=5)** | 1.45 | Higher tail weight |
| **Meridian ECAP** | **1.40** | Conservative blend |

**Fallback Application**:
```
VaR(99.9%, 1-day) = VaR(99%, 1-day) × 1.40
SVaR(99.9%, 1-day) = SVaR(99%, 1-day) × 1.40
```

#### 4.2.3 Method Selection

| Condition | Method | Rationale |
|-----------|--------|-----------|
| Standard daily calculation | Empirical | Direct observation of tail |
| New portfolio (limited history) | Parametric | Insufficient tail observations |
| Validation/benchmarking | Both | Cross-check methods |
| Stressed conditions | Parametric | Tail may be understated empirically |

### 4.3 Liquidity Horizon Framework

#### 4.3.1 Asset Class Liquidity Horizons

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        LIQUIDITY HORIZON ASSIGNMENTS                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ASSET CLASS                     │ HORIZON │ √T SCALING │ RATIONALE                     │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  HIGHLY LIQUID (10 days)                                                                │
│  ───────────────────────                                                                │
│  G10 FX Spot/Forwards            │ 10 days │   1.00     │ Deep interbank markets        │
│  G10 Government Bonds            │ 10 days │   1.00     │ Benchmark securities          │
│  Major Equity Indices            │ 10 days │   1.00     │ Large cap, high ADV           │
│  Exchange-traded Futures         │ 10 days │   1.00     │ Standardized, cleared         │
│                                                                                         │
│  MODERATELY LIQUID (15 days)                                                            │
│  ──────────────────────────                                                             │
│  EM FX (Major)                   │ 15 days │   1.22     │ Reasonable depth, some gaps   │
│  G10 Interest Rate Swaps         │ 15 days │   1.22     │ OTC but well-traded           │
│  IG Credit (Benchmark)           │ 15 days │   1.22     │ Investment grade bonds        │
│                                                                                         │
│  LESS LIQUID (20 days)                                                                  │
│  ─────────────────────                                                                  │
│  IG Credit (Non-benchmark)       │ 20 days │   1.41     │ Smaller issue sizes           │
│  EM Rates                        │ 20 days │   1.41     │ Concentrated markets          │
│  Small/Mid Cap Equities          │ 20 days │   1.41     │ Lower ADV                     │
│  Equity Options (Vanilla)        │ 20 days │   1.41     │ OTC, position-dependent       │
│                                                                                         │
│  ILLIQUID (25 days)                                                                     │
│  ──────────────────                                                                     │
│  High Yield Credit               │ 25 days │   1.58     │ Wide bid-offer, episodic      │
│  EM Credit                       │ 25 days │   1.58     │ Thin markets                  │
│  Complex Derivatives             │ 25 days │   1.58     │ Bespoke, limited exit         │
│  Structured Products             │ 25 days │   1.58     │ Custom terms                  │
│  EM FX (Frontier)                │ 25 days │   1.58     │ Capital controls              │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.3.2 Horizon Scaling Mathematics

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        SQUARE ROOT OF TIME SCALING                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  FORMULA:                                                                               │
│  VaR(T-day) = VaR(1-day) × √T                                                           │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  SCALING FACTORS:                                                                       │
│                                                                                         │
│  Horizon (T)  │  √T    │  Relative to 10-day (√T/√10)                                   │
│  ─────────────┼────────┼──────────────────────────────                                  │
│  10 days      │  3.16  │  1.00 (baseline)                                               │
│  15 days      │  3.87  │  1.22                                                          │
│  20 days      │  4.47  │  1.41                                                          │
│  25 days      │  5.00  │  1.58                                                          │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  EXAMPLE:                                                                               │
│  High Yield Credit position:                                                            │
│  • VaR(99.9%, 1-day) = $500k                                                            │
│  • Liquidity horizon = 25 days                                                          │
│  • VaR(99.9%, 25-day) = $500k × √25 = $500k × 5.0 = $2.5M                               │
│                                                                                         │
│  vs. Regulatory treatment:                                                              │
│  • VaR(99%, 10-day) = $357k × √10 = $1.13M                                              │
│                                                                                         │
│  ECAP / Regulatory ratio = $2.5M / $1.13M = 2.2x                                        │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.3.3 Liquidity Horizon Calibration

| Calibration Factor | Data Source | Review Frequency |
|-------------------|-------------|------------------|
| Bid-offer spreads | Bloomberg, Tradeweb | Monthly |
| Average Daily Volume (ADV) | Exchange data, TRACE | Monthly |
| Position vs market size | Internal positions | Daily |
| Stress period experience | Historical analysis | Annual |
| Dealer depth | Counterparty feedback | Quarterly |

**Calibration Criteria**:

| Factor | 10-day | 15-day | 20-day | 25-day |
|--------|--------|--------|--------|--------|
| Bid-offer (% of notional) | <0.1% | 0.1-0.3% | 0.3-0.5% | >0.5% |
| Position/ADV ratio | <1% | 1-3% | 3-5% | >5% |
| Dealer count | >10 | 5-10 | 3-5 | <3 |

### 4.4 Worst-of Treatment

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        WORST-OF VaR/SVaR TREATMENT                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  RATIONALE:                                                                             │
│  • VaR reflects risk under current market conditions                                    │
│  • SVaR reflects risk under stressed market conditions                                  │
│  • ECAP should cover capital needs under EITHER scenario                                │
│  • Conservative approach appropriate for capital adequacy                               │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  FORMULA (per asset class):                                                             │
│                                                                                         │
│  ECAP_asset = max(VaR_asset(99.9%, T), SVaR_asset(99.9%, T))                            │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  EXAMPLE:                                                                               │
│                                                                                         │
│  Asset Class: IG Credit (T = 20 days)                                                   │
│                                                                                         │
│  VaR basis:                                                                             │
│  • VaR(99.9%, 1-day) = $800k                                                            │
│  • VaR(99.9%, 20-day) = $800k × √20 = $3.58M                                            │
│                                                                                         │
│  SVaR basis:                                                                            │
│  • SVaR(99.9%, 1-day) = $1.2M                                                           │
│  • SVaR(99.9%, 20-day) = $1.2M × √20 = $5.37M                                           │
│                                                                                         │
│  ECAP_IG_Credit = max($3.58M, $5.37M) = $5.37M (SVaR basis)                             │
│                                                                                         │
│  In this example, stressed conditions drive the capital requirement                     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.5 Aggregation and Diversification

#### 4.5.1 ECAP Aggregation Approach

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        ECAP AGGREGATION                                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  CONSERVATIVE APPROACH (No Diversification Benefit at ECAP Level):                      │
│                                                                                         │
│  Total ECAP = Σ ECAP_asset_class                                                        │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  RATIONALE FOR NO DIVERSIFICATION:                                                      │
│                                                                                         │
│  1. CORRELATION BREAKDOWN IN STRESS                                                     │
│     • Correlations tend toward 1 in severe stress                                       │
│     • Diversification benefit may evaporate when needed most                            │
│                                                                                         │
│  2. CAPITAL CONSERVATISM                                                                │
│     • ECAP is for capital adequacy, not day-to-day risk management                      │
│     • Better to hold excess capital than be undercapitalized                            │
│                                                                                         │
│  3. REGULATORY EXPECTATION                                                              │
│     • PRA expects conservative treatment in ICAAP                                       │
│     • Diversification benefit requires strong justification                             │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  NOTE: Diversification IS captured within each asset class through the                  │
│  underlying Historical Simulation aggregation (per MR-L6-001)                           │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.5.2 ECAP Breakdown Structure

| Level | Aggregation | Diversification |
|-------|-------------|-----------------|
| Position | Sum of P&L scenarios | Full (via HS) |
| Book | Sum across positions | Full (via HS) |
| Desk | Sum across books | Full (via HS) |
| Asset Class | Percentile of aggregated P&L | Full (via HS) |
| **Total ECAP** | **Sum across asset classes** | **None (conservative)** |

### 4.6 Aged Inventory Illiquidity Add-on

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        AGED INVENTORY ILLIQUIDITY ADD-ON                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  SOURCE: MR-L4-014 Aged Inventory Monitoring                                            │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  AGED INVENTORY CRITERIA:                                                               │
│  • Position held > 6 months (180 calendar days)                                         │
│  • Turnover < 10% in trailing 90 days                                                   │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  ILLIQUIDITY ADD-ON CALCULATION:                                                        │
│                                                                                         │
│  For each aged position:                                                                │
│  1. Assess if standard liquidity horizon is sufficient                                  │
│  2. If not, assign extended horizon based on category:                                  │
│                                                                                         │
│     │ Category      │ Standard Horizon │ Extended Horizon │ Add-on Multiplier │         │
│     ├───────────────┼──────────────────┼──────────────────┼───────────────────┤         │
│     │ Watch List    │ Asset default    │ +5 days          │ ~1.2x             │         │
│     │ Aged          │ Asset default    │ +10 days         │ ~1.4x             │         │
│     │ Stale         │ Asset default    │ +20 days         │ ~1.7x             │         │
│                                                                                         │
│  3. Calculate add-on:                                                                   │
│     Illiquidity Add-on = ECAP(extended horizon) - ECAP(standard horizon)                │
│                                                                                         │
│  4. Aggregate across all aged positions                                                 │
│                                                                                         │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  TOTAL ECAP FORMULA:                                                                    │
│                                                                                         │
│  Total ECAP = Base ECAP + Aged Inventory Illiquidity Add-on                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Model Assumptions and Limitations

### 5.1 Key Assumptions

| Assumption | Description | Validation |
|------------|-------------|------------|
| **Square root of time** | Volatility scales with √T | Autocorrelation study (MR-L6-001 Section 5.4) |
| **Static portfolio** | Positions unchanged during horizon | Daily recalculation mitigates |
| **Historical distribution** | Past returns represent future risk | SVaR captures stressed conditions |
| **Liquidity horizon sufficiency** | Assigned horizons allow orderly exit | Annual calibration review |
| **No diversification at aggregate** | Conservative for capital | Stress correlation analysis |

### 5.2 Model Limitations

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        MODEL LIMITATIONS                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  1. LIQUIDITY HORIZON UNCERTAINTY                                                       │
│     Limitation: Actual liquidation time may exceed assigned horizon in severe stress    │
│     Mitigation: Conservative horizon assignments; aged inventory monitoring             │
│                                                                                         │
│  2. SQUARE ROOT SCALING ASSUMPTION                                                      │
│     Limitation: May understate risk for mean-reverting or trending assets               │
│     Mitigation: Conservative 99.9% confidence; worst-of treatment                       │
│                                                                                         │
│  3. EXTREME TAIL ESTIMATION                                                             │
│     Limitation: 99.9% percentile based on limited observations (1 in 500)               │
│     Mitigation: Averaging approach; parametric fallback; stress testing overlay         │
│                                                                                         │
│  4. CORRELATION STABILITY                                                               │
│     Limitation: Asset class correlations may change in stress                           │
│     Mitigation: No diversification benefit at aggregate level                           │
│                                                                                         │
│  5. FORWARD-LOOKING GAPS                                                                │
│     Limitation: Historical data may not capture emerging risks                          │
│     Mitigation: Complementary stress testing; scenario analysis                         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Complementary Measures

| Limitation | Complementary Measure | Reference |
|------------|----------------------|-----------|
| Liquidity horizon uncertainty | Aged inventory monitoring | MR-L4-014 |
| Extreme tail estimation | Scenario stress testing | MR-L5-002 |
| Forward-looking gaps | Reverse stress testing | MR-L4-011 |
| Model risk | Annual validation | Section 6 |

---

## 6. EaR and ECAP Outputs and Usage

### 6.1 Output Structure

| Output | Granularity | Frequency | Consumer |
|--------|-------------|-----------|----------|
| **Entity EaR** | Entity | Daily | ExCo, ALCO, BRMC (vs RAS) |
| **EaR by Risk Type** | Risk type | Monthly | RMC, ALCO |
| **EaR by Desk** | Desk | Daily | Business, Market Risk |
| **Total ECAP** | Entity | Daily | ALCO, ICAAP |
| **ECAP by Asset Class** | Asset class | Daily | Market Risk, MLRC |
| **ECAP by Desk** | Desk | Daily | Business, Market Risk |
| **ECAP vs Regulatory** | Entity | Daily | Capital Management |
| **Illiquidity Add-on** | Entity | Quarterly | ICAAP |
| **EaR/ECAP/VaR Ratios** | Entity | Daily | Market Risk, RAV |

### 6.2 ICAAP Integration

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        ECAP IN ICAAP                                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ICAAP SECTION: Market Risk Capital Assessment                                          │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │                                                                                 │    │
│  │  1. Pillar 1 Market Risk Capital                                                │    │
│  │     • IMA: VaR + SVaR + IRC                                                     │    │
│  │     • Source: Daily regulatory calculation                                      │    │
│  │                                                                                 │    │
│  │  2. Pillar 2A Market Risk Capital (ECAP)                                        │    │
│  │     • ECAP at 99.9% with liquidity horizons                                     │    │
│  │     • Includes aged inventory illiquidity add-on                                │    │
│  │     • Source: Quarterly average ECAP                                            │    │
│  │                                                                                 │    │
│  │  3. Pillar 2A Add-on                                                            │    │
│  │     • = max(0, ECAP - Pillar 1)                                                 │    │
│  │     • Only charged if ECAP exceeds regulatory capital                           │    │
│  │                                                                                 │    │
│  │  4. Stress Capital                                                              │    │
│  │     • Stressed ECAP under PRA scenarios                                         │    │
│  │     • Feeds into stressed capital projections                                   │    │
│  │                                                                                 │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  TIMING:                                                                                │
│  • ECAP calculated daily                                                                │
│  • Quarterly average used for ICAAP                                                     │
│  • Annual ICAAP submission to PRA                                                       │
│  • Quarterly internal capital assessment                                                │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Performance Measurement Usage

| Use Case | ECAP Application |
|----------|------------------|
| **Capital Allocation** | ECAP allocated to desks/businesses |
| **RAROC** | Return on ECAP for performance measurement |
| **Pricing** | ECAP cost included in trade pricing |
| **Limit Setting** | ECAP utilisation as secondary constraint |

---

## 7. Model Validation

### 7.1 Validation Framework

| Validation Type | Frequency | Responsibility |
|-----------------|-----------|----------------|
| **Confidence level scaling** | Annual | Model Risk |
| **Liquidity horizon calibration** | Annual | RMA + Model Risk |
| **ECAP/VaR ratio monitoring** | Daily | RAV |
| **Independent validation** | Annual | Model Risk |
| **Benchmark comparison** | Annual | RMA |

### 7.2 Key Validation Tests

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        ECAP VALIDATION TESTS                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  1. CONFIDENCE LEVEL VALIDATION                                                         │
│     • Compare empirical vs parametric 99.9% scaling                                     │
│     • Expected ratio: 1.3 - 1.5 (empirical/99%)                                         │
│     • Flag if <1.2 or >1.7                                                              │
│                                                                                         │
│  2. LIQUIDITY HORIZON BACKTESTING                                                       │
│     • For each asset class, compare actual liquidation times to assigned horizons       │
│     • Review stress period experience (GFC, COVID)                                      │
│     • Adjust horizons if evidence warrants                                              │
│                                                                                         │
│  3. ECAP/VaR RATIO MONITORING                                                           │
│     • Expected range: 1.5x - 2.5x                                                       │
│     • Lower bound driven by confidence scaling                                          │
│     • Upper bound driven by illiquid asset concentration                                │
│     • Investigate if outside range                                                      │
│                                                                                         │
│  4. ICAAP RECONCILIATION                                                                │
│     • Reconcile daily ECAP to quarterly ICAAP submission                                │
│     • Explain any material differences                                                  │
│     • Finance sign-off required                                                         │
│                                                                                         │
│  5. PEER BENCHMARKING                                                                   │
│     • Compare ECAP/Pillar 1 ratio to peer banks                                         │
│     • Identify methodology differences                                                  │
│     • Document rationale for deviations                                                 │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Validation KPIs

| KPI | Target | Threshold | Escalation |
|-----|--------|-----------|------------|
| Empirical/parametric scaling ratio | 0.95 - 1.05 | 0.85 - 1.15 | Model Risk |
| ECAP/VaR ratio stability | ±10% monthly | ±20% monthly | RMA |
| Liquidity horizon breach rate | <5% | <10% | MLRC |
| ICAAP reconciliation breaks | 0 | <$1M | Finance |

---

## 8. Model Change Governance

### 8.1 Change Categories

| Category | Examples | Approval Authority |
|----------|----------|-------------------|
| **Material** | Confidence level; aggregation approach | Model Risk Committee + MLRC + PRA |
| **Significant** | Liquidity horizon framework; scaling factors | MLRC |
| **Minor** | Individual asset horizon assignment | RMA Head |
| **Calibration** | Horizon updates within framework | RMA |

### 8.2 PRA Notification Requirements

| Change Type | Notification | Timing |
|-------------|--------------|--------|
| Confidence level change | Pre-approval required | Before implementation |
| Aggregation methodology | Pre-approval required | Before implementation |
| Liquidity framework | Notification | Within ICAAP cycle |
| Horizon calibration | Disclosure | Annual ICAAP |

---

## 9. Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| **RMA (Owner)** | Methodology ownership; parameter calibration; documentation |
| **Model Risk** | Independent validation; model approval; ongoing monitoring |
| **RAV** | Daily calculation oversight; ECAP/VaR monitoring |
| **Finance** | ICAAP integration; capital reporting |
| **ALCO** | ECAP governance; capital allocation decisions |
| **MLRC** | Methodology approval; limit monitoring |

---

## 10. Related Documents

| Document | Relationship |
|----------|--------------|
| [Risk Appetite Statement](../../L3-Governance/risk-appetite-statement.md) | EaR and ECAP limits/thresholds (GOV-L3-010) |
| [Risk Appetite Framework](../../L3-Governance/risk-appetite-framework.md) | Methodology for appetite setting (GOV-L3-011) |
| [Historical Simulation VaR/SVaR](./var-svar-methodology.md) | Parent model - base calculation |
| [Market Risk Policy (Section 8.6)](../../L3-Governance/policies/market-risk-policy.md) | EaR/ECAP regulatory drivers and governance |
| [Risk Engine Calculation (Section 6.7)](../../L4-Processes/processes/risk-engine-calculation.md) | EaR/ECAP calculation process |
| [Aged Inventory Monitoring](../../L4-Processes/processes/aged-inventory-monitoring.md) | Source for illiquidity add-on (ECAP) |
| [ECAP and EaR Controls](../../L5-Controls/market-risk/ecap-controls.md) | L5 control framework |
| [System Architecture](../../L7-Systems/market-risk/system-architecture.md) | System implementation |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-16 | Initial version - standalone ECAP methodology extending MR-L6-001 | Model Risk Committee / MLRC |
| 1.1 | 2025-01-17 | Added Earnings at Risk (EaR) methodology (Section 3); linked to Risk Appetite Statement (GOV-L3-010) | Model Risk Committee / MLRC |

### 11.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full methodology review | Annual | January 2026 |
| Liquidity horizon calibration | Annual | January 2026 |
| Confidence scaling validation | Annual | January 2026 |
| Independent validation | Annual | January 2026 |
| ICAAP alignment review | Quarterly | April 2025 |

### 11.3 Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Head of RMA | [Name] | | |
| Head of Model Risk | [Name] | | |
| CRO | [Name] | | |
| MLRC Chair | [Name] | | |

---

*End of Document*
