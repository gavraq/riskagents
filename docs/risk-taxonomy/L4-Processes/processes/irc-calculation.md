---
# Process Metadata
process_id: MR-L4-010
process_name: Incremental Risk Charge (IRC) Calculation
version: 1.0
effective_date: 2025-01-16
next_review_date: 2026-01-16
owner: Head of Risk Methodology & Analytics (RMA)
approving_committee: MLRC

# Taxonomy Linkages
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-003  # FRTB
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-002   # MLRC Terms of Reference
l4_related_processes:
  - MR-L4-001   # Market Risk Process Orchestration
  - MR-L4-006   # Risk Engine Calculation
l5_controls:
  - MR-L5-001   # VaR and SVaR Limits
l6_models:
  - MR-L6-002   # IRC Model (this document defines requirements)
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-001  # Murex (FO System)
---

# Incremental Risk Charge (IRC) Calculation Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-010 |
| **Version** | 1.0 |
| **Effective Date** | 16 January 2025 |
| **Owner** | Head of Risk Methodology & Analytics (RMA) |

---

## 1. Purpose

The Incremental Risk Charge (IRC) process captures default and migration risk for credit-sensitive positions in the trading book that are not adequately captured by the VaR model. This document describes the end-to-end process for calculating, validating, and reporting IRC.

---

## 2. Regulatory Context

### 2.1 Regulatory Basis

| Regulation | Article | Requirement |
|------------|---------|-------------|
| **CRR** | Article 325bi | IRC for trading book positions subject to default and migration risk |
| **CRR** | Article 325bj | IRC model requirements |
| **PRA Rulebook** | Market Risk Chapter | IMA permission conditions for IRC |

### 2.2 Scope of IRC

IRC applies to positions where:
- Default risk is material
- Migration risk (rating change) is material
- VaR does not adequately capture the full risk

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           IRC SCOPE                                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  IN-SCOPE POSITIONS:                                                                    │
│  ──────────────────                                                                     │
│  • Corporate bonds                                                                      │
│  • Credit default swaps (CDS)                                                           │
│  • Credit indices (iTraxx, CDX)                                                         │
│  • Sovereign bonds (non-G10 and lower-rated G10)                                        │
│  • Loan positions in trading book                                                       │
│  • Credit-linked notes                                                                  │
│  • Total return swaps on credit                                                         │
│                                                                                         │
│  OUT-OF-SCOPE POSITIONS:                                                                │
│  ────────────────────────                                                               │
│  • G10 sovereign bonds (AAA/AA rated)                                                   │
│  • Interest rate products without credit risk                                           │
│  • FX positions                                                                         │
│  • Equity positions (covered by separate equity risk charge)                            │
│  • Commodity positions                                                                  │
│  • Securitisation positions (subject to separate treatment)                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. IRC Model Overview

### 3.1 Methodology Summary

The IRC model uses a Monte Carlo simulation approach to capture:
- **Default risk**: Probability of issuer default over 1-year horizon
- **Migration risk**: Probability of rating changes and associated P&L impact
- **Liquidity horizon**: Position-specific holding periods (minimum 3 months)

### 3.2 Key Model Parameters

| Parameter | Description | Source |
|-----------|-------------|--------|
| **Probability of Default (PD)** | 1-year default probability by rating | Credit Risk / External ratings |
| **Transition Matrix** | Rating migration probabilities | Historical analysis / S&P/Moody's |
| **Loss Given Default (LGD)** | Recovery rate assumptions | Credit Risk policy |
| **Correlation** | Inter-obligor default correlation | Model calibration |
| **Liquidity Horizon** | Position-specific holding period | Market Risk assessment |

### 3.3 Confidence Level and Horizon

| Parameter | Regulatory Requirement | Meridian Setting |
|-----------|------------------------|------------------|
| **Confidence Level** | 99.9% | 99.9% |
| **Capital Horizon** | 1 year | 1 year |
| **Minimum Liquidity Horizon** | 3 months | 3 months |
| **Simulations** | Sufficient for convergence | 100,000 |

---

## 4. Process Flow

### 4.1 High-Level Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           IRC CALCULATION PROCESS                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         1. POSITION EXTRACTION                                           │
│                                                                                          │
│  • Extract credit-sensitive trading book positions from Murex                            │
│  • Identify IRC-eligible positions based on product type                                 │
│  • Map positions to issuers                                                              │
│  • Determine liquidity horizons                                                          │
│                                                                                          │
│  Systems: Murex → Trade ODS                                                              │
│  Timing: EOD (18:30)                                                                     │
│  Owner: Risk Operations                                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         2. ISSUER DATA ENRICHMENT                                        │
│                                                                                          │
│  • Retrieve issuer ratings (S&P, Moody's, Fitch)                                         │
│  • Apply internal rating where external not available                                    │
│  • Source PD curves from Credit Risk                                                     │
│  • Retrieve LGD assumptions                                                              │
│  • Flag any missing issuer data                                                          │
│                                                                                          │
│  Systems: Credit Risk Systems → Trade ODS                                                │
│  Timing: EOD (19:00)                                                                     │
│  Owner: Credit Risk / Risk Operations                                                    │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         3. STRESS GRID GENERATION                                        │
│                                                                                          │
│  For each IRC-eligible position, Front Office systems calculate:                         │
│  • Full revaluation P&L under credit spread stress scenarios                             │
│  • Default scenario P&L (LGD-based)                                                      │
│  • Rating migration scenario P&L (spread widening/tightening)                            │
│                                                                                          │
│  Systems: Murex → IRC Calculation Engine                                                 │
│  Timing: EOD (20:00)                                                                     │
│  Owner: Front Office Quants / Risk Technology                                            │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         4. IRC MONTE CARLO SIMULATION                                    │
│                                                                                          │
│  IRC Engine performs:                                                                    │
│  • Generate correlated default/migration scenarios (100,000 paths)                       │
│  • For each path, simulate rating changes and defaults                                   │
│  • Calculate portfolio P&L for each path                                                 │
│  • Apply liquidity horizon adjustments                                                   │
│  • Determine 99.9th percentile loss                                                      │
│                                                                                          │
│  Systems: IRC Calculation Engine                                                         │
│  Timing: EOD (22:00 - 02:00)                                                             │
│  Owner: Risk Technology                                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         5. RESULTS VALIDATION                                            │
│                                                                                          │
│  • Reasonableness checks vs. prior day (±50% threshold)                                  │
│  • Reconcile position count to source system                                             │
│  • Verify issuer coverage (no missing ratings)                                           │
│  • Check simulation convergence                                                          │
│                                                                                          │
│  Systems: Risk ODS                                                                       │
│  Timing: T+1 (04:00)                                                                     │
│  Owner: RMA                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         6. SIGN-OFF AND REPORTING                                        │
│                                                                                          │
│  • IRC results signed off by RMA                                                         │
│  • Results published to Risk Reporting DataMart                                          │
│  • Capital feed sent to Regulatory Capital system                                        │
│  • MLRC pack updated                                                                     │
│                                                                                          │
│  Systems: Risk DataMart → Capital System                                                 │
│  Timing: T+1 (06:00)                                                                     │
│  Owner: RMA / Risk Reporting                                                             │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Detailed Swimlane Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    IRC PROCESS - SWIMLANE VIEW                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  FRONT OFFICE                                                                           │
│  ────────────                                                                           │
│  │                                                                                      │
│  │  ┌───────────────┐     ┌───────────────────────┐                                     │
│  │  │ Trade booking │────▶│ Position snapshot     │                                     │
│  │  │ (intraday)    │     │ extracted to Trade ODS│                                     │
│  │  └───────────────┘     └───────────┬───────────┘                                     │
│  │                                    │                                                 │
│  │                                    ▼                                                 │
│  │                        ┌───────────────────────┐                                     │
│  │                        │ FO systems calculate  │                                     │
│  │                        │ stress grid (full     │                                     │
│  │                        │ revaluation)          │                                     │
│  │                        └───────────┬───────────┘                                     │
│  │                                    │                                                 │
│  ├────────────────────────────────────┼─────────────────────────────────────────────────│
│  │                                    │                                                 │
│  CREDIT RISK                          │                                                 │
│  ───────────                          │                                                 │
│  │                                    │                                                 │
│  │  ┌───────────────────────┐         │                                                 │
│  │  │ Provide PD curves,    │─────────┤                                                 │
│  │  │ LGD assumptions,      │         │                                                 │
│  │  │ issuer ratings        │         │                                                 │
│  │  └───────────────────────┘         │                                                 │
│  │                                    │                                                 │
│  ├────────────────────────────────────┼─────────────────────────────────────────────────│
│  │                                    │                                                 │
│  RISK TECHNOLOGY                      ▼                                                 │
│  ───────────────      ┌───────────────────────────────┐                                 │
│  │                    │ IRC Engine: Monte Carlo       │                                 │
│  │                    │ simulation (100k paths)       │                                 │
│  │                    │ • Default scenarios           │                                 │
│  │                    │ • Migration scenarios         │                                 │
│  │                    │ • Correlation structure       │                                 │
│  │                    └───────────────┬───────────────┘                                 │
│  │                                    │                                                 │
│  │                                    ▼                                                 │
│  │                    ┌───────────────────────────────┐                                 │
│  │                    │ Publish results to Risk ODS   │                                 │
│  │                    └───────────────┬───────────────┘                                 │
│  │                                    │                                                 │
│  ├────────────────────────────────────┼─────────────────────────────────────────────────│
│  │                                    │                                                 │
│  MARKET RISK (RMA)                    ▼                                                 │
│  ─────────────────    ┌───────────────────────────────┐                                 │
│  │                    │ Validate IRC results:         │                                 │
│  │                    │ • Reasonableness checks       │                                 │
│  │                    │ • Position reconciliation     │                                 │
│  │                    │ • Issuer coverage             │                                 │
│  │                    └───────────────┬───────────────┘                                 │
│  │                                    │                                                 │
│  │                                    ▼                                                 │
│  │                    ┌───────────────────────────────┐     ┌───────────────────────┐   │
│  │                    │ Sign-off IRC                  │────▶│ Publish to Capital    │   │
│  │                    │                               │     │ and MLRC reporting    │   │
│  │                    └───────────────────────────────┘     └───────────────────────┘   │
│  │                                                                                      │
│  ├──────────────────────────────────────────────────────────────────────────────────────│
│  │                                                                                      │
│  MLRC                                                                                   │
│  ────                                                                                   │
│  │                                                          ┌───────────────────────┐   │
│  │                                                          │ Review IRC in monthly │   │
│  │                                                          │ MLRC pack             │   │
│  │                                                          └───────────────────────┘   │
│  │                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Input Data Requirements

### 5.1 Position Data

| Data Element | Source | Frequency | Validation |
|--------------|--------|-----------|------------|
| Trade ID | Murex | EOD | Completeness check |
| Position (notional) | Murex | EOD | Sign check |
| Issuer ID | Murex / Security Master | EOD | Mapping validation |
| Product type | Murex | EOD | IRC eligibility |
| Maturity date | Murex | EOD | Plausibility |
| Currency | Murex | EOD | Valid ISO code |

### 5.2 Issuer Data

| Data Element | Source | Frequency | Validation |
|--------------|--------|-----------|------------|
| External rating (S&P) | Bloomberg | Daily | Rating valid |
| External rating (Moody's) | Bloomberg | Daily | Rating valid |
| Internal rating | Credit Risk | Daily | Within range |
| PD curve | Credit Risk | Monthly | Non-negative |
| LGD assumption | Credit Risk | Quarterly | 0-100% |
| Industry sector | Security Master | Static | Valid sector |
| Country | Security Master | Static | Valid ISO |

### 5.3 Market Data

| Data Element | Source | Frequency | Validation |
|--------------|--------|-----------|------------|
| Credit spreads | Bloomberg/Reuters | EOD | Non-negative |
| Recovery rates | Markit | Daily | 0-100% |
| Transition matrices | Internal calibration | Quarterly | Row sums = 1 |

---

## 6. Liquidity Horizon Framework

### 6.1 Liquidity Horizon Determination

Positions are assigned liquidity horizons based on market liquidity and position size:

| Liquidity Category | Horizon | Criteria |
|-------------------|---------|----------|
| **Highly Liquid** | 3 months | Investment grade; large issue size; active CDS market |
| **Liquid** | 6 months | Investment grade; medium issue size |
| **Less Liquid** | 9 months | High yield; smaller issue size |
| **Illiquid** | 12 months | Distressed; no active market |

### 6.2 Concentration Adjustment

For concentrated positions (>10% of daily trading volume), liquidity horizon is extended:

```
Adjusted_Horizon = Base_Horizon × (1 + Position_Size / Daily_Volume × 0.1)
```

---

## 7. Validation and Controls

### 7.1 Daily Validation Checks

| Check ID | Check | Threshold | Action if Failed |
|----------|-------|-----------|------------------|
| IRC-V01 | Day-on-day IRC change | ±50% | Investigate; escalate if unexplained |
| IRC-V02 | Position count reconciliation | 100% match | Hold results until resolved |
| IRC-V03 | Issuer coverage | 100% rated | Apply conservative proxy |
| IRC-V04 | Simulation convergence | <2% variation | Increase simulations |
| IRC-V05 | Negative IRC | Must be positive | Investigate model issue |

### 7.2 Monthly Validation

| Check | Owner | Deliverable |
|-------|-------|-------------|
| Top 10 issuer contributors | RMA | Concentration report |
| IRC vs. VaR credit component | RMA | Reasonableness analysis |
| Rating migration actual vs. model | Model Validation | Back-testing report |

### 7.3 Annual Validation

| Activity | Owner | Timing |
|----------|-------|--------|
| Full IRC model validation | Model Risk | Annual |
| Transition matrix recalibration | RMA | Annual |
| LGD assumption review | Credit Risk | Annual |
| Correlation parameter review | RMA | Annual |

---

## 8. Reporting

### 8.1 Daily Reports

| Report | Audience | Content |
|--------|----------|---------|
| IRC Summary | MLRC, CRO | Total IRC, day-on-day change |
| IRC by Desk | Trading Desks | IRC allocation by desk |
| Top Issuer Exposures | Market Risk | Top 20 issuer IRC contributors |

### 8.2 Monthly Reports

| Report | Audience | Content |
|--------|----------|---------|
| IRC Trend Analysis | MLRC | 12-month IRC trend |
| IRC vs. Credit VaR | MLRC | Comparison and explanation |
| IRC Concentration | MLRC | Issuer and sector concentration |

### 8.3 Regulatory Reporting

| Report | Frequency | Submission |
|--------|-----------|------------|
| COREP C24.00 | Quarterly | IRC capital requirement |
| IMA Questionnaire | Annual | IRC model description |

---

## 9. System Dependencies

### 9.1 System Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│   Murex     │────▶│  Trade ODS  │────▶│  IRC Calculation│────▶│  Risk ODS   │
│  (Positions)│     │             │     │     Engine      │     │             │
└─────────────┘     └─────────────┘     └─────────────────┘     └─────────────┘
                                               │
                                               │
┌─────────────┐     ┌─────────────┐            │
│  Credit     │────▶│  Issuer     │────────────┘
│  Risk       │     │  Data       │
└─────────────┘     └─────────────┘
```

### 9.2 System SLAs

| System | Data | SLA | Criticality |
|--------|------|-----|-------------|
| Murex | Positions | 18:30 | Critical |
| Credit Risk | PD/LGD | 19:00 | Critical |
| Murex | Stress grid | 20:00 | Critical |
| IRC Engine | IRC results | 02:00+1 | Critical |

---

## 10. Exception Handling

### 10.1 Missing Data

| Scenario | Treatment | Escalation |
|----------|-----------|------------|
| Missing issuer rating | Use internal rating; apply 1-notch conservative adjustment | Report to MLRC |
| Missing PD curve | Use generic rating-based PD | Report to Credit Risk |
| Missing position | Exclude with documented rationale | Escalate to Risk Ops |

### 10.2 System Failure

| Scenario | Fallback | Authority |
|----------|----------|-----------|
| IRC Engine failure | Use T-1 IRC + 20% buffer | Head of RMA |
| Stress grid not received | Delay IRC; escalate to FO Quants | Head of RMA |
| Credit data not received | Use T-1 credit data | Head of RMA + Credit Risk |

---

## 11. Governance

### 11.1 Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| **Front Office** | Position accuracy; stress grid generation |
| **Credit Risk** | PD curves; LGD assumptions; issuer ratings |
| **Risk Technology** | IRC Engine operation; system availability |
| **RMA** | IRC validation; sign-off; methodology |
| **Model Validation** | Independent model validation |
| **MLRC** | Oversight; limit approval |

### 11.2 Approval Authority

| Activity | Approver |
|----------|----------|
| IRC methodology changes | MLRC |
| Transition matrix updates | RMA Head |
| LGD assumption changes | Credit Risk + RMA |
| Liquidity horizon changes | RMA Head |
| IRC limit changes | MLRC |

---

## 12. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration process |
| [VaR/SVaR Methodology](../L6-Models/market-risk/var-svar-methodology.md) | Related model documentation |
| [Market Risk Reporting and Sign-off](./market-risk-reporting-signoff.md) | Sign-off process |
| [System Architecture](../L7-Systems/market-risk/system-architecture.md) | System specifications |
| [Regulatory Reporting](./regulatory-reporting.md) | COREP submission |

---

## 13. Document Control

### 13.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-16 | Initial version - separated from VaR process | MLRC |

### 13.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Model validation | Annual | Per Model Risk schedule |
| Parameter review | Quarterly | April 2025 |

---

*End of Document*
