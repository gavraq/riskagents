---
# Control Metadata
control_id: MR-L5-004
control_name: Backtesting Exception Controls
version: 1.0
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Market Risk
approving_committee: RMC

# Taxonomy Linkages
parent_process: MR-L4-008  # Backtesting
parent_framework: MR-L3-003  # VaR Limit Framework
l1_requirements:
  - REQ-L1-001  # CRR (UK)
  - REQ-L1-003  # FRTB
  - REQ-L1-004  # Basel III/IV
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-003   # VaR Limit Framework
l4_processes:
  - MR-L4-008   # Backtesting
  - MR-L4-006   # Risk Engine Calculation
  - MR-L4-009   # Regulatory Reporting
l6_models:
  - MR-L6-001   # Historical Simulation VaR
  - MR-L6-002   # Stressed VaR
l7_systems:
  - SYS-MR-001  # Risk Engine (FMDM)
  - SYS-FIN-001 # Finance/P&L System
---

# Backtesting Exception Controls

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Control ID** | MR-L5-004 |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Framework** | VaR Limit Framework (MR-L3-003) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

This document defines the controls for VaR model backtesting, exception identification, analysis, and escalation. Backtesting is a critical validation mechanism that compares VaR predictions against actual P&L outcomes to assess model accuracy and calibration.

---

## 2. Regulatory Framework

### 2.1 CRR Requirements

| Article | Requirement | Implementation |
|---------|-------------|----------------|
| **CRR Article 366** | Daily backtesting required | Hypothetical and Actual P&L backtesting |
| **CRR Article 366(3)** | 250 business day rolling window | Exception counting over rolling year |
| **CRR Article 366(4)** | Traffic light zones for multipliers | Green/Yellow/Red zones |

### 2.2 Traffic Light Zone Classification

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  BASEL TRAFFIC LIGHT ZONES (CRR Article 366)                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ZONE          │  EXCEPTIONS (250 days)  │  PLUS FACTOR (mc)  │  INTERPRETATION         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  🟢 GREEN      │  0 - 4                  │  0.00              │  Model is accurate      │
│                │                         │                    │                         │
│  🟡 YELLOW     │  5                      │  0.40              │  Monitor closely        │
│                │  6                      │  0.50              │                         │
│                │  7                      │  0.65              │                         │
│                │  8                      │  0.75              │                         │
│                │  9                      │  0.85              │                         │
│                │                         │                    │                         │
│  🔴 RED        │  10+                    │  1.00              │  Model is inaccurate    │
│                │                         │                    │  PRA notification req'd │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CAPITAL IMPACT:                                                                        │
│  Own Funds = max(VaRt-1, mc × VaRavg) + max(SVaRt-1, ms × SVaRavg) + IRC                │
│                                                                                         │
│  Where mc = 3 + plus factor (minimum 3, maximum 4)                                      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Exception Definition

An **exception** (or "backtesting breach") occurs when:
- **Actual P&L loss** > **VaR prediction** (for actual backtesting)
- **Hypothetical P&L loss** > **VaR prediction** (for hypothetical backtesting)

At 99% confidence, we statistically expect ~2.5 exceptions per 250 days.

---

## 3. Backtesting Types

### 3.1 Hypothetical Backtesting (Regulatory)

| Attribute | Value |
|-----------|-------|
| **P&L Type** | Hypothetical (clean P&L) |
| **Definition** | P&L that would have occurred if positions held unchanged |
| **Excludes** | New trades, fees, commissions, intraday trading P&L |
| **Purpose** | Tests VaR model accuracy in isolation |
| **Regulatory Use** | Determines traffic light zone and plus factor |

### 3.2 Actual Backtesting (Risk Management)

| Attribute | Value |
|-----------|-------|
| **P&L Type** | Actual daily P&L |
| **Definition** | True economic P&L including all trading activity |
| **Includes** | All P&L components |
| **Purpose** | Tests VaR usefulness as risk measure |
| **Regulatory Use** | Additional monitoring; does not affect multiplier |

---

## 4. Control Objectives

| Objective ID | Objective | Risk Mitigated |
|--------------|-----------|----------------|
| **CO-01** | All backtesting exceptions are identified daily | Undetected model failures |
| **CO-02** | Exception root causes are documented | Unaddressed model deficiencies |
| **CO-03** | Traffic light zone changes are escalated | Capital adequacy surprises |
| **CO-04** | P&L feed accuracy is validated | Incorrect backtesting results |
| **CO-05** | Exception count is reported to regulators | Regulatory non-compliance |
| **CO-06** | Persistent exceptions trigger model review | Model obsolescence |

---

## 5. Control Inventory

### 5.1 Control Summary

| Control ID | Control Name | Type | Frequency | Owner |
|------------|--------------|------|-----------|-------|
| BT-C01 | Daily Backtesting Comparison | Detective | Daily | RAV |
| BT-C02 | Exception Identification | Detective | Daily | RAV |
| BT-C03 | Exception Root Cause Analysis | Detective | Per exception | RAV / Trading |
| BT-C04 | Exception Count Tracking (Rolling 250) | Detective | Daily | RAV |
| BT-C05 | Traffic Light Zone Monitoring | Detective | Daily | Market Risk |
| BT-C06 | Zone Change Escalation | Responsive | On change | Market Risk |
| BT-C07 | P&L Feed Reconciliation | Detective | Daily | RAV |
| BT-C08 | Hypothetical P&L Validation | Detective | Daily | Finance / RAV |
| BT-C09 | Desk-Level Backtesting | Detective | Daily | RAV |
| BT-C10 | MLRC Backtesting Report | Detective | Weekly | MLRC |
| BT-C11 | RMC Backtesting Review | Detective | Monthly | RMC |
| BT-C12 | PRA Notification (Red Zone) | Responsive | On trigger | CRO |

---

## 6. Control Details

### 6.1 BT-C01: Daily Backtesting Comparison

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: BT-C01 - Daily Backtesting Comparison                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Compare VaR prediction against actual/hypothetical P&L daily                │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Daily (by 10:00 T+1)                                                        │
│  OWNER: RAV                                                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  PROCESS FLOW:                                                                          │
│                                                                                         │
│       T (Trade Date)                           T+1 (Backtesting)                        │
│       ──────────────                           ─────────────────                        │
│                                                                                         │
│       ┌────────────┐                           ┌────────────┐                           │
│       │  VaR (COB) │────────────────────────▶  │  Compare   │                           │
│       │  $18.5m    │                           │  VaR vs    │                           │
│       └────────────┘                           │    P&L     │                           │
│                                                └─────┬──────┘                           │
│       ┌────────────┐                                 │                                  │
│       │  Actual    │────────────────────────▶        │                                  │
│       │  P&L       │                                 ▼                                  │
│       │  -$12.3m   │                           ┌────────────┐                           │
│       └────────────┘                           │  Exception │                           │
│                                                │  Check     │                           │
│       ┌────────────┐                           └─────┬──────┘                           │
│       │  Hypo P&L  │────────────────────────▶        │                                  │
│       │  -$11.8m   │                                 ▼                                  │
│       └────────────┘                           If Loss > VaR                            │
│                                                = EXCEPTION                              │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EXAMPLE (No Exception):                                                                │
│  • VaR (T, 99%, 1-day): $18.5m                                                          │
│  • Hypothetical P&L (T+1): -$11.8m loss                                                 │
│  • Result: $11.8m < $18.5m → No exception                                               │
│                                                                                         │
│  EXAMPLE (Exception):                                                                   │
│  • VaR (T, 99%, 1-day): $18.5m                                                          │
│  • Hypothetical P&L (T+1): -$22.1m loss                                                 │
│  • Result: $22.1m > $18.5m → EXCEPTION                                                  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Daily Backtesting Report                                                             │
│  • VaR vs P&L scatter chart (updated daily)                                             │
│  • Exception flag in system                                                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 BT-C02: Exception Identification

| Attribute | Value |
|-----------|-------|
| **Control ID** | BT-C02 |
| **Objective** | Identify and flag all backtesting exceptions |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | RAV |

**Control Activities**:
1. Compare Hypothetical P&L loss against previous day's VaR
2. If loss exceeds VaR:
   - Flag as exception in backtesting system
   - Record exception details:
     - Date
     - VaR figure
     - Hypothetical P&L
     - Actual P&L
     - Overshoot amount ($ and %)
3. Generate exception notification
4. Update rolling 250-day exception count

**Evidence**:
- Exception flag in system
- Exception notification email
- Backtesting exception log

### 6.3 BT-C03: Exception Root Cause Analysis

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: BT-C03 - Exception Root Cause Analysis                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Document root cause of each exception for model improvement                 │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Per exception (within 3 business days)                                      │
│  OWNER: RAV (lead) / Trading (input)                                                    │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ROOT CAUSE CATEGORIES:                                                                 │
│                                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │  CATEGORY A: Market Event                                                        │   │
│  │  ────────────────────────────────────────────────────────────────────────────────│   │
│  │  • Extreme market move beyond historical observations                            │   │
│  │  • Fat-tail event (legitimate exception)                                         │   │
│  │  • Example: COVID-19 March 2020, Brexit vote, Lehman default                     │   │
│  │  • Action: Document event; no model change typically needed                      │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │  CATEGORY B: Model Deficiency                                                    │   │
│  │  ────────────────────────────────────────────────────────────────────────────────│   │
│  │  • Risk factor not captured in VaR                                               │   │
│  │  • Incorrect volatility/correlation assumptions                                  │   │
│  │  • Proxy risk factors inadequate                                                 │   │
│  │  • Example: Missing basis risk, wrong curve mapping                              │   │
│  │  • Action: Escalate to Model Risk; potential model enhancement                   │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │  CATEGORY C: Data Issue                                                          │   │
│  │  ────────────────────────────────────────────────────────────────────────────────│   │
│  │  • Position data error (VaR calculated on wrong positions)                       │   │
│  │  • Market data error (incorrect prices/rates)                                    │   │
│  │  • P&L feed error (incorrect P&L reported)                                       │   │
│  │  • Example: Missing trade, stale price, booking error                            │   │
│  │  • Action: Correct data; may reclassify as "non-exception"                       │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  DOCUMENTATION REQUIREMENTS:                                                            │
│  1. Exception date and magnitude                                                        │
│  2. Market conditions on exception day                                                  │
│  3. Portfolio breakdown showing drivers                                                 │
│  4. Root cause category and explanation                                                 │
│  5. Recommended action (if any)                                                         │
│  6. Sign-off by Head of RAV                                                             │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Exception Root Cause Analysis form                                                   │
│  • Supporting market data/P&L analysis                                                  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.4 BT-C04: Exception Count Tracking (Rolling 250)

| Attribute | Value |
|-----------|-------|
| **Control ID** | BT-C04 |
| **Objective** | Maintain accurate rolling 250-day exception count |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | RAV |

**Control Activities**:
1. Update rolling 250-day exception count after each backtesting comparison
2. Track separately for:
   - Entity level (regulatory)
   - Division level (management)
   - Desk level (management)
3. Track both hypothetical and actual backtesting exceptions
4. Maintain audit trail of exception history
5. Calculate current traffic light zone

**Evidence**:
- Daily exception count report
- Rolling 250-day exception history log

### 6.5 BT-C05: Traffic Light Zone Monitoring

| Attribute | Value |
|-----------|-------|
| **Control ID** | BT-C05 |
| **Objective** | Monitor traffic light zone and capital implications |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | Market Risk |

**Control Activities**:
1. Determine current traffic light zone based on exception count:
   - 0-4: Green
   - 5-9: Yellow
   - 10+: Red
2. Calculate applicable plus factor (mc)
3. Estimate capital impact of current zone
4. Project zone changes based on rolling window
5. Flag imminent zone transitions (e.g., 4th exception approaching)

**Evidence**:
- Traffic light zone indicator in daily report
- Capital impact estimation

### 6.6 BT-C06: Zone Change Escalation

| Attribute | Value |
|-----------|-------|
| **Control ID** | BT-C06 |
| **Objective** | Escalate traffic light zone changes appropriately |
| **Type** | Responsive |
| **Frequency** | On zone change |
| **Owner** | Market Risk |

**Escalation Matrix**:

| Zone Change | Escalate To | Timeline | Actions Required |
|-------------|-------------|----------|------------------|
| Green → Yellow | MLRC, CRO | Same day | Capital impact assessment; model review consideration |
| Yellow → Yellow (higher) | MLRC | Same day | Updated capital impact; intensified monitoring |
| Yellow → Red | CRO, RMC, Board Risk | Immediate | PRA notification; model remediation plan |
| Any → Green | MLRC | Information | Confirm sustained improvement |

**Evidence**:
- Zone change notification
- Capital impact memo
- Escalation email chain

### 6.7 BT-C07: P&L Feed Reconciliation

| Attribute | Value |
|-----------|-------|
| **Control ID** | BT-C07 |
| **Objective** | Ensure P&L used for backtesting is accurate |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | RAV |

**Control Activities**:
1. Reconcile Risk P&L feed against Finance P&L
2. Identify and investigate breaks:
   - Tolerance: ±1% or $100k (whichever greater)
3. Common break causes:
   - Timing differences
   - Adjustment entries
   - Trade amendments
4. Document and resolve breaks before backtesting
5. Escalate persistent breaks to Head of RAV

**Evidence**:
- Daily P&L reconciliation report
- Break investigation log

### 6.8 BT-C08: Hypothetical P&L Validation

| Attribute | Value |
|-----------|-------|
| **Control ID** | BT-C08 |
| **Objective** | Validate hypothetical P&L calculation methodology |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | Finance / RAV |

**Control Activities**:
1. Finance calculates hypothetical P&L:
   - Start with T-1 COB positions
   - Apply T market moves
   - Exclude intraday trading, new trades, fees
2. RAV validates calculation:
   - Check position snapshot is correct
   - Verify market data used
   - Confirm exclusions applied correctly
3. Compare hypothetical vs actual P&L:
   - Large divergence warrants investigation
4. Sign-off on hypothetical P&L

**Evidence**:
- Hypothetical P&L calculation workbook
- RAV validation sign-off

### 6.9 BT-C09: Desk-Level Backtesting

| Attribute | Value |
|-----------|-------|
| **Control ID** | BT-C09 |
| **Objective** | Identify model weaknesses at desk level |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | RAV |

**Control Activities**:
1. Perform backtesting at desk level (in addition to entity)
2. Track desk-level exception counts
3. Identify desks with poor backtesting performance:
   - More than expected exceptions
   - Systematic under/over prediction
4. Flag concerns to MLRC for investigation
5. May trigger desk-specific model review

**Note**: Desk-level backtesting is for internal management purposes; entity-level is for regulatory purposes.

**Evidence**:
- Desk-level backtesting report
- Performance heat map

### 6.10 BT-C10: MLRC Backtesting Report

| Attribute | Value |
|-----------|-------|
| **Control ID** | BT-C10 |
| **Objective** | Regular governance review of backtesting performance |
| **Type** | Detective |
| **Frequency** | Weekly |
| **Owner** | MLRC |

**Control Activities**:
1. Market Risk presents backtesting report to MLRC:
   - Rolling 250-day exception count
   - Current traffic light zone
   - Recent exceptions and root causes
   - Desk-level performance
   - Capital impact
2. MLRC reviews and challenges analysis
3. Decisions on model reviews or enhancements
4. Actions minuted

**Evidence**:
- MLRC agenda and pack
- MLRC minutes

### 6.11 BT-C11: RMC Backtesting Review

| Attribute | Value |
|-----------|-------|
| **Control ID** | BT-C11 |
| **Objective** | Senior governance oversight of VaR model performance |
| **Type** | Detective |
| **Frequency** | Monthly |
| **Owner** | RMC |

**Control Activities**:
1. Monthly backtesting summary presented to RMC:
   - Exception count and trend
   - Traffic light zone status
   - Capital implications
   - Model review status (if applicable)
   - Comparison to peers (if available)
2. RMC provides strategic direction on model investment
3. Escalate to Board if Red zone reached

**Evidence**:
- RMC agenda and pack
- RMC minutes

### 6.12 BT-C12: PRA Notification (Red Zone)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: BT-C12 - PRA Notification (Red Zone)                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Notify PRA when backtesting triggers Red zone                               │
│                                                                                         │
│  TYPE: Responsive                                                                       │
│  FREQUENCY: On trigger (10+ exceptions in 250 days)                                     │
│  OWNER: CRO                                                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  TRIGGER CONDITIONS:                                                                    │
│  • Rolling 250-day hypothetical backtesting exceptions ≥ 10                             │
│  • First time entering Red zone OR re-entering after Green/Yellow                       │
│                                                                                         │
│  NOTIFICATION TIMELINE:                                                                 │
│  • Internal escalation: Immediate (CRO, CEO, Board Risk Chair)                          │
│  • PRA notification: Within 5 business days of 10th exception                           │
│                                                                                         │
│  NOTIFICATION CONTENT:                                                                  │
│  1. Date of 10th exception                                                              │
│  2. Rolling 250-day exception history                                                   │
│  3. Root cause analysis summary                                                         │
│  4. Capital impact (plus factor = 1.00)                                                 │
│  5. Remediation plan:                                                                   │
│     • Model review timeline                                                             │
│     • Proposed enhancements                                                             │
│     • Target date to return to Yellow/Green                                             │
│  6. Interim risk management measures                                                    │
│                                                                                         │
│  ONGOING REQUIREMENTS WHILE IN RED ZONE:                                                │
│  • Monthly update to PRA on remediation progress                                        │
│  • Enhanced senior management reporting                                                 │
│  • May trigger supervisory review of IMA status                                         │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • PRA notification letter                                                              │
│  • Remediation plan document                                                            │
│  • Monthly progress reports                                                             │
│  • Board Risk Committee minutes                                                         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Backtesting Dashboard

### 7.1 Entity-Level Display

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        MERIDIAN GLOBAL BANK - BACKTESTING DASHBOARD                     │
│                                   As at: [Date]                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  TRAFFIC LIGHT ZONE:  🟢 GREEN                                                          │
│  Rolling 250-day Exceptions: 3                                                          │
│  Plus Factor (mc): 0.00                                                                 │
│  Current Multiplier: 3.00                                                               │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EXCEPTION HISTORY (Last 250 Days):                                                     │
│  ─────────────────────────────────                                                      │
│  [#] │ Date       │ VaR    │ Hypo P&L │ Overshoot │ Root Cause                          │
│  ────┼────────────┼────────┼──────────┼───────────┼──────────────────────────────────   │
│   1  │ 2024-03-15 │ $18.2m │ -$21.3m  │ $3.1m     │ Market Event (Rate spike)           │
│   2  │ 2024-06-22 │ $17.8m │ -$19.5m  │ $1.7m     │ Market Event (EM selloff)           │
│   3  │ 2024-11-08 │ $19.1m │ -$20.2m  │ $1.1m     │ Model (Basis risk)                  │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ZONE TRANSITION FORECAST:                                                              │
│  • Next exception would keep us in GREEN (4 exceptions)                                 │
│  • 5th exception would move us to YELLOW (mc = 0.40)                                    │
│  • Exception #1 rolls off on: 2025-03-15                                                │
│                                                                                         │
│  CAPITAL IMPACT (if zone change):                                                       │
│  • Current (Green, mc=3.00): $XX.Xm                                                     │
│  • Yellow (mc=3.40): +$X.Xm (+Y%)                                                       │
│  • Red (mc=4.00): +$XX.Xm (+Z%)                                                         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Control Testing Schedule

| Control | Test Frequency | Test Type | Tester |
|---------|---------------|-----------|--------|
| BT-C01 | Monthly | Sample testing | Internal Audit |
| BT-C02 | Monthly | Process review | RAV |
| BT-C03 | Quarterly | Sample review | Model Risk |
| BT-C04 | Monthly | Reconciliation | RAV |
| BT-C05 | Monthly | Calculation check | Internal Audit |
| BT-C06 | Semi-annually | Scenario test | Operational Risk |
| BT-C07 | Monthly | Full reconciliation | Finance / RAV |
| BT-C08 | Quarterly | Methodology review | Model Risk |
| BT-C09 | Quarterly | Coverage review | RAV |
| BT-C10 | Ongoing | Attendance/minutes | MLRC Secretary |
| BT-C11 | Ongoing | Attendance/minutes | RMC Secretary |
| BT-C12 | Semi-annually | Process review | Compliance |

---

## 9. Key Risk Indicators (KRIs)

| KRI ID | Indicator | Threshold | Escalation |
|--------|-----------|-----------|------------|
| KRI-BT-01 | Rolling 250-day exception count | ≥5 | MLRC/CRO |
| KRI-BT-02 | Time in Yellow/Red zone | >90 days | RMC |
| KRI-BT-03 | Consecutive exceptions | ≥3 | Market Risk |
| KRI-BT-04 | P&L reconciliation breaks | >1% | Head of RAV |
| KRI-BT-05 | Root cause analysis backlog | >5 days | Head of RAV |
| KRI-BT-06 | Desk-level exception rate | >4 in 250 (desk) | MLRC |

---

## 10. Related Controls

| Control ID | Control Name | Relationship |
|------------|--------------|--------------|
| MR-L5-001 | VaR Limits Controls | Related - VaR quality affects limits |
| MR-L5-002 | Stress Limits Controls | Complementary - stress captures tail |
| MR-L6-001 | VaR Model Documentation | Upstream - model drives backtesting |
| MR-L4-009 | Regulatory Reporting | Downstream - exception count reported |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | RMC |

### 11.2 Review Schedule

- Full review: Annually (January)
- Exception analysis methodology: Semi-annually
- Post-incident: Following Red zone entry

---

*End of Document*
