---
# Control Metadata
control_id: MR-L5-007
control_name: Economic Capital (ECAP) and Earnings at Risk (EaR) Controls
version: 1.1
effective_date: 2025-01-16
next_review_date: 2026-01-16
owner: Head of Market Risk
approving_committee: RMC

# Taxonomy Linkages
parent_process: MR-L4-006  # Risk Engine Calculation
parent_framework: MR-L3-001  # Market Risk Policy
risk_appetite: GOV-L3-010  # Risk Appetite Statement (EaR/ECAP limits)
l1_requirements:
  - REQ-L1-001  # CRR/CRR III
  - REQ-L1-006  # CRD VI
  - REQ-L1-007  # PRA SS13/13 (Market Risk)
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
l6_models:
  - MR-L6-001   # Historical Simulation VaR (extended for ECAP/EaR)
  - MR-L6-002   # ECAP Methodology
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-004  # Risk Reporting DataMart
---

# Economic Capital (ECAP) and Earnings at Risk (EaR) Controls

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Control ID** | MR-L5-007 |
| **Version** | 1.1 |
| **Effective Date** | 16 January 2025 |
| **Parent Framework** | Market Risk Policy (MR-L3-001), Risk Appetite Statement (GOV-L3-010) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

This document defines the controls for **Economic Capital (ECAP)** and **Earnings at Risk (EaR)** calculation, monitoring, and governance. These are the two primary internal capital measures used by the Bank:

| Measure | Confidence | Purpose | Governance |
|---------|------------|---------|------------|
| **EaR** | 90% (1-in-10 year) | Earnings volatility measure for Risk Appetite | RMC → ExCo → BRMC |
| **ECAP** | 99.9% (1-in-1000 year) | Solvency/capital adequacy for ICAAP | RMC → ALCO → Board |

Both measures are derived from the same VaR/SVaR calculation engine using different confidence level scalings. They are linked to the **Risk Appetite Statement (GOV-L3-010)** as Level 1 and Level 2 risk appetite metrics.

> **Regulatory Drivers**: For ECAP regulatory requirements (CRD VI, CRR, PRA SS13/13, BCBS Pillar 2), see [Market Risk Policy Section 8.6.1](../../L3-Governance/policies/market-risk-policy.md#861-ecap-regulatory-drivers).
>
> **Risk Appetite Linkage**: EaR and ECAP thresholds are defined in the [Risk Appetite Statement (GOV-L3-010)](../../L3-Governance/risk-appetite-statement.md) and methodology in the [Risk Appetite Framework (GOV-L3-011)](../../L3-Governance/risk-appetite-framework.md).

---

## 2. EaR, ECAP and Regulatory VaR Comparison

### 2.1 Key Differences

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  EaR vs ECAP vs REGULATORY VaR COMPARISON                                                       │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│  PARAMETER          │  REGULATORY VaR/SVaR  │  EARNINGS AT RISK (EaR) │  ECONOMIC CAPITAL (ECAP)│
│  ─────────────────────────────────────────────────────────────────────────────────────────────  │
│  Confidence Level   │  99%                  │  90% (1-in-10 years)    │  99.9% (1-in-1000 years)│
│  Time Horizon       │  10 days              │  1 year                 │  1 year                 │
│  Liquidity Horizon  │  10 days (uniform)    │  Asset-specific         │  Asset-specific         │
│  Observation Period │  500 days / Stressed  │  Same as VaR/SVaR       │  Worst-of VaR/SVaR      │
│  Purpose            │  Pillar 1 capital     │  Risk Appetite (EaR)    │  Pillar 2 / ICAAP       │
│  Frequency          │  Daily                │  Monthly (RAS)          │  Monthly (RAS/ICAAP)    │
│  Governance         │  MLRC                 │  RMC → ExCo → BRMC      │  RMC → ALCO → Board     │
│  Regulatory Driver  │  CRR Article 325ff    │  Internal (RAS)         │  CRD VI, PRA SS13/13    │
│  ─────────────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                                 │
│  RELATIONSHIP:                                                                                  │
│  • VaR < EaR < ECAP (always)                                                                    │
│  • EaR ≈ VaR × 1.9 (scaling 99% to 90% over 1 year)                                             │
│  • ECAP ≈ VaR × 2.5-3.0 (99% to 99.9% with liquidity adjustment)                                │
│  • EaR/ECAP ratio ≈ 0.6-0.7 (EaR is ~60-70% of ECAP due to lower confidence)                    │
│                                                                                                 │
│  KEY PRINCIPLE: These measures form a hierarchy of conservatism:                                │
│  1. VaR: Daily trading limit management (99%, 10-day)                                           │
│  2. EaR: Annual earnings protection (90%, 1-year) - Risk Appetite                               │
│  3. ECAP: Solvency protection (99.9%, 1-year) - ICAAP                                           │
│                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 EaR and ECAP Calculation Formulas

**From VaR to EaR (90% confidence, 1-year horizon):**

```
EaR_Market = VaR(1d,99%) × (Normsinv(0.9) / Normsinv(0.99)) × √250

Where:
• VaR(1d,99%) = Average daily VaR for preceding 60 business days
• Normsinv(0.9)/Normsinv(0.99) = 1.282 / 2.326 = 0.551 (confidence scaling)
• √250 = 15.81 (1-day to 1-year scaling)
• Net multiplier ≈ 8.7 (but applied to 1-day VaR, so typically EaR < ECAP)
```

**From VaR to ECAP (99.9% confidence, 1-year horizon with liquidity adjustment):**

```
ECAP_Market = VaR(1d,99%) × (Normsinv(0.999) / Normsinv(0.99)) × √250 × Liquidity_Adj

Where:
• Normsinv(0.999)/Normsinv(0.99) = 3.09 / 2.326 = 1.33 (confidence scaling)
• Liquidity_Adj = Asset-specific factor (1.0 - 1.58)
• Takes worst-of VaR or SVaR basis
```

### 2.3 Risk Appetite Linkage

Both EaR and ECAP are **Level 1 Risk Appetite metrics** as defined in [GOV-L3-010](../../L3-Governance/risk-appetite-statement.md):

| Metric | Green | Amber | Red |
|--------|-------|-------|-----|
| **EaR (Market Risk)** | <$105m | $105m - $120m | >$120m |
| **ECAP Ratio (AFR/ECap)** | >130% | 120% - 130% | <120% |
| **Market Risk ECAP Allocation** | <$500m | $500m - $550m | >$550m |

The EaR and ECAP are also cascaded as **Level 2 allocations** to Market Risk from the enterprise totals.

### 2.4 EaR and ECAP Calculation Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  EaR AND ECAP CALCULATION FLOW (MR-L4-006 Section 6.7)                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Step 1: Calculate base VaR and SVaR at 99% (standard process)                  │    │
│  └──────────────────────────────────┬──────────────────────────────────────────────┘    │
│                                     │                                                   │
│                                     ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Step 2: Scale to 99.9% confidence                                              │    │
│  │                                                                                 │    │
│  │  99.9% VaR ≈ 99% VaR × 1.4 (normal distribution approximation)                  │    │
│  │  OR use empirical 99.9th percentile from Historical Simulation                  │    │
│  └──────────────────────────────────┬──────────────────────────────────────────────┘    │
│                                     │                                                   │
│                                     ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Step 3: Apply asset-specific liquidity horizon scaling                         │    │
│  │                                                                                 │    │
│  │  │ Asset Class          │ Horizon │ Scaling Factor (√T/10)                      │    │
│  │  ├──────────────────────┼─────────┼─────────────────────────                    │    │
│  │  │ G10 FX               │ 10 days │ 1.00                                        │    │
│  │  │ Large Cap Equity     │ 10 days │ 1.00                                        │    │
│  │  │ G10 Government Bonds │ 10 days │ 1.00                                        │    │
│  │  │ IG Credit            │ 20 days │ 1.41                                        │    │
│  │  │ HY Credit            │ 25 days │ 1.58                                        │    │
│  │  │ EM Rates             │ 20 days │ 1.41                                        │    │
│  │  │ EM FX                │ 15 days │ 1.22                                        │    │
│  │  │ Small Cap Equity     │ 20 days │ 1.41                                        │    │
│  │  │ Complex Derivatives  │ 25 days │ 1.58                                        │    │
│  └──────────────────────────────────┬──────────────────────────────────────────────┘    │
│                                     │                                                   │
│                                     ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Step 4: Take worst-of VaR or SVaR basis                                        │    │
│  │                                                                                 │    │
│  │  ECAP = max(ECAP_VaR_basis, ECAP_SVaR_basis)                                    │    │
│  └──────────────────────────────────┬──────────────────────────────────────────────┘    │
│                                     │                                                   │
│                                     ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Step 5: Add illiquidity add-on from Aged Inventory (MR-L4-014)                 │    │
│  │                                                                                 │    │
│  │  Final ECAP = Base ECAP + Aged Inventory Illiquidity Adjustment                 │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.5 EaR and ECAP Thresholds

| Metric | Green | Amber | Red | Escalation |
|--------|-------|-------|-----|------------|
| **EaR (Market Risk)** | <$105m | $105m - $120m | >$120m | RMC → ExCo → BRMC |
| **ECAP (Market Risk)** | <$450m | $450m - $500m | >$500m | RMC → ALCO |
| **ECAP Utilisation** | <80% | 80% - 90% | >90% | ALCO |
| **EaR/ECAP Ratio** | 0.55 - 0.75 | <0.55 or >0.75 | Investigate | Market Risk |
| **ECAP/VaR Ratio** | 1.5x - 2.5x | <1.2x or >2.5x | Investigate | Market Risk |

**Note**: EaR and ECAP thresholds are aligned with the [Risk Appetite Statement (GOV-L3-010)](../../L3-Governance/risk-appetite-statement.md). The EaR triggers are set at 10% below limit as per the Risk Appetite Framework.

---

## 3. Control Objectives

| Objective ID | Objective | Risk Mitigated |
|--------------|-----------|----------------|
| **CO-01** | EaR and ECAP are calculated daily using approved methodology | Incorrect capital/earnings assessment |
| **CO-02** | EaR and ECAP incorporate asset-specific liquidity horizons | Underestimation of illiquidity risk |
| **CO-03** | ECAP includes aged inventory illiquidity adjustment | Missing ICAAP capital for illiquid positions |
| **CO-04** | EaR is compared to Risk Appetite limits | Risk appetite breach |
| **CO-05** | ECAP is compared to allocated economic capital | Capital inadequacy |
| **CO-06** | ECAP contributes accurately to ICAAP | Regulatory non-compliance |
| **CO-07** | EaR contributes accurately to RAS dashboard | Governance gap |
| **CO-08** | EaR/ECAP methodology is validated annually | Model risk |
| **CO-09** | EaR and ECAP are signed off daily alongside VaR/SVaR | Governance gap |

---

## 4. Control Inventory

### 4.1 Control Summary

| Control ID | Control Name | Type | Frequency | Owner |
|------------|--------------|------|-----------|-------|
| EC-C01 | Daily EaR and ECAP Calculation Validation | Detective | Daily | RAV |
| EC-C02 | Liquidity Horizon Assignment Review | Preventive | Monthly | Market Risk |
| EC-C03 | ECAP vs Allocated Capital Comparison | Detective | Daily | Market Risk |
| EC-C04 | EaR vs Risk Appetite Limit Comparison | Detective | Daily | Market Risk |
| EC-C05 | ECAP/VaR and EaR/ECAP Ratio Monitoring | Detective | Daily | RAV |
| EC-C06 | Aged Inventory Illiquidity Add-on | Detective | Quarterly | Market Risk |
| EC-C07 | EaR and ECAP Sign-off (Daily Report) | Preventive | Daily | Head of Market Risk |
| EC-C08 | ECAP ICAAP Contribution Review | Detective | Quarterly | Market Risk |
| EC-C09 | EaR RAS Dashboard Contribution | Detective | Monthly | Market Risk |
| EC-C10 | EaR/ECAP Methodology Validation | Preventive | Annual | Model Risk |
| EC-C11 | ALCO ECAP Dashboard Review | Detective | Monthly | ALCO |
| EC-C12 | RMC EaR/RAS Dashboard Review | Detective | Monthly | RMC |
| EC-C13 | Capital and Earnings Utilisation Trend Analysis | Detective | Weekly | Market Risk |

---

## 5. Control Details

### 5.1 EC-C01: Daily ECAP Calculation Validation

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: EC-C01 - Daily ECAP Calculation Validation                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Ensure ECAP is calculated correctly using approved methodology              │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Daily (by 08:00)                                                            │
│  OWNER: RAV                                                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CONTROL ACTIVITIES:                                                                    │
│  1. Verify ECAP batch completed successfully (check Risk Engine logs)                   │
│  2. Validate ECAP > regulatory VaR (must always be true)                                │
│  3. Validate ECAP > regulatory SVaR (must always be true)                               │
│  4. Check confidence level scaling applied correctly (99% → 99.9%)                      │
│  5. Verify liquidity horizon scalings match approved asset class mappings               │
│  6. Confirm worst-of treatment applied (VaR basis vs SVaR basis)                        │
│  7. Reconcile ECAP components sum to total                                              │
│                                                                                         │
│  VALIDATION CHECKS:                                                                     │
│  • ECAP ≥ 1.2 × max(VaR, SVaR) - if not, investigate                                    │
│  • ECAP breakdown by asset class available                                              │
│  • Day-on-day change explainable by position or market moves                            │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Risk Engine batch completion log                                                     │
│  • ECAP validation checklist (daily)                                                    │
│  • ECAP vs VaR/SVaR reconciliation                                                      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 EC-C02: Liquidity Horizon Assignment Review

| Attribute | Value |
|-----------|-------|
| **Control ID** | EC-C02 |
| **Objective** | Ensure all positions have appropriate liquidity horizon assignments |
| **Type** | Preventive |
| **Frequency** | Monthly |
| **Owner** | Market Risk |

**Control Activities**:
1. Extract all instrument types from Risk Engine
2. Verify each instrument has liquidity horizon assignment
3. Review new instruments added in month - confirm horizon assigned
4. Challenge any horizon assignments that appear inconsistent with:
   - Market liquidity data (bid-ask spreads, ADV)
   - Aged inventory analysis
   - Stress period liquidity experience
5. Propose adjustments for MLRC approval if warranted

**Horizon Review Criteria**:

| Factor | Shorter Horizon (10 days) | Longer Horizon (20-25 days) |
|--------|---------------------------|----------------------------|
| Bid-ask spread | Tight (<5bp) | Wide (>20bp) |
| ADV | High | Low |
| Number of dealers | Many (>10) | Few (<5) |
| Position vs market | Small | Large |
| Stress experience | Remained liquid | Became illiquid |

**Evidence**:
- Monthly Liquidity Horizon Review Report
- MLRC approval for any changes

### 5.3 EC-C03: ECAP vs Allocated Capital Comparison

| Attribute | Value |
|-----------|-------|
| **Control ID** | EC-C03 |
| **Objective** | Ensure ECAP remains within allocated economic capital |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | Market Risk |

**Control Activities**:
1. Compare daily ECAP to allocated economic capital for Market Risk
2. Calculate utilisation percentage: ECAP / Allocated Capital × 100
3. Apply traffic light status:
   - GREEN: 0-79% utilisation
   - AMBER: 80-89% utilisation (Warning)
   - RED: 90%+ utilisation (Escalate to ALCO)
4. Include in daily Market Risk report

**Escalation**:
- Warning (80%): Notify Head of Market Risk
- Breach (90%): Escalate to ALCO; prepare capital action plan

**Evidence**:
- Daily ECAP vs Allocated Capital report
- Escalation notifications (if applicable)

### 5.4 EC-C04: ECAP/VaR Ratio Monitoring

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: EC-C04 - ECAP/VaR Ratio Monitoring                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Monitor relationship between ECAP and regulatory VaR as validation check    │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Daily                                                                       │
│  OWNER: RAV                                                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  RATIONALE:                                                                             │
│  The ECAP/VaR ratio provides insight into:                                              │
│  • Portfolio liquidity profile (higher ratio = more illiquid assets)                    │
│  • Consistency of methodology                                                           │
│  • Changes in portfolio composition affecting capital requirements                      │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EXPECTED RANGE:                                                                        │
│  • Minimum: 1.2x (due to confidence level scaling alone)                                │
│  • Normal: 1.5x - 2.0x (typical for diversified trading book)                           │
│  • Maximum: 2.5x (indicates high proportion of illiquid assets)                         │
│                                                                                         │
│  CONTROL ACTIVITIES:                                                                    │
│  1. Calculate daily ECAP / VaR ratio                                                    │
│  2. Track 20-day moving average                                                         │
│  3. Flag if ratio falls outside expected range:                                         │
│     • Alert if <1.2x (calculation error likely)                                         │
│     • Alert if >2.5x (review illiquid asset concentration)                              │
│  4. Investigate significant day-on-day changes (>10%)                                   │
│  5. Include ratio trend in MLRC reporting                                               │
│                                                                                         │
│  IMPLICATIONS:                                                                          │
│                                                                                         │
│  LOW RATIO (<1.2x):                                                                     │
│  • Likely calculation or methodology error                                              │
│  • Immediate investigation required                                                     │
│                                                                                         │
│  HIGH RATIO (>2.5x):                                                                    │
│  • High concentration in illiquid assets                                                │
│  • May indicate need for portfolio rebalancing                                          │
│  • Review against aged inventory analysis                                               │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Daily ECAP/VaR ratio in Market Risk report                                           │
│  • Alert notifications                                                                  │
│  • Investigation notes                                                                  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.5 EC-C05: Aged Inventory Illiquidity Add-on

| Attribute | Value |
|-----------|-------|
| **Control ID** | EC-C05 |
| **Objective** | Ensure aged inventory illiquidity is captured in ECAP |
| **Type** | Detective |
| **Frequency** | Quarterly |
| **Owner** | Market Risk |

**Control Activities**:
1. Obtain aged inventory list from MR-L4-014 Aged Inventory Monitoring
2. For each aged position, assess if standard liquidity horizon is sufficient
3. Calculate illiquidity add-on for positions requiring extended horizons:
   - Extended horizon ECAP - Standard horizon ECAP = Add-on
4. Aggregate illiquidity add-ons by desk and entity
5. Include in quarterly ICAAP submission

**Integration with MR-L4-014**:

| MR-L4-014 Output | Use in EC-C05 |
|------------------|---------------|
| Aged inventory list | Positions requiring extended horizons |
| Turnover analysis | Validate liquidity horizon assumption |
| Market depth assessment | Calibrate extended horizon length |
| Quarterly aged inventory report | Source for illiquidity add-on calculation |

**Evidence**:
- Quarterly Illiquidity Add-on Calculation
- Aged inventory to ECAP mapping
- ICAAP submission documentation

### 5.6 EC-C06: ECAP Sign-off (Daily Report)

| Attribute | Value |
|-----------|-------|
| **Control ID** | EC-C06 |
| **Objective** | Ensure ECAP is formally reviewed and signed off daily |
| **Type** | Preventive |
| **Frequency** | Daily |
| **Owner** | Head of Market Risk |

**Control Activities**:
1. ECAP included in daily Market Risk Report (MR-L4-007)
2. Head of Market Risk reviews ECAP as part of daily sign-off checklist:
   - ECAP value and day-on-day change
   - ECAP vs allocated capital utilisation
   - ECAP/VaR ratio
   - Any alerts or exceptions
3. Sign-off confirms:
   - ECAP calculated using approved methodology
   - Results reviewed and understood
   - No unresolved data quality issues
4. Sign-off recorded in report system

**Sign-off Checklist (ECAP Section)**:

| Item | Check |
|------|-------|
| ECAP calculated successfully | ☐ |
| ECAP > VaR and > SVaR | ☐ |
| ECAP vs allocated capital < 90% | ☐ |
| ECAP/VaR ratio within range | ☐ |
| D-o-D change explainable | ☐ |
| No data quality issues | ☐ |

**Evidence**:
- Daily Market Risk Report (signed)
- Sign-off log with timestamp

### 5.7 EC-C07: ECAP ICAAP Contribution Review

| Attribute | Value |
|-----------|-------|
| **Control ID** | EC-C07 |
| **Objective** | Ensure ECAP accurately contributes to ICAAP |
| **Type** | Detective |
| **Frequency** | Quarterly |
| **Owner** | Market Risk |

**Control Activities**:
1. Reconcile quarterly average ECAP to ICAAP submission
2. Verify ECAP breakdown by risk type in ICAAP:
   - Interest Rate Risk
   - FX Risk
   - Equity Risk
   - Credit Spread Risk
   - Commodity Risk
3. Confirm illiquidity add-on from aged inventory included
4. Cross-check with Finance/Treasury ICAAP consolidation
5. Document any differences and explanations

**ICAAP Integration Points**:

| ICAAP Section | ECAP Contribution |
|---------------|-------------------|
| Pillar 2A - Market Risk | Quarterly average ECAP |
| Illiquidity Risk | Aged inventory illiquidity add-on |
| Concentration Risk | ECAP concentration attribution |
| Stress Testing | Stressed ECAP scenarios |

**Evidence**:
- Quarterly ECAP to ICAAP reconciliation
- ICAAP submission (Market Risk section)
- Finance sign-off on reconciliation

### 5.8 EC-C08: ECAP Methodology Validation

| Attribute | Value |
|-----------|-------|
| **Control ID** | EC-C08 |
| **Objective** | Ensure ECAP methodology remains fit for purpose |
| **Type** | Preventive |
| **Frequency** | Annual |
| **Owner** | Model Risk |

**Control Activities**:
1. Review ECAP methodology document for currency
2. Validate confidence level scaling approach:
   - Compare parametric scaling vs empirical 99.9th percentile
   - Assess fat-tail adjustment adequacy
3. Review liquidity horizon calibration:
   - Compare assigned horizons to observed market liquidity
   - Assess stress period liquidity experience
4. Validate worst-of treatment implementation
5. Benchmark against peer practices
6. Document findings and recommendations
7. Present to Model Risk Committee

**Validation Scope**:

| Component | Validation Approach |
|-----------|---------------------|
| 99.9% scaling | Compare parametric vs empirical; assess conservatism |
| Liquidity horizons | Market data analysis; stress period review |
| Worst-of treatment | Implementation testing |
| Aggregation | Correlation assumptions; diversification benefit |
| Illiquidity add-on | Aged inventory methodology review |

**Evidence**:
- Annual ECAP Methodology Validation Report
- Model Risk Committee minutes
- Remediation tracking (if applicable)

### 5.9 EC-C09: ALCO ECAP Dashboard Review

| Attribute | Value |
|-----------|-------|
| **Control ID** | EC-C09 |
| **Objective** | Governance oversight of ECAP and capital adequacy |
| **Type** | Detective |
| **Frequency** | Monthly |
| **Owner** | ALCO |

**Control Activities**:
1. Market Risk presents ECAP dashboard to ALCO
2. Dashboard includes:
   - ECAP vs allocated capital (utilisation %)
   - ECAP trend (3-month history)
   - ECAP breakdown by asset class
   - ECAP/VaR ratio trend
   - Aged inventory illiquidity contribution
   - Comparison to Pillar 1 capital requirement
3. ALCO challenges and approves actions
4. Decisions minuted and tracked

**ALCO Dashboard Contents**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        ECAP DASHBOARD - ALCO MONTHLY REVIEW                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  CAPITAL UTILISATION                                                                    │
│  ──────────────────────                                                                 │
│  │  Metric              │   Value    │  Allocated  │  Util %  │  Status  │              │
│  ├──────────────────────┼────────────┼─────────────┼──────────┼──────────┤              │
│  │  ECAP (Market Risk)  │   $58m     │   $75m      │   77%    │    🟢    │              │
│  │  Pillar 1 (VaR)      │   $42m     │   $50m      │   84%    │    🟡    │              │
│  │  ECAP/Pillar 1 Ratio │   1.38x    │    -        │    -     │    🟢    │              │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ECAP BY ASSET CLASS                                                                    │
│  ───────────────────────                                                                │
│  │  Asset Class        │   ECAP     │  % of Total │  Liq Horizon │                      │
│  ├─────────────────────┼────────────┼─────────────┼──────────────┤                      │
│  │  G10 Rates          │   $18m     │    31%      │    10 days   │                      │
│  │  IG Credit          │   $15m     │    26%      │    20 days   │                      │
│  │  FX                 │   $12m     │    21%      │    10-15 days│                      │
│  │  Equities           │   $8m      │    14%      │    10-20 days│                      │
│  │  HY/EM Credit       │   $5m      │     9%      │    25 days   │                      │
│  │  TOTAL              │   $58m     │   100%      │              │                      │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ILLIQUIDITY ADD-ON (from Aged Inventory)                                               │
│  ─────────────────────────────────────────                                              │
│  Aged positions requiring extended horizons: $3.2m                                      │
│  Illiquidity add-on contribution to ECAP: $0.8m                                         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Evidence**:
- ALCO agenda and pack
- ALCO minutes with decisions

### 5.10 EC-C10: Capital Utilisation Trend Analysis

| Attribute | Value |
|-----------|-------|
| **Control ID** | EC-C10 |
| **Objective** | Identify emerging capital pressure through trend analysis |
| **Type** | Detective |
| **Frequency** | Weekly |
| **Owner** | Market Risk |

**Control Activities**:
1. Analyse 4-week ECAP utilisation trend
2. Flag if:
   - Sustained high utilisation (>75% average over 4 weeks)
   - Upward trend (>10% increase over 4 weeks)
   - ECAP/VaR ratio increasing (portfolio becoming less liquid)
3. Identify drivers of trend:
   - Business growth
   - Market moves affecting risk
   - Portfolio composition changes
4. Prepare trend report for MLRC
5. Recommend actions if structural issues identified:
   - Portfolio rebalancing
   - Capital allocation increase request
   - Business strategy review

**Evidence**:
- Weekly Capital Utilisation Trend Report
- MLRC presentation

---

## 6. Control Testing Schedule

| Control | Test Frequency | Test Type | Tester |
|---------|---------------|-----------|--------|
| EC-C01 | Monthly | Sample testing | Internal Audit |
| EC-C02 | Quarterly | Horizon mapping review | Market Risk |
| EC-C03 | Monthly | Reconciliation | RAV |
| EC-C04 | Monthly | Ratio analysis | RAV |
| EC-C05 | Quarterly | Calculation review | Internal Audit |
| EC-C06 | Quarterly | Walkthrough | Operational Risk |
| EC-C07 | Quarterly | Reconciliation to ICAAP | Finance |
| EC-C08 | Annual | Full validation | Model Risk |
| EC-C09 | Ongoing | Attendance/minutes | ALCO Secretary |
| EC-C10 | Monthly | Trend review | Market Risk |

---

## 7. Key Risk Indicators (KRIs)

| KRI ID | Indicator | Threshold | Escalation |
|--------|-----------|-----------|------------|
| KRI-EC-01 | ECAP vs Allocated Capital utilisation | >85% | ALCO |
| KRI-EC-02 | ECAP/VaR ratio | <1.2x or >2.5x | Market Risk |
| KRI-EC-03 | ECAP day-on-day change | >15% | Head of Market Risk |
| KRI-EC-04 | Aged inventory illiquidity add-on | >5% of ECAP | MLRC |
| KRI-EC-05 | ECAP methodology validation findings | Any High | Model Risk Committee |
| KRI-EC-06 | ECAP sign-off delays | >2 hours | RAV |

---

## 8. Related Controls

| Control ID | Control Name | Relationship |
|------------|--------------|--------------|
| MR-L5-001 | VaR/SVaR Limits Controls | ECAP builds on VaR/SVaR calculation |
| MR-L5-005 | Concentration Limits Controls | Concentration feeds liquidity horizon assessment |
| MR-L5-002 | Stress Limits Controls | Stressed ECAP scenarios |
| MR-L4-014 | Aged Inventory Monitoring | Source for illiquidity add-on |

---

## 9. Document Control

### 9.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-16 | Initial version - new document for Economic Capital controls, aligned with MR-L4-006 Section 6.7 | RMC |
| 1.1 | 2025-01-17 | Added Earnings at Risk (EaR) as parallel measure; linked to Risk Appetite Statement (GOV-L3-010) and Risk Appetite Framework (GOV-L3-011); added EaR-specific controls | RMC |

### 9.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Methodology validation | Annual | Model Risk Committee |
| ICAAP alignment | Quarterly | Finance review |

---

*End of Document*
