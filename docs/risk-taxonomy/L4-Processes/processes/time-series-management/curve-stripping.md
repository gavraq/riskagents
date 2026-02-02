---
# Process Metadata
process_id: MR-L4-005e
process_name: Curve Stripping
version: 1.0
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Reporting, Analysis & Validation (RAV)
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-005  # Time Series Management
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-003  # FRTB
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
l6_models:
  - MR-L6-001   # Historical Simulation VaR
l7_systems:
  - SYS-MR-010  # Time Series Service
  - SYS-MR-013  # Curve Stripping Engine (QT2)
---

# Curve Stripping Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-005e |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Time Series Management (MR-L4-005) |
| **Owner** | Head of Reporting, Analysis & Validation (RAV) |

---

## 1. Purpose

The Curve Stripping process converts market-quoted **par rates** (swap rates, deposit rates, futures prices) into **zero coupon rates** required for Value-at-Risk (VaR) calculations. It also constructs **cross-currency (XCCY) basis curves** from FX forward points. This transformation is essential because:

- VaR models require zero rates for consistent discounting
- Time series returns are calculated on zero rates, not par rates
- Alignment with front office valuation curves ensures VaR captures actual portfolio risk

---

## 2. Scope

### 2.1 Instruments Subject to Stripping

| Instrument Type | Input Format | Output Format |
|-----------------|--------------|---------------|
| **Deposit Rates** | Par rate (e.g., 3M EURIBOR) | Zero rate |
| **Interest Rate Futures** | Futures price | Implied zero rate |
| **Forward Rate Agreements (FRAs)** | FRA rate | Zero rate |
| **Interest Rate Swaps** | Par swap rate | Zero curve (bootstrap) |
| **OIS Swaps** | OIS rate | Zero curve |
| **FX Swap Points** | Forward points | XCCY basis curve |
| **XCCY Basis Swaps** | Basis spread | XCCY zero curve |

### 2.2 Out of Scope

| Item | Reason |
|------|--------|
| **Bond curves** | Use generic bond yields directly (agreed with Market Risk) |
| **Credit CDS curves** | Collected as spreads, not stripped |
| **Volatility surfaces** | No stripping required |
| **Equity/FX spot** | Direct observation, no transformation |

---

## 3. Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           CURVE STRIPPING PROCESS                                        │
│                           (Daily - Post-Validation)                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [From Cleaning & Validation]
              │
              ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    1. INPUT PREPARATION                                                  │
│                                                                                          │
│  For each curve requiring stripping:                                                     │
│  • Gather validated par rate observations                                                │
│  • Load curve configuration (instruments, tenors, conventions)                           │
│  • Verify all required input points available                                            │
│                                                                                          │
│  Missing inputs → flag for proxy or manual intervention                                  │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    2. CURVE STRIPPING ENGINE (QT2)                                       │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                     │ │
│  │   INPUT: Par Rates                        OUTPUT: Zero Rates                        │ │
│  │   ┌─────────────────┐                     ┌─────────────────┐                       │ │
│  │   │ Deposits        │                     │ Continuous zero │                       │ │
│  │   │ 1M: 3.50%       │                     │ rates           │                       │ │
│  │   │ 3M: 3.55%       │ ═══════════════════▶│                 │                       │ │
│  │   │                 │    Bootstrap         │ 1M: 3.4975%     │                       │ │
│  │   │ Swaps           │    Algorithm         │ 3M: 3.5423%     │                       │ │
│  │   │ 1Y: 3.60%       │                     │ 1Y: 3.5812%     │                       │ │
│  │   │ 2Y: 3.65%       │                     │ 2Y: 3.6234%     │                       │ │
│  │   │ 5Y: 3.70%       │                     │ 5Y: 3.6678%     │                       │ │
│  │   │ 10Y: 3.75%      │                     │ 10Y: 3.7089%    │                       │ │
│  │   └─────────────────┘                     └─────────────────┘                       │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  Configuration includes:                                                                 │
│  • Day count conventions (ACT/360, ACT/365, 30/360)                                      │
│  • Compounding frequency (annual, semi-annual, continuous)                               │
│  • Settlement conventions (T+0, T+1, T+2)                                                │
│  • Interpolation method (linear, cubic spline, log-linear)                               │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    3. XCCY CURVE CONSTRUCTION                                            │
│                                                                                          │
│  For cross-currency curves:                                                              │
│                                                                                          │
│   FX Forward Points              Interest Rate                  XCCY Zero Curve          │
│   ┌─────────────────┐           Differential                   ┌─────────────────┐      │
│   │ EUR/USD 1M: -12 │    +     ┌─────────────────┐            │ EUR/USD XCCY     │      │
│   │ EUR/USD 3M: -35 │ ═════════│ USD Zero - EUR  │ ══════════▶│ Zero Curve       │      │
│   │ EUR/USD 6M: -68 │          │ Zero            │            │                  │      │
│   │ EUR/USD 1Y: -125│          └─────────────────┘            └─────────────────┘      │
│   └─────────────────┘                                                                   │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    4. VALIDATION                                                         │
│                                                                                          │
│  • Reasonableness checks on output zero rates                                            │
│  • Comparison to previous day (spike detection on zeros)                                 │
│  • Alignment check vs. front office valuation curves                                     │
│  • Forward rate positivity check (no-arbitrage)                                          │
│                                                                                          │
│  Validation failures → exception queue                                                   │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    5. OUTPUT                                                             │
│                                                                                          │
│  • Store zero rate curves in Time Series ODS                                             │
│  • Calculate returns (1-day, 10-day for FRTB liquidity horizons)                         │
│  • Publish to Risk Engine                                                                │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                                [To Time Series Construction / Risk Engine]
```

---

## 4. Stripping Methodologies

### 4.1 Bootstrap Algorithm

The standard approach for constructing zero curves from par instruments:

**Step 1: Short End (Deposits)**
```
Zero_Rate = Par_Rate  (for deposits with single payment)
Discount_Factor = 1 / (1 + Zero_Rate × DayCountFraction)
```

**Step 2: Medium/Long End (Swaps)**
```
For each swap tenor, solve for zero rate such that:
PV(Fixed Leg) = PV(Floating Leg)

Where floating leg PV = 1 (at par)
And fixed leg PV = Σ (Coupon × DF_i) + Notional × DF_n
```

**Step 3: Interpolation**
- **Between known points**: Cubic spline on zero rates
- **Extrapolation beyond longest point**: Flat extrapolation

### 4.2 XCCY Curve Construction

Cross-currency zero curves are derived from:
1. Domestic zero curve (e.g., USD OIS)
2. Foreign zero curve (e.g., EUR OIS)
3. FX forward points

**Methodology**:
```
XCCY_Zero_Rate = Domestic_Zero + Implied_FX_Basis

Where Implied_FX_Basis derived from:
Forward_Rate = Spot × exp[(Domestic_Zero - Foreign_Zero + Basis) × T]
```

### 4.3 Configuration Parameters

| Parameter | Description | Source |
|-----------|-------------|--------|
| `curve_id` | Unique curve identifier | Risk Factor Setup |
| `instruments` | List of input instruments by tenor | Market Data ODS |
| `day_count` | Day count convention | Aligned to front office |
| `compounding` | Compounding frequency | Aligned to front office |
| `settlement` | Settlement convention | Market standard |
| `interpolation` | Interpolation method | RMA approved |
| `extrapolation` | Extrapolation method | RMA approved |

---

## 5. Alignment with Front Office

### 5.1 Consistency Requirement

Curve stripping parameters must be **consistent with front office valuation curves** to ensure VaR captures actual portfolio risk. This means:

- Same instruments used for curve construction
- Same day count and compounding conventions
- Same interpolation methods
- Same settlement conventions

### 5.2 Configuration Governance

| Activity | Owner | Approval |
|----------|-------|----------|
| Initial curve configuration | RAV | RMA |
| Parameter changes | RAV | RMA + Market Risk |
| New curve addition | RAV | RMA (MLRC for material) |

### 5.3 Alignment Verification

Monthly reconciliation between:
- Time Series Service curve configurations
- Front Office valuation curve configurations (from Trading Systems)

Discrepancies documented and resolved or captured in RniV.

---

## 6. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| CS-C01 | All input par rates must pass validation before stripping | Preventive | RAV |
| CS-C02 | Curve configuration aligned with front office | Preventive | RMA |
| CS-C03 | Output zero rates validated (no-arbitrage, reasonableness) | Detective | RAV |
| CS-C04 | Stripping failures logged and investigated | Detective | RAV |
| CS-C05 | Monthly alignment check vs. front office | Detective | RAV + MR |
| CS-C06 | Configuration changes require RMA approval | Preventive | RMA |

---

## 7. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| Stripping batch complete | 20:30 GMT | 21:00 GMT | RAV Manager |
| Stripping success rate | 100% | 99% | RAV Team Lead |
| Alignment validation pass | 100% | 98% | RMA |

---

## 8. Exception Handling

### 8.1 Stripping Failures

| Failure Type | Cause | Resolution |
|--------------|-------|------------|
| **Missing input** | Par rate not collected | Use proxy or previous day |
| **Bootstrap failure** | Numerical instability | Review input data quality |
| **Arbitrage violation** | Forward rates negative | Investigate input; may need adjustment |
| **Alignment failure** | Differs from front office | Investigate configuration |

### 8.2 Escalation Path

1. **RAV Analyst**: First-line investigation
2. **RAV Manager**: If not resolved in 30 minutes
3. **RMA**: If methodology issue suspected
4. **Market Risk**: If material impact on VaR

---

## 9. Phased Implementation

Meridian Global Bank implements curve stripping in phases:

### Phase 1 (Current)
- OIS curves (discounting)
- Major swap curves (projection)
- Key XCCY basis curves

### Phase 2 (Planned)
- IR Futures integration
- FRA curves
- Tenor basis curves
- Full alignment with all front office curves

---

## 10. Related Documents

| Document | Relationship |
|----------|--------------|
| [Time Series Management](./time-series-overview.md) | Parent process |
| [Risk Factor Setup](./risk-factor-setup.md) | Provides curve definitions |
| [Cleaning & Validation](./cleaning-validation.md) | Upstream - provides validated par rates |
| [Proxying Process](./proxying-process.md) | Related - handles missing inputs |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |

---

*End of Document*
