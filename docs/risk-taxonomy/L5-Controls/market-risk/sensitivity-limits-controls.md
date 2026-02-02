---
# Control Metadata
control_id: MR-L5-003
control_name: Sensitivity Limits Controls
version: 1.0
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Market Risk
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-013  # Market Risk Limits Management
parent_framework: MR-L3-003  # VaR Limit Framework
l1_requirements:
  - REQ-L1-001  # CRR (UK)
  - REQ-L1-003  # FRTB
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-003   # VaR Limit Framework
l4_processes:
  - MR-L4-007   # Market Risk Reporting and Sign-off
  - MR-L4-013   # Market Risk Limits Management
l6_models:
  - MR-L6-004   # Sensitivity Calculation Models
l7_systems:
  - SYS-MR-003  # Murex (Front Office)
  - SYS-MR-001  # Risk Engine (FMDM)
---

# Sensitivity Limits Controls

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Control ID** | MR-L5-003 |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Framework** | VaR Limit Framework (MR-L3-003) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

This document defines the controls for monitoring and managing sensitivity limits (Greeks). Sensitivity limits provide granular control over specific risk factors that may not be fully captured by VaR, enabling early identification of concentrated or outsized risk factor exposures.

---

## 2. Scope

### 2.1 Sensitivity Measures Covered

| Sensitivity | Symbol | Definition | Unit |
|-------------|--------|------------|------|
| **DV01** | δV/δr | P&L change for 1bp parallel rate move | $ per bp |
| **CS01** | δV/δcs | P&L change for 1bp credit spread move | $ per bp |
| **Vega** | δV/δσ | P&L change for 1% volatility move | $ per % vol |
| **FX Delta** | δV/δFX | P&L change for 1% spot FX move | $ per % |
| **Equity Delta** | δV/δEq | P&L change for 1% equity index move | $ per % |
| **Gamma** | δ²V/δS² | Rate of change of delta | $ per %² |
| **Theta** | δV/δt | Time decay per day | $ per day |

### 2.2 Entity-Level Sensitivity Limits

| Sensitivity | Metric | Entity Limit |
|-------------|--------|--------------|
| **DV01** | $/bp | $500,000 |
| **CS01** | $/bp | $300,000 |
| **Vega** | $/%vol | $200,000 |
| **FX Delta** | $/% | $5,000,000 |
| **Equity Delta** | $/% | $2,000,000 |

### 2.3 Tenor Bucket Limits (DV01)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  DV01 LIMITS BY TENOR BUCKET (Entity Level)                                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│     Tenor          │    Limit ($k/bp)   │    Warning ($k/bp)                            │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│     0-3M           │        100         │         80                                    │
│     3M-1Y          │        150         │        120                                    │
│     1Y-5Y          │        150         │        120                                    │
│     5Y-10Y         │         75         │         60                                    │
│     10Y+           │         25         │         20                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│     TOTAL          │        500         │        400                                    │
│                                                                                         │
│  Note: Sub-limits may exceed total due to assumed diversification                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.4 Rating Bucket Limits (CS01)

| Rating Bucket | Limit ($k/bp) | Warning ($k/bp) |
|---------------|---------------|-----------------|
| IG (A- and above) | 150 | 120 |
| IG (BBB) | 100 | 80 |
| HY (BB) | 40 | 32 |
| HY (B and below) | 10 | 8 |
| **Total** | **300** | **240** |

---

## 3. Control Objectives

| Objective ID | Objective | Risk Mitigated |
|--------------|-----------|----------------|
| **CO-01** | Sensitivity limits are monitored intraday | Undetected concentrated exposures |
| **CO-02** | Tenor/rating bucket limits prevent curve risk concentration | Duration or credit curve risk |
| **CO-03** | Greeks are calculated consistently across systems | Calculation errors |
| **CO-04** | Breaches are escalated with appropriate urgency | Delayed response to excess exposure |
| **CO-05** | Sensitivity trends inform trading strategy | Drift into concentrated positions |

---

## 4. Control Inventory

### 4.1 Control Summary

| Control ID | Control Name | Type | Frequency | Owner |
|------------|--------------|------|-----------|-------|
| SE-C01 | Intraday Sensitivity Monitoring | Detective | Hourly | Trading / RAV |
| SE-C02 | Sensitivity Warning Alert | Detective | On threshold | Trading / Market Risk |
| SE-C03 | Sensitivity Breach Escalation | Responsive | On breach | Trading / Market Risk |
| SE-C04 | End-of-Day Sensitivity Report | Detective | Daily | RAV |
| SE-C05 | Tenor Bucket Limit Monitoring | Detective | Daily | Market Risk |
| SE-C06 | Rating Bucket Limit Monitoring | Detective | Daily | Market Risk |
| SE-C07 | Sensitivity Reconciliation (FO vs Risk) | Detective | Daily | RAV |
| SE-C08 | Large Trade Sensitivity Pre-Check | Preventive | Per trade | Trading |
| SE-C09 | MLRC Sensitivity Dashboard Review | Detective | Weekly | MLRC |
| SE-C10 | Sensitivity Limit Configuration Validation | Preventive | On change | Risk Technology |

---

## 5. Control Details

### 5.1 SE-C01: Intraday Sensitivity Monitoring

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: SE-C01 - Intraday Sensitivity Monitoring                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Monitor sensitivities in near-real-time to enable proactive management      │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Hourly (10:00, 11:00, 12:00, 14:00, 15:00, 16:00)                           │
│  OWNER: Trading (primary) / RAV (oversight)                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  DATA FLOW:                                                                             │
│                                                                                         │
│       ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                        │
│       │   Murex FO   │────▶│  Risk Engine │────▶│  Dashboard   │                        │
│       │  (Positions) │     │    (FMDM)    │     │  (Real-time) │                        │
│       └──────────────┘     └──────────────┘     └──────────────┘                        │
│              │                    │                    │                                │
│              │              Sensitivity                │                                │
│              │              Calculation               Alert                             │
│              │                    │               Notification                          │
│              ▼                    ▼                    ▼                                │
│       Trade Capture        Greeks: DV01,         Traffic Light                          │
│       System               CS01, Vega,           Status                                 │
│                            Delta, Gamma                                                 │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CONTROL ACTIVITIES:                                                                    │
│  1. Hourly position snapshot extracted from Murex                                       │
│  2. Risk Engine calculates sensitivities by:                                            │
│     • Desk                                                                              │
│     • Risk factor                                                                       │
│     • Tenor bucket (for rates)                                                          │
│     • Rating bucket (for credit)                                                        │
│  3. Compare to limits and generate traffic light status                                 │
│  4. Dashboard updated and auto-refreshed                                                │
│  5. Trading desks responsible for monitoring their positions                            │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Intraday sensitivity snapshots (retained 90 days)                                    │
│  • Dashboard access logs                                                                │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 SE-C02: Sensitivity Warning Alert

| Attribute | Value |
|-----------|-------|
| **Control ID** | SE-C02 |
| **Objective** | Alert traders and risk when approaching sensitivity limits |
| **Type** | Detective |
| **Frequency** | On threshold breach (80%) |
| **Owner** | Trading / Market Risk |

**Control Activities**:
1. System generates automatic alert when sensitivity reaches 80% of limit
2. Alert sent to:
   - Desk Head
   - Trading Operations
   - Market Risk Monitoring
3. Alert includes:
   - Current sensitivity value
   - Limit value
   - Utilisation %
   - Top contributing positions
4. Trader must acknowledge alert in system

**Evidence**:
- Alert notification (email/Bloomberg message)
- System acknowledgement log

### 5.3 SE-C03: Sensitivity Breach Escalation

| Attribute | Value |
|-----------|-------|
| **Control ID** | SE-C03 |
| **Objective** | Escalate sensitivity breaches for immediate action |
| **Type** | Responsive |
| **Frequency** | On breach |
| **Owner** | Trading / Market Risk |

**Escalation Matrix**:

| Breach Level | Escalate To | Timeline | Action Required |
|--------------|-------------|----------|-----------------|
| Desk limit | Desk Head + Market Risk | Immediate | Reduce position or hedge |
| BU limit | BU Head + MLRC Chair | 30 minutes | Risk reduction plan |
| Entity limit | CRO + Trading Head | 15 minutes | Immediate position reduction |

**Key Difference from VaR Breaches**:
- Sensitivity breaches are more immediately actionable
- Trading can typically reduce exposure quickly via hedging
- Breaches due to market moves (passive) vs new trades (active) same treatment

**Evidence**:
- Escalation notification
- Position reduction confirmation
- Breach Register entry

### 5.4 SE-C04: End-of-Day Sensitivity Report

| Attribute | Value |
|-----------|-------|
| **Control ID** | SE-C04 |
| **Objective** | Official daily record of sensitivity positions |
| **Type** | Detective |
| **Frequency** | Daily (by 19:00) |
| **Owner** | RAV |

**Control Activities**:
1. Final sensitivity calculation on COB positions
2. Report includes:
   - All sensitivity measures by desk/BU/division/entity
   - Limit utilisation percentages
   - Daily change analysis
   - Top 10 positions by each sensitivity
3. Published to SharePoint and distributed to Trading, Market Risk, MLRC
4. Archived for regulatory/audit purposes

**Evidence**:
- Daily Sensitivity Report
- SharePoint publication timestamp

### 5.5 SE-C05: Tenor Bucket Limit Monitoring

| Attribute | Value |
|-----------|-------|
| **Control ID** | SE-C05 |
| **Objective** | Prevent concentration of interest rate risk in specific tenors |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | Market Risk |

**Control Activities**:
1. Calculate DV01 by tenor bucket (0-3M, 3M-1Y, 1Y-5Y, 5Y-10Y, 10Y+)
2. Compare to tenor bucket limits
3. Identify:
   - Bucket breaches
   - Curve shape risks (steep/flat positioning)
   - Basis risks between curves
4. Flag concerns to MLRC

**Evidence**:
- Tenor bucket analysis in Daily Sensitivity Report
- Curve risk commentary

### 5.6 SE-C06: Rating Bucket Limit Monitoring

| Attribute | Value |
|-----------|-------|
| **Control ID** | SE-C06 |
| **Objective** | Prevent concentration of credit spread risk in specific ratings |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | Market Risk |

**Control Activities**:
1. Calculate CS01 by rating bucket (IG A-/above, IG BBB, HY BB, HY B/below)
2. Compare to rating bucket limits
3. Identify:
   - Bucket breaches
   - Migration risk (positions near rating boundaries)
   - Sector concentrations within buckets
4. Flag concerns to MLRC

**Evidence**:
- Rating bucket analysis in Daily Sensitivity Report
- Credit concentration commentary

### 5.7 SE-C07: Sensitivity Reconciliation (FO vs Risk)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: SE-C07 - Sensitivity Reconciliation (Front Office vs Risk)                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Ensure sensitivities calculated by FO and Risk systems are consistent       │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Daily                                                                       │
│  OWNER: RAV                                                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  RECONCILIATION POINTS:                                                                 │
│                                                                                         │
│       ┌────────────────┐              ┌────────────────┐                                │
│       │   MUREX (FO)   │◄────────────▶│   FMDM (Risk)  │                                │
│       │                │   Compare    │                │                                │
│       │  DV01: $485k   │◄────────────▶│  DV01: $482k   │                                │
│       │  CS01: $290k   │              │  CS01: $288k   │                                │
│       │  Vega: $195k   │              │  Vega: $192k   │                                │
│       └────────────────┘              └────────────────┘                                │
│                                                                                         │
│  TOLERANCE THRESHOLDS:                                                                  │
│  • DV01: ±2% or $5k (whichever greater)                                                 │
│  • CS01: ±2% or $3k                                                                     │
│  • Vega: ±3% or $5k                                                                     │
│  • Delta: ±2% or $50k                                                                   │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CONTROL ACTIVITIES:                                                                    │
│  1. Extract COB sensitivities from both systems                                         │
│  2. Compare at desk level for each sensitivity type                                     │
│  3. Identify breaks outside tolerance                                                   │
│  4. Investigate root cause:                                                             │
│     • Position differences                                                              │
│     • Pricing model differences                                                         │
│     • Market data differences                                                           │
│     • Calculation methodology differences                                               │
│  5. Log break and resolution                                                            │
│  6. Escalate unresolved breaks to Head of RAV                                           │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Daily Reconciliation Report                                                          │
│  • Break investigation log                                                              │
│  • Resolution documentation                                                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.8 SE-C08: Large Trade Sensitivity Pre-Check

| Attribute | Value |
|-----------|-------|
| **Control ID** | SE-C08 |
| **Objective** | Prevent trades that would cause immediate sensitivity breach |
| **Type** | Preventive |
| **Frequency** | Per trade (threshold trades only) |
| **Owner** | Trading |

**Control Activities**:
1. For trades exceeding threshold size:
   - DV01 impact > $20k
   - CS01 impact > $10k
   - Vega impact > $10k
2. Pre-trade sensitivity check required
3. System calculates post-trade sensitivity position
4. If breach would result:
   - Alert displayed to trader
   - Trade requires senior approval (Desk Head or above)
   - Market Risk notification
5. Approval documented in trade record

**Evidence**:
- Pre-trade check system log
- Override approval (if applicable)

### 5.9 SE-C09: MLRC Sensitivity Dashboard Review

| Attribute | Value |
|-----------|-------|
| **Control ID** | SE-C09 |
| **Objective** | Governance oversight of sensitivity risk management |
| **Type** | Detective |
| **Frequency** | Weekly |
| **Owner** | MLRC |

**Control Activities**:
1. Market Risk presents sensitivity dashboard to MLRC
2. Review includes:
   - Entity-level sensitivities vs limits
   - Tenor/rating bucket analysis
   - Trend analysis (4-week)
   - Breaches in period
   - Reconciliation break summary
3. MLRC challenges positions and approves actions
4. Decisions minuted

**Evidence**:
- MLRC agenda and pack
- MLRC minutes

### 5.10 SE-C10: Sensitivity Limit Configuration Validation

| Attribute | Value |
|-----------|-------|
| **Control ID** | SE-C10 |
| **Objective** | Ensure sensitivity limit changes are correctly implemented |
| **Type** | Preventive |
| **Frequency** | On change |
| **Owner** | Risk Technology |

**Control Activities**:
1. Limit change request received from Market Risk
2. Four-eyes review of configuration change
3. Implement in TEST environment
4. RAV validates in TEST:
   - Limit values correct
   - Warning thresholds correct (80%)
   - Alert routing correct
5. Promote to PRODUCTION
6. RAV confirms PRODUCTION configuration

**Evidence**:
- Change Request ticket
- TEST validation sign-off
- PRODUCTION confirmation

---

## 6. Control Testing Schedule

| Control | Test Frequency | Test Type | Tester |
|---------|---------------|-----------|--------|
| SE-C01 | Monthly | System check | Risk Technology |
| SE-C02 | Quarterly | Alert test | Market Risk |
| SE-C03 | Semi-annually | Scenario test | Operational Risk |
| SE-C04 | Monthly | Sample review | Internal Audit |
| SE-C05 | Quarterly | Sample testing | Market Risk |
| SE-C06 | Quarterly | Sample testing | Market Risk |
| SE-C07 | Monthly | Full reconciliation | RAV |
| SE-C08 | Quarterly | Trade simulation | Trading / Risk |
| SE-C09 | Ongoing | Attendance/minutes | MLRC Secretary |
| SE-C10 | On change | Validation | RAV |

---

## 7. Key Risk Indicators (KRIs)

| KRI ID | Indicator | Threshold | Escalation |
|--------|-----------|-----------|------------|
| KRI-SE-01 | Sensitivity limit breaches per week | >3 | MLRC |
| KRI-SE-02 | Average time to resolve breach (hours) | >4 | Market Risk |
| KRI-SE-03 | FO/Risk reconciliation breaks | >5% of desks | Head of RAV |
| KRI-SE-04 | Entities at >80% any sensitivity | >5 | MLRC |
| KRI-SE-05 | Pre-trade check overrides | >5 per week | Trading Head |

---

## 8. Related Controls

| Control ID | Control Name | Relationship |
|------------|--------------|--------------|
| MR-L5-001 | VaR Limits Controls | Complementary - VaR captures aggregate risk |
| MR-L5-002 | Stress Limits Controls | Complementary - tail risk coverage |
| MR-L5-005 | Concentration Limits Controls | Related - position-level limits |
| MR-L5-006 | Stop-Loss Controls | Complementary - P&L-based limits |

---

## 9. Document Control

### 9.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |

### 9.2 Review Schedule

- Full review: Annually (January)
- Limit calibration: Annually or on material portfolio change
- Post-incident: Following any control failure

---

*End of Document*
