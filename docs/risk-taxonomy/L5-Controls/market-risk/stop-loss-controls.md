---
# Control Metadata
control_id: MR-L5-006
control_name: Stop-Loss Controls
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
  - REQ-L1-005  # PRA Rulebook
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-003   # VaR Limit Framework
l4_processes:
  - MR-L4-007   # Market Risk Reporting and Sign-off
  - MR-L4-013   # Market Risk Limits Management
l6_models:
  - N/A         # Stop-loss is P&L-based, not model-based
l7_systems:
  - SYS-MR-003  # Murex (Front Office)
  - SYS-FIN-001 # Finance/P&L System
---

# Stop-Loss Controls

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Control ID** | MR-L5-006 |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Framework** | VaR Limit Framework (MR-L3-003) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

This document defines the controls for stop-loss limits, which provide a P&L-based constraint on trading activity. Stop-loss limits complement statistical measures (VaR) by triggering mandatory risk reduction when actual losses exceed defined thresholds, preventing trading desks from "doubling down" on losing positions.

---

## 2. Stop-Loss Philosophy

### 2.1 Why Stop-Loss Limits?

| VaR Limitations | Stop-Loss Solution |
|-----------------|-------------------|
| VaR is forward-looking; doesn't account for actual losses | Stop-loss responds to realized P&L |
| VaR allows "averaging down" if within limit | Stop-loss forces action after losses |
| VaR may underestimate during regime changes | Stop-loss caps cumulative loss |
| VaR is model-dependent | Stop-loss is based on actual P&L |

### 2.2 Stop-Loss Types

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  STOP-LOSS LIMIT TYPES                                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  DAILY STOP-LOSS                                                                │    │
│  │  ─────────────────                                                              │    │
│  │  • Trigger: Single-day P&L loss exceeds threshold                               │    │
│  │  • Calibration: Multiple of VaR limit (e.g., 1.5x VaR)                          │    │
│  │  • Action: Risk reduction; management notification                              │    │
│  │  • Reset: Daily (new limit each day)                                            │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  MTD (Month-to-Date) STOP-LOSS                                                  │    │
│  │  ──────────────────────────                                                     │    │
│  │  • Trigger: Cumulative MTD P&L loss exceeds threshold                           │    │
│  │  • Calibration: Multiple of VaR limit (e.g., 3x VaR)                            │    │
│  │  • Action: Significant risk reduction; senior escalation                        │    │
│  │  • Reset: Monthly (1st business day)                                            │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  YTD (Year-to-Date) STOP-LOSS (Entity Level Only)                               │    │
│  │  ────────────────────────────────────────────────                               │    │
│  │  • Trigger: Cumulative YTD P&L loss exceeds threshold                           │    │
│  │  • Calibration: Absolute amount aligned to risk appetite                        │    │
│  │  • Action: Trading restrictions; Board notification                             │    │
│  │  • Reset: Annually (1st business day of year)                                   │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Stop-Loss Limit Structure

### 3.1 Limit Table

| Level | Daily Stop-Loss | MTD Stop-Loss | YTD Stop-Loss |
|-------|-----------------|---------------|---------------|
| **Desk** | 1.5× VaR limit | 3× VaR limit | N/A |
| **Business Unit** | 2× VaR limit | 4× VaR limit | N/A |
| **Division** | 2× VaR limit | 4× VaR limit | N/A |
| **Entity** | N/A | N/A | $60m |

### 3.2 Example Limit Calculation

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  EXAMPLE: G10 Swaps Desk                                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  VaR Limit: $4m (99%, 1-day)                                                            │
│                                                                                         │
│  DAILY STOP-LOSS:                                                                       │
│  • Limit: 1.5 × $4m = $6m loss                                                          │
│  • Warning: 80% × $6m = $4.8m loss                                                      │
│                                                                                         │
│  MTD STOP-LOSS:                                                                         │
│  • Limit: 3 × $4m = $12m cumulative loss                                                │
│  • Warning: 80% × $12m = $9.6m cumulative loss                                          │
│                                                                                         │
│  If desk loses $6.5m in a single day:                                                   │
│  → Daily stop-loss BREACHED                                                             │
│  → Mandatory risk reduction triggered                                                   │
│  → Trading Head and MLRC Chair notified                                                 │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Warning Thresholds

| Utilisation | Status | Action |
|-------------|--------|--------|
| **0-79%** | 🟢 Green | Normal operations |
| **80-99%** | 🟡 Amber | Warning notification; enhanced monitoring |
| **100%+** | 🔴 Red | Stop-loss triggered; mandatory actions |

---

## 4. Control Objectives

| Objective ID | Objective | Risk Mitigated |
|--------------|-----------|----------------|
| **CO-01** | Stop-loss limits monitored intraday | Delayed response to large losses |
| **CO-02** | Triggered stop-losses result in mandatory risk reduction | Continued loss accumulation |
| **CO-03** | P&L feeds accurate and timely | Incorrect trigger decisions |
| **CO-04** | Exceptions properly approved | Unauthorized risk-taking |
| **CO-05** | Stop-loss performance reviewed | Framework calibration drift |

---

## 5. Control Inventory

### 5.1 Control Summary

| Control ID | Control Name | Type | Frequency | Owner |
|------------|--------------|------|-----------|-------|
| SL-C01 | Intraday P&L Monitoring | Detective | Hourly | Trading / RAV |
| SL-C02 | Daily Stop-Loss Comparison | Detective | Hourly / EOD | RAV |
| SL-C03 | MTD Stop-Loss Comparison | Detective | Daily | RAV |
| SL-C04 | YTD Stop-Loss Comparison | Detective | Daily | Market Risk |
| SL-C05 | Stop-Loss Trigger Alert | Detective | On trigger | RAV |
| SL-C06 | Mandatory Risk Reduction | Corrective | On trigger | Trading |
| SL-C07 | Stop-Loss Exception Approval | Preventive | On request | MLRC |
| SL-C08 | P&L Feed Validation | Detective | Daily | Finance / RAV |
| SL-C09 | Monthly Stop-Loss Reset | Preventive | Monthly | RAV |
| SL-C10 | MLRC Stop-Loss Review | Detective | Weekly | MLRC |
| SL-C11 | Stop-Loss Calibration Review | Detective | Annually | Market Risk |

---

## 6. Control Details

### 6.1 SL-C01: Intraday P&L Monitoring

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: SL-C01 - Intraday P&L Monitoring                                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Monitor P&L throughout the day to identify approaching stop-losses          │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Hourly (10:00, 11:00, 12:00, 14:00, 15:00, 16:00)                           │
│  OWNER: Trading (primary) / RAV (oversight)                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  P&L FEED:                                                                              │
│                                                                                         │
│       ┌──────────────┐     ┌──────────────┐     ┌──────────────┐                        │
│       │   Murex FO   │────▶│   Finance    │────▶│  Risk        │                        │
│       │  (Positions) │     │   (P&L Calc) │     │  Dashboard   │                        │
│       └──────────────┘     └──────────────┘     └──────────────┘                        │
│              │                    │                    │                                │
│              │              Hourly P&L              Traffic                             │
│              │              Snapshot                Light                               │
│              │                    │                    │                                │
│              ▼                    ▼                    ▼                                │
│       Position Values      Intraday P&L          Stop-Loss                              │
│       MTM Update           by Desk/BU            Utilisation                            │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CONTROL ACTIVITIES:                                                                    │
│  1. Finance calculates hourly P&L estimate for each desk                                │
│  2. P&L published to risk dashboard                                                     │
│  3. Compare to daily and MTD stop-loss limits                                           │
│  4. Generate traffic light status                                                       │
│  5. Trading desks responsible for monitoring their P&L                                  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Hourly P&L snapshots                                                                 │
│  • Dashboard access logs                                                                │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 SL-C02: Daily Stop-Loss Comparison

| Attribute | Value |
|-----------|-------|
| **Control ID** | SL-C02 |
| **Objective** | Compare daily P&L against daily stop-loss limit |
| **Type** | Detective |
| **Frequency** | Hourly (intraday) and EOD (official) |
| **Owner** | RAV |

**Control Activities**:
1. Calculate daily P&L for each desk, BU, division
2. Compare against daily stop-loss limit (1.5-2× VaR)
3. Apply traffic light classification:
   - Green: P&L loss < 80% of stop-loss
   - Amber: P&L loss 80-99% of stop-loss
   - Red: P&L loss ≥ stop-loss → TRIGGERED
4. Generate alerts for Amber and Red status
5. EOD comparison is official (trigger Finance P&L)

**Evidence**:
- Intraday P&L dashboard
- Daily stop-loss status report

### 6.3 SL-C03: MTD Stop-Loss Comparison

| Attribute | Value |
|-----------|-------|
| **Control ID** | SL-C03 |
| **Objective** | Compare MTD cumulative P&L against MTD stop-loss limit |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | RAV |

**Control Activities**:
1. Calculate cumulative MTD P&L for each desk, BU, division
2. Compare against MTD stop-loss limit (3-4× VaR)
3. Apply traffic light classification
4. Generate alerts for Amber and Red status
5. Include in daily risk report

**Evidence**:
- MTD P&L tracker
- Daily stop-loss status report

### 6.4 SL-C04: YTD Stop-Loss Comparison

| Attribute | Value |
|-----------|-------|
| **Control ID** | SL-C04 |
| **Objective** | Monitor entity-level YTD P&L against annual stop-loss |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | Market Risk |

**Control Activities**:
1. Calculate cumulative YTD P&L for entity trading book
2. Compare against YTD stop-loss limit ($60m)
3. Apply traffic light classification
4. Report to MLRC weekly and RMC monthly
5. Escalate to Board if approaching limit

**Evidence**:
- YTD P&L tracker
- MLRC/RMC reporting

### 6.5 SL-C05: Stop-Loss Trigger Alert

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: SL-C05 - Stop-Loss Trigger Alert                                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Immediate notification when stop-loss is triggered                          │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: On trigger                                                                  │
│  OWNER: RAV                                                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ESCALATION MATRIX:                                                                     │
│                                                                                         │
│  DESK STOP-LOSS TRIGGER                                                                 │
│  ├─ Notify: Desk Head, BU Head, Market Risk                                             │
│  ├─ Timeline: Immediate (within 15 minutes)                                             │
│  ├─ Method: Email + Phone call + Dashboard alert                                        │
│  └─ Required: Verbal acknowledgement from Desk Head                                     │
│                                                                                         │
│  BU STOP-LOSS TRIGGER                                                                   │
│  ├─ Notify: BU Head, Trading Head, Market Risk, MLRC Chair                              │
│  ├─ Timeline: Immediate (within 15 minutes)                                             │
│  ├─ Method: Email + Phone call                                                          │
│  └─ Required: Risk reduction plan within 2 hours                                        │
│                                                                                         │
│  DIVISION STOP-LOSS TRIGGER                                                             │
│  ├─ Notify: Division Head, CRO, MLRC, RMC Secretary                                     │
│  ├─ Timeline: Immediate (within 15 minutes)                                             │
│  ├─ Method: Email + Phone call to CRO                                                   │
│  └─ Required: Emergency MLRC call; formal reduction plan                                │
│                                                                                         │
│  ENTITY YTD STOP-LOSS TRIGGER                                                           │
│  ├─ Notify: CRO, CEO, Board Risk Chair, RMC, MLRC                                       │
│  ├─ Timeline: Immediate (within 15 minutes)                                             │
│  ├─ Method: Phone calls + Emergency Board notification                                  │
│  └─ Required: Trading restrictions; Board approval to continue                          │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Stop-loss trigger notification (timestamped)                                         │
│  • Phone call log                                                                       │
│  • Acknowledgement record                                                               │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.6 SL-C06: Mandatory Risk Reduction

| Attribute | Value |
|-----------|-------|
| **Control ID** | SL-C06 |
| **Objective** | Ensure triggered stop-loss results in risk reduction |
| **Type** | Corrective |
| **Frequency** | On trigger |
| **Owner** | Trading |

**Control Activities**:
1. Upon stop-loss trigger, trading must:
   - Reduce gross risk by minimum 25%
   - Hedge or close largest losing positions
   - Document positions closed/hedged
2. Risk reduction to be completed within:
   - Daily stop-loss: End of trading day
   - MTD stop-loss: 2 business days
   - YTD stop-loss: As directed by CRO/Board
3. Market Risk verifies risk reduction
4. MLRC reviews adequacy of reduction

**Exception**: Risk reduction may be deferred if market conditions make orderly exit impossible (requires MLRC approval)

**Evidence**:
- Position reduction confirmation
- Before/after risk comparison
- MLRC review

### 6.7 SL-C07: Stop-Loss Exception Approval

| Attribute | Value |
|-----------|-------|
| **Control ID** | SL-C07 |
| **Objective** | Formal approval for exceptions to stop-loss action |
| **Type** | Preventive |
| **Frequency** | On request |
| **Owner** | MLRC |

**Exception Types**:

| Type | Description | Approval |
|------|-------------|----------|
| **Deferral** | Delay risk reduction due to market conditions | MLRC (max 2 days) |
| **Reduction** | Reduce risk by less than 25% | MLRC |
| **Override** | Continue trading without reduction | RMC |

**Approval Requirements**:
1. Written request with business justification
2. Market conditions assessment
3. Alternative risk mitigation measures
4. Timeline for compliance
5. MLRC/RMC approval recorded in minutes

**Evidence**:
- Exception request form
- Approval email/minutes

### 6.8 SL-C08: P&L Feed Validation

| Attribute | Value |
|-----------|-------|
| **Control ID** | SL-C08 |
| **Objective** | Ensure P&L used for stop-loss is accurate |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | Finance / RAV |

**Control Activities**:
1. Reconcile intraday P&L estimates to official EOD P&L
2. Investigate significant deviations (>5%)
3. Validate P&L feed completeness (all desks included)
4. Check for late bookings that affect prior day P&L
5. Confirm Finance P&L is source of truth for triggers

**Evidence**:
- P&L reconciliation report
- Variance investigation log

### 6.9 SL-C09: Monthly Stop-Loss Reset

| Attribute | Value |
|-----------|-------|
| **Control ID** | SL-C09 |
| **Objective** | Ensure MTD stop-loss resets correctly each month |
| **Type** | Preventive |
| **Frequency** | Monthly (1st business day) |
| **Owner** | RAV |

**Control Activities**:
1. On 1st business day of month:
   - MTD P&L counters reset to zero
   - MTD stop-loss limits restored
2. Verify system reset completed correctly
3. Confirm dashboard shows reset
4. Archive prior month stop-loss history

**Evidence**:
- System reset confirmation
- Prior month archive

### 6.10 SL-C10: MLRC Stop-Loss Review

| Attribute | Value |
|-----------|-------|
| **Control ID** | SL-C10 |
| **Objective** | Governance oversight of stop-loss framework |
| **Type** | Detective |
| **Frequency** | Weekly |
| **Owner** | MLRC |

**Control Activities**:
1. Market Risk presents stop-loss summary to MLRC:
   - Current MTD P&L vs limits (all levels)
   - Any triggers in period
   - Risk reduction actions taken
   - Exceptions granted
   - Trend analysis
2. MLRC reviews and challenges
3. Decisions minuted

**Evidence**:
- MLRC agenda and pack
- MLRC minutes

### 6.11 SL-C11: Stop-Loss Calibration Review

| Attribute | Value |
|-----------|-------|
| **Control ID** | SL-C11 |
| **Objective** | Ensure stop-loss limits remain appropriately calibrated |
| **Type** | Detective |
| **Frequency** | Annually |
| **Owner** | Market Risk |

**Control Activities**:
1. Review stop-loss trigger frequency over past year
2. Analyse effectiveness:
   - Did triggered stop-losses prevent further loss?
   - Were limits triggered by idiosyncratic or market events?
3. Benchmark against peer practices
4. Assess calibration (VaR multiples) appropriateness
5. Recommend changes to MLRC/RMC

**Evidence**:
- Annual Stop-Loss Calibration Review
- MLRC/RMC presentation

---

## 7. Stop-Loss Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        STOP-LOSS DASHBOARD (Example)                                    │
│                            As at: [Date] 14:00                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ENTITY YTD STOP-LOSS                                                                   │
│  ─────────────────────                                                                  │
│  YTD P&L: +$12.3m                        Limit: $60m loss                               │
│  Status: 🟢 SAFE (positive P&L)           No utilisation                                │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  DAILY STOP-LOSS STATUS                                                                 │
│  ─────────────────────────                                                              │
│  Entity          │  Daily P&L  │  Limit   │  Util   │  Status                           │
│  ────────────────┼─────────────┼──────────┼─────────┼─────────                          │
│  G10 Swaps       │   -$2.1m    │  $6.0m   │   35%   │   🟢                              │
│  EM Rates        │   -$0.8m    │  $3.75m  │   21%   │   🟢                              │
│  Options         │   +$0.3m    │  $2.25m  │    0%   │   🟢                              │
│  FX G10 Spot     │   -$1.5m    │  $3.0m   │   50%   │   🟢                              │
│  FX EM           │   -$2.8m    │  $3.0m   │   93%   │   🟡 WARNING                      │
│  FX Options      │   +$0.5m    │  $1.5m   │    0%   │   🟢                              │
│  Credit IG       │   -$0.2m    │  $3.0m   │    7%   │   🟢                              │
│  Credit HY       │   -$1.9m    │  $2.25m  │   84%   │   🟡 WARNING                      │
│  Credit EM       │   -$0.4m    │  $0.75m  │   53%   │   🟢                              │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  MTD STOP-LOSS STATUS                                                                   │
│  ────────────────────                                                                   │
│  Entity          │  MTD P&L    │  Limit   │  Util   │  Status                           │
│  ────────────────┼─────────────┼──────────┼─────────┼─────────                          │
│  G10 Swaps       │   +$3.2m    │  $12.0m  │    0%   │   🟢                              │
│  EM Rates        │   -$1.5m    │  $7.5m   │   20%   │   🟢                              │
│  Options         │   +$1.8m    │  $4.5m   │    0%   │   🟢                              │
│  FX G10 Spot     │   -$2.1m    │  $6.0m   │   35%   │   🟢                              │
│  FX EM           │   -$5.2m    │  $6.0m   │   87%   │   🟡 WARNING                      │
│  FX Options      │   +$2.2m    │  $3.0m   │    0%   │   🟢                              │
│  Credit IG       │   +$1.5m    │  $6.0m   │    0%   │   🟢                              │
│  Credit HY       │   -$3.8m    │  $4.5m   │   84%   │   🟡 WARNING                      │
│  Credit EM       │   -$0.9m    │  $1.5m   │   60%   │   🟢                              │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ⚠️  ALERTS:                                                                            │
│  • FX EM approaching daily stop-loss (93%) - notify Desk Head                           │
│  • Credit HY approaching daily stop-loss (84%) - monitor closely                        │
│  • FX EM approaching MTD stop-loss (87%) - MLRC attention                               │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Stop-Loss Trigger Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  STOP-LOSS TRIGGER PROCESS FLOW                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐            │
│  │   P&L       │     │   Compare   │     │   Trigger   │     │   Risk      │            │
│  │   Monitor   │────▶│   to Limit  │────▶│   Alert     │────▶│   Reduction │            │
│  │             │     │             │     │             │     │             │            │
│  └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘            │
│        │                   │                   │                   │                    │
│        │                   │                   │                   │                    │
│        ▼                   ▼                   ▼                   ▼                    │
│   Hourly P&L          If ≥100%:           Notify:             Reduce risk               │
│   snapshots           TRIGGERED           - Desk Head         by 25%+                   │
│                                           - Market Risk                                 │
│                       If ≥80%:            - MLRC Chair         Verify                   │
│                       WARNING             (if BU+)             reduction                │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  DECISION POINTS:                                                                       │
│                                                                                         │
│       ┌─────────────────────────────────────────────────────────────────────────────┐   │
│       │                         STOP-LOSS TRIGGERED                                 │   │
│       └─────────────────────────────────┬───────────────────────────────────────────┘   │
│                                         │                                               │
│                    ┌────────────────────┼────────────────────┐                          │
│                    │                    │                    │                          │
│                    ▼                    ▼                    ▼                          │
│           ┌───────────────┐    ┌───────────────┐    ┌───────────────┐                   │
│           │   Standard    │    │   Deferral    │    │   Override    │                   │
│           │   Reduction   │    │   Requested   │    │   Requested   │                   │
│           │               │    │               │    │               │                   │
│           │  Reduce 25%+  │    │  MLRC review  │    │  RMC review   │                   │
│           │  by EOD       │    │  Max 2 days   │    │  Exceptional  │                   │
│           └───────────────┘    └───────────────┘    └───────────────┘                   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Control Testing Schedule

| Control | Test Frequency | Test Type | Tester |
|---------|---------------|-----------|--------|
| SL-C01 | Monthly | System check | Risk Technology |
| SL-C02 | Monthly | Calculation verification | Internal Audit |
| SL-C03 | Monthly | Calculation verification | Internal Audit |
| SL-C04 | Quarterly | Review | Market Risk |
| SL-C05 | Semi-annually | Scenario simulation | Operational Risk |
| SL-C06 | Semi-annually | Process review | Internal Audit |
| SL-C07 | Annually | Sample testing | Internal Audit |
| SL-C08 | Monthly | Reconciliation | Finance / RAV |
| SL-C09 | Monthly | System check | RAV |
| SL-C10 | Ongoing | Attendance/minutes | MLRC Secretary |
| SL-C11 | Annually | Full review | Market Risk |

---

## 10. Key Risk Indicators (KRIs)

| KRI ID | Indicator | Threshold | Escalation |
|--------|-----------|-----------|------------|
| KRI-SL-01 | Stop-loss triggers per month | >3 | MLRC |
| KRI-SL-02 | Desks at >80% MTD utilisation | >3 | MLRC |
| KRI-SL-03 | Entity YTD utilisation | >50% | RMC |
| KRI-SL-04 | Exception requests per quarter | >5 | CRO |
| KRI-SL-05 | Time to risk reduction (hours) | >4 | Market Risk |
| KRI-SL-06 | P&L feed reconciliation breaks | >2% | Finance |

---

## 11. Related Controls

| Control ID | Control Name | Relationship |
|------------|--------------|--------------|
| MR-L5-001 | VaR Limits Controls | Complementary - VaR is forward-looking risk |
| MR-L5-002 | Stress Limits Controls | Complementary - tail risk control |
| MR-L5-003 | Sensitivity Limits Controls | Complementary - risk factor control |
| MR-L5-005 | Concentration Limits Controls | Related - position-level constraints |

---

## 12. Document Control

### 12.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |

### 12.2 Review Schedule

- Full review: Annually (January)
- Calibration review: Annually
- Post-incident: Following any YTD trigger

---

*End of Document*
