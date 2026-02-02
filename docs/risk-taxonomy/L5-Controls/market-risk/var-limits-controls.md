---
# Control Metadata
control_id: MR-L5-001
control_name: VaR and SVaR Limits Controls
version: 1.1
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
  - REQ-L1-004  # Basel III/IV
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - MR-L3-003   # VaR Limit Framework
l4_processes:
  - MR-L4-006   # Risk Engine Calculation
  - MR-L4-007   # Market Risk Reporting and Sign-off
  - MR-L4-013   # Market Risk Limits Management
l6_models:
  - MR-L6-001   # Historical Simulation VaR (VaR and SVaR)
l7_systems:
  - SYS-MR-001  # Risk Engine (FMDM)
  - SYS-MR-003  # Murex (Front Office)
  - SYS-MR-004  # Risk Reporting DataMart
---

# VaR and SVaR Limits Controls

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Control ID** | MR-L5-001 |
| **Version** | 1.1 |
| **Effective Date** | 15 January 2025 |
| **Parent Framework** | VaR Limit Framework (MR-L3-003) |
| **Owner** | Head of Market Risk |

---

## 1. Purpose

This document defines the key controls for Value at Risk (VaR) and Stressed VaR (SVaR) limits. VaR and SVaR are calculated using the same Historical Simulation model with different observation periods - VaR uses recent history while SVaR uses a stressed historical period (2008-09). These controls ensure both measures remain within approved risk appetite and that breaches are appropriately escalated and managed.

---

## 2. Scope

### 2.1 VaR and SVaR Relationship

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  VaR AND SVaR: SAME MODEL, DIFFERENT OBSERVATION PERIODS                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│                        ┌─────────────────────────────────────────┐                      │
│                        │     HISTORICAL SIMULATION MODEL         │                      │
│                        │          (MR-L6-001)                    │                      │
│                        └──────────────────┬──────────────────────┘                      │
│                                           │                                             │
│                    ┌──────────────────────┴──────────────────────┐                      │
│                    │                                             │                      │
│                    ▼                                             ▼                      │
│         ┌─────────────────────┐                       ┌─────────────────────┐           │
│         │        VaR          │                       │       SVaR          │           │
│         │                     │                       │                     │           │
│         │  Observation:       │                       │  Observation:       │           │
│         │  Rolling 500 days   │                       │  Stressed period    │           │
│         │  (recent history)   │                       │  (2008-09 GFC)      │           │
│         │                     │                       │                     │           │
│         │  Purpose:           │                       │  Purpose:           │           │
│         │  Current risk       │                       │  Risk under stress  │           │
│         └─────────────────────┘                       └─────────────────────┘           │
│                                                                                         │
│  KEY PRINCIPLE: A methodology change to the model always affects BOTH VaR and SVaR     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Limit Parameters

| Metric | Parameters | Entity Limit | Warning (80%) |
|--------|------------|--------------|---------------|
| **Daily VaR** | 99%, 1-day, HS | $25m | $20m |
| **10-day VaR** | 99%, 10-day, HS | $79m | $63m |
| **Stressed VaR** | 99%, 1-day, 2008-09 | $50m | $40m |
| **Stressed VaR 10-day** | 99%, 10-day, 2008-09 | $158m | $126m |

### 2.3 Limit Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        ENTITY VaR/SVaR LIMITS                                           │
│                                                                                         │
│               VaR: $25m (99%, 1-day)    │    SVaR: $50m (99%, 1-day)                    │
│               Approved by: Board/RMC    │    Approved by: Board/RMC                     │
└─────────────────────────────────────────┬───────────────────────────────────────────────┘
                                          │
         ┌────────────────────────────────┼────────────────────────────────┐
         │                                │                                │
         ▼                                ▼                                ▼
┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐
│      MARKETS        │        │      TREASURY       │        │      RESERVE        │
│   VaR: $19m         │        │   VaR: $6m          │        │   (Unallocated)     │
│   SVaR: $38m        │        │   SVaR: $12m        │        │   VaR: $2.5m        │
│   (RMC)             │        │   (RMC)             │        │                     │
└──────────┬──────────┘        └──────────┬──────────┘        └─────────────────────┘
           │                              │
    ┌──────┴──────┬──────────┐            │
    │             │          │            │
    ▼             ▼          ▼            ▼
┌────────┐  ┌────────┐  ┌────────┐   ┌────────┐
│ Rates  │  │   FX   │  │ Credit │   │Treasury│
│VaR:$10m│  │VaR:$6m │  │VaR:$5m │   │VaR:$6m │
│SVaR:$20│  │SVaR:$12│  │SVaR:$10│   │SVaR:$12│
│(MLRC)  │  │(MLRC)  │  │(MLRC)  │   │(MLRC)  │
└────────┘  └────────┘  └────────┘   └────────┘
```

**Note**: Sum of sub-limits exceeds parent due to diversification benefit assumption (~25% at division level).

---

## 3. Control Objectives

| Objective ID | Objective | Risk Mitigated |
|--------------|-----------|----------------|
| **CO-01** | VaR and SVaR limits are monitored daily against approved thresholds | Undetected limit breaches |
| **CO-02** | Limit breaches are escalated within defined timeframes | Delayed response to excess risk |
| **CO-03** | Breach remediation actions are tracked to completion | Persistent limit breaches |
| **CO-04** | Limit utilisation trends are reported to governance | Risk appetite drift |
| **CO-05** | Limit hierarchy integrity is maintained | Incorrect limit aggregation |
| **CO-06** | Temporary excesses are approved and time-bound | Unapproved risk-taking |
| **CO-07** | SVaR/VaR ratio monitored as early warning indicator | Model calibration drift |

---

## 4. Control Inventory

### 4.1 Control Summary

| Control ID | Control Name | Type | Frequency | Owner |
|------------|--------------|------|-----------|-------|
| VL-C01 | Daily VaR vs Limit Comparison | Detective | Daily | RAV |
| VL-C02 | Daily SVaR vs Limit Comparison | Detective | Daily | RAV |
| VL-C03 | Warning Threshold Monitoring (VaR & SVaR) | Detective | Daily | RAV |
| VL-C04 | Breach Identification and Classification | Detective | Daily | RAV |
| VL-C05 | Breach Escalation | Responsive | On breach | RAV / Market Risk |
| VL-C06 | Breach Root Cause Documentation | Detective | On breach | Trading / RAV |
| VL-C07 | Remediation Action Tracking | Corrective | Daily | Market Risk |
| VL-C08 | Temporary Excess Approval | Preventive | On request | MLRC / RMC |
| VL-C09 | Temporary Excess Expiry Monitoring | Detective | Daily | Market Risk |
| VL-C10 | Limit Hierarchy Reconciliation | Detective | Weekly | RAV |
| VL-C11 | Limit Utilisation Trend Analysis | Detective | Weekly | Market Risk |
| VL-C12 | SVaR/VaR Ratio Monitoring | Detective | Daily | RAV |
| VL-C13 | MLRC Limit Dashboard Review | Detective | Weekly | MLRC |
| VL-C14 | System Limit Configuration Validation | Preventive | On change | Risk Technology |

---

## 5. Control Details

### 5.1 VL-C01: Daily VaR vs Limit Comparison

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: VL-C01 - Daily VaR vs Limit Comparison                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Ensure all VaR measures are compared against approved limits daily          │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Daily (by 09:00)                                                            │
│  OWNER: Risk Analytics and Validation (RAV)                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CONTROL ACTIVITIES:                                                                    │
│  1. Extract VaR results from Risk Engine (FMDM) for all levels:                         │
│     • Entity                                                                            │
│     • Division                                                                          │
│     • Business Unit                                                                     │
│     • Trading Desk                                                                      │
│                                                                                         │
│  2. Compare each VaR against corresponding approved limit                               │
│                                                                                         │
│  3. Calculate utilisation percentage: VaR / Limit × 100                                 │
│                                                                                         │
│  4. Apply traffic light classification:                                                 │
│     • GREEN: 0-79% utilisation                                                          │
│     • AMBER: 80-99% utilisation (Warning)                                               │
│     • RED: 100-109% utilisation (Breach)                                                │
│     • BLACK: ≥110% utilisation (Critical)                                               │
│                                                                                         │
│  5. Populate daily VaR dashboard with results                                           │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Daily VaR Report (auto-generated from FMDM)                                          │
│  • VaR Dashboard (published to SharePoint by 09:00)                                     │
│  • Limit utilisation log (retained 7 years)                                             │
│                                                                                         │
│  TESTING:                                                                               │
│  • Monthly: Sample 5 days, verify VaR/Limit calculation accuracy                        │
│  • Quarterly: Full reconciliation of limit values to approved framework                 │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 VL-C02: Daily SVaR vs Limit Comparison

| Attribute | Value |
|-----------|-------|
| **Control ID** | VL-C02 |
| **Objective** | Ensure all SVaR measures are compared against approved limits daily |
| **Type** | Detective |
| **Frequency** | Daily (by 09:00) |
| **Owner** | RAV |

**Control Activities**:
1. Extract SVaR results from Risk Engine (FMDM) for all levels:
   - Entity
   - Division
   - Business Unit
2. Compare each SVaR against corresponding approved SVaR limit
3. Calculate utilisation percentage: SVaR / SVaR Limit × 100
4. Apply traffic light classification (same as VaR)
5. Include in daily VaR/SVaR dashboard

**Note**: SVaR limits are typically set at 2x VaR limits to accommodate the stressed observation period.

**Evidence**:
- Daily VaR/SVaR Report
- SVaR Dashboard section
- SVaR limit utilisation log

### 5.3 VL-C03: Warning Threshold Monitoring (VaR & SVaR)

| Attribute | Value |
|-----------|-------|
| **Control ID** | VL-C03 |
| **Objective** | Identify approaching breaches before they occur |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | RAV |

**Control Activities**:
1. Identify all entities at AMBER status (80-99% utilisation) for both VaR and SVaR
2. Generate warning notification to:
   - Desk Head (for desk-level warnings)
   - Business Unit Head (for BU-level warnings)
   - Division Head + MLRC Chair (for division-level SVaR warnings)
   - Market Risk (all warnings)
3. Include in daily VaR/SVaR report "Watch List" section
4. Assess trend - is utilisation increasing?

**Evidence**:
- Warning notification emails (auto-generated)
- Daily VaR/SVaR Report "Watch List" section

### 5.4 VL-C04: Breach Identification and Classification

| Attribute | Value |
|-----------|-------|
| **Control ID** | VL-C04 |
| **Objective** | Correctly identify and classify all VaR and SVaR limit breaches |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | RAV |

**Control Activities**:
1. Identify all entities at RED or BLACK status (≥100% utilisation) for VaR or SVaR
2. Classify breach type:
   - **Technical**: Data/system error (investigate immediately)
   - **Passive**: Market movement caused breach (no new risk taken)
   - **Active**: New position caused breach
3. Record in Breach Register with:
   - Date/time of breach
   - Metric type (VaR or SVaR)
   - Entity and limit type
   - Breach amount ($ and %)
   - Classification
   - Initial assessment

**Evidence**:
- Breach Register entry
- Classification sign-off by Head of RAV

### 5.5 VL-C05: Breach Escalation

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: VL-C05 - Breach Escalation                                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ESCALATION MATRIX (applies to both VaR and SVaR breaches)                              │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  DESK LIMIT BREACH                                                                      │
│  ├─ Notify: Desk Head, Business Unit Head, Market Risk                                  │
│  ├─ Timeline: Immediate (within 30 minutes of identification)                           │
│  ├─ Method: Email + Phone call                                                          │
│  └─ Required: Verbal acknowledgement from Desk Head                                     │
│                                                                                         │
│  BUSINESS UNIT LIMIT BREACH                                                             │
│  ├─ Notify: BU Head, Trading Head, Market Risk, MLRC Chair                              │
│  ├─ Timeline: Immediate (within 30 minutes)                                             │
│  ├─ Method: Email + Phone call to MLRC Chair                                            │
│  └─ Required: Written acknowledgement; action plan within 4 hours                       │
│                                                                                         │
│  DIVISION LIMIT BREACH                                                                  │
│  ├─ Notify: Division Head, CRO, MLRC, RMC Secretary                                     │
│  ├─ Timeline: Immediate (within 15 minutes)                                             │
│  ├─ Method: Email + Phone call to CRO                                                   │
│  └─ Required: Emergency MLRC call; reduction plan within 24 hours                       │
│                                                                                         │
│  ENTITY LIMIT BREACH                                                                    │
│  ├─ Notify: CRO, CEO, RMC Chair, Board Risk Chair                                       │
│  ├─ Timeline: Immediate (within 15 minutes)                                             │
│  ├─ Method: Phone call to CRO and CEO; email to Board                                   │
│  └─ Required: Emergency RMC; formal reduction plan; Board notification                  │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  ADDITIONAL SVaR-SPECIFIC CONSIDERATIONS:                                               │
│  • SVaR breaches may indicate inadequate capital reserves                               │
│  • CRO must assess capital adequacy implications                                        │
│  • Prolonged SVaR breaches may require PRA notification                                 │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Escalation notification (email with timestamp)                                       │
│  • Phone call log (if applicable)                                                       │
│  • Acknowledgement receipt                                                              │
│  • Breach Register updated with escalation details                                      │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.6 VL-C06: Breach Root Cause Documentation

| Attribute | Value |
|-----------|-------|
| **Control ID** | VL-C06 |
| **Objective** | Document root cause of each breach for trend analysis |
| **Type** | Detective |
| **Frequency** | On breach |
| **Owner** | Trading (prepare) / RAV (review) |

**Control Activities**:
1. Trading desk completes root cause analysis within 24 hours
2. Analysis must include:
   - Positions contributing to breach
   - Market movements (if passive breach)
   - Trade activity (if active breach)
   - Data issues (if technical breach)
3. RAV reviews and validates root cause
4. Head of RAV signs off classification

**Evidence**:
- Root Cause Analysis form (in Breach Register)
- Sign-off by Desk Head and Head of RAV

### 5.7 VL-C07: Remediation Action Tracking

| Attribute | Value |
|-----------|-------|
| **Control ID** | VL-C07 |
| **Objective** | Ensure breach remediation actions are completed |
| **Type** | Corrective |
| **Frequency** | Daily (for open breaches) |
| **Owner** | Market Risk |

**Control Activities**:
1. Each breach requires documented remediation plan
2. Market Risk tracks progress daily
3. Remediation status reported to MLRC weekly
4. Overdue actions escalated to CRO

**Remediation Timeline Targets**:

| Breach Level | Back to Warning | Back to Green |
|--------------|-----------------|---------------|
| Desk | 2 days | 5 days |
| BU | 3 days | 7 days |
| Division | 5 days | 10 days |
| Entity | As agreed with RMC | As agreed with Board |

**Evidence**:
- Remediation tracker (updated daily)
- MLRC weekly breach report

### 5.8 VL-C08: Temporary Excess Approval

| Attribute | Value |
|-----------|-------|
| **Control ID** | VL-C08 |
| **Objective** | Ensure temporary limit excesses are formally approved |
| **Type** | Preventive |
| **Frequency** | On request |
| **Owner** | MLRC / RMC |

**Control Activities**:
1. Temporary excess request submitted with:
   - Business justification
   - Requested excess amount and duration
   - Risk mitigation measures
   - Exit strategy
2. Approval authority per framework:
   - MLRC: Up to 10% excess, max 5 business days
   - RMC: Up to 20% excess, max 10 business days
   - Board: >20% excess (exceptional only)
3. Approved excess recorded in Limit System
4. Enhanced monitoring during excess period

**Evidence**:
- Temporary Excess Request form
- Approval email/minutes
- Limit system configuration

### 5.9 VL-C09: Temporary Excess Expiry Monitoring

| Attribute | Value |
|-----------|-------|
| **Control ID** | VL-C09 |
| **Objective** | Ensure temporary excesses do not extend beyond approved period |
| **Type** | Detective |
| **Frequency** | Daily |
| **Owner** | Market Risk |

**Control Activities**:
1. Daily check of all active temporary excesses
2. T-2 days: Warning to Trading and MLRC Chair
3. T-1 day: Escalation if no extension request or reduction plan
4. Expiry day: Automatic removal from system; breach if still exceeded

**Evidence**:
- Temporary Excess Register
- Expiry warning notifications
- System removal confirmation

### 5.10 VL-C10: Limit Hierarchy Reconciliation

| Attribute | Value |
|-----------|-------|
| **Control ID** | VL-C10 |
| **Objective** | Ensure limit hierarchy in systems matches approved framework |
| **Type** | Detective |
| **Frequency** | Weekly |
| **Owner** | RAV |

**Control Activities**:
1. Extract VaR and SVaR limit configuration from Risk Engine
2. Compare to approved Limit Framework document
3. Verify:
   - All desks/BUs/divisions have both VaR and SVaR limits assigned
   - Limit values match approved amounts
   - Hierarchy roll-up is correct
   - Warning thresholds are correctly set (80%)
4. Investigate and resolve any discrepancies

**Evidence**:
- Weekly Limit Reconciliation Report
- Discrepancy log (if any)

### 5.11 VL-C11: Limit Utilisation Trend Analysis

| Attribute | Value |
|-----------|-------|
| **Control ID** | VL-C11 |
| **Objective** | Identify emerging limit pressure through trend analysis |
| **Type** | Detective |
| **Frequency** | Weekly |
| **Owner** | Market Risk |

**Control Activities**:
1. Analyse 4-week utilisation trend for each entity (VaR and SVaR)
2. Flag entities with:
   - Sustained high utilisation (>70% average)
   - Upward trend (>10% increase over 4 weeks)
   - Frequent warning breaches (>3 in 4 weeks)
3. Prepare trend report for MLRC
4. Recommend limit reviews if structural issues identified

**Evidence**:
- Weekly Utilisation Trend Report
- MLRC presentation

### 5.12 VL-C12: SVaR/VaR Ratio Monitoring

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  CONTROL: VL-C12 - SVaR/VaR Ratio Monitoring                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  OBJECTIVE: Monitor relationship between SVaR and VaR as early warning indicator        │
│                                                                                         │
│  TYPE: Detective                                                                        │
│  FREQUENCY: Daily                                                                       │
│  OWNER: RAV                                                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  RATIONALE:                                                                             │
│  Since VaR and SVaR use the same model with different observation periods, the ratio    │
│  provides insight into:                                                                 │
│  • How current market conditions compare to stressed period                             │
│  • Whether stressed period remains appropriately stressed                               │
│  • Portfolio composition changes affecting stress sensitivity                           │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  CONTROL ACTIVITIES:                                                                    │
│  1. Calculate daily SVaR/VaR ratio at entity level                                      │
│  2. Track 20-day moving average                                                         │
│  3. Flag if ratio deviates significantly:                                               │
│     • Normal range: 1.5x - 2.5x                                                         │
│     • Alert if <1.2x (stressed period may not be adequately stressed)                   │
│     • Alert if >3.0x (current period unusually calm vs stressed)                        │
│  4. Investigate significant deviations                                                  │
│  5. Report outliers to MLRC                                                             │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  IMPLICATIONS OF RATIO DEVIATIONS:                                                      │
│                                                                                         │
│  LOW RATIO (<1.2x):                                                                     │
│  • Current market more stressed than "stressed" period                                  │
│  • May indicate stressed period no longer appropriate                                   │
│  • Review stressed period selection with Model Risk                                     │
│                                                                                         │
│  HIGH RATIO (>3.0x):                                                                    │
│  • Large gap between current and stressed risk                                          │
│  • Portfolio may be highly sensitive to stress scenarios                                │
│  • May indicate capital adequacy concerns if stress materializes                        │
│                                                                                         │
│  EVIDENCE:                                                                              │
│  • Daily SVaR/VaR ratio in VaR/SVaR report                                              │
│  • Alert notifications                                                                  │
│  • Investigation notes                                                                  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.13 VL-C13: MLRC Limit Dashboard Review

| Attribute | Value |
|-----------|-------|
| **Control ID** | VL-C13 |
| **Objective** | Governance oversight of limit framework effectiveness |
| **Type** | Detective |
| **Frequency** | Weekly (at MLRC) |
| **Owner** | MLRC |

**Control Activities**:
1. Market Risk presents limit dashboard to MLRC
2. Review includes:
   - Current VaR and SVaR utilisation by level
   - Breaches in period (new and outstanding)
   - Temporary excesses (active and expiring)
   - Trend analysis and concerns
   - SVaR/VaR ratio analysis
3. MLRC challenges and approves actions
4. Decisions minuted

**Evidence**:
- MLRC agenda and pack
- MLRC minutes with decisions

### 5.14 VL-C14: System Limit Configuration Validation

| Attribute | Value |
|-----------|-------|
| **Control ID** | VL-C14 |
| **Objective** | Ensure limit changes are correctly implemented in systems |
| **Type** | Preventive |
| **Frequency** | On change |
| **Owner** | Risk Technology |

**Control Activities**:
1. Limit change request received from Market Risk (VaR and/or SVaR)
2. Four-eyes review of change request
3. Implement in TEST environment first
4. RAV validates configuration in TEST
5. Promote to PRODUCTION
6. RAV confirms PRODUCTION configuration

**Evidence**:
- Change Request ticket
- TEST validation sign-off
- PRODUCTION confirmation

---

## 6. VaR/SVaR Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        MERIDIAN GLOBAL BANK - VaR/SVaR DASHBOARD                        │
│                                   As at: [Date]                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ENTITY SUMMARY                                                                         │
│  ──────────────                                                                         │
│  │  Metric      │    Value    │   Limit   │   Util   │  Status  │                       │
│  ├──────────────┼─────────────┼───────────┼──────────┼──────────┤                       │
│  │  VaR         │   $18.5m    │   $25m    │   74%    │    🟢    │                       │
│  │  SVaR        │   $38.2m    │   $50m    │   76%    │    🟢    │                       │
│  │  SVaR/VaR    │   2.06x     │  1.5-2.5  │    -     │    🟢    │                       │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  DIVISION BREAKDOWN                                                                     │
│  ──────────────────                                                                     │
│                                                                                         │
│  MARKETS                              │  TREASURY                                       │
│  VaR:  $14.2m / $19m  (75%) 🟢        │  VaR:  $4.8m / $6m   (80%) 🟡                   │
│  SVaR: $29.1m / $38m  (77%) 🟢        │  SVaR: $9.5m / $12m  (79%) 🟢                   │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  BUSINESS UNIT HEAT MAP                                                                 │
│  ──────────────────────                                                                 │
│  │  Business Unit   │  VaR Util  │  SVaR Util │                                         │
│  ├──────────────────┼────────────┼────────────┤                                         │
│  │  Rates Trading   │  72% 🟢    │  75% 🟢    │                                         │
│  │  FX Trading      │  68% 🟢    │  71% 🟢    │                                         │
│  │  Credit Trading  │  85% 🟡    │  82% 🟡    │  ← Watch List                           │
│  │  Treasury        │  80% 🟡    │  79% 🟢    │  ← Watch List                           │
│                                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  WATCH LIST                                                                             │
│  ──────────────                                                                         │
│  • Credit Trading: VaR at 85%, approaching warning threshold                            │
│  • Treasury: VaR at warning threshold (80%)                                             │
│                                                                                         │
│  BREACHES                                                                               │
│  ─────────                                                                              │
│  • None currently                                                                       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Control Testing Schedule

| Control | Test Frequency | Test Type | Tester |
|---------|---------------|-----------|--------|
| VL-C01 | Monthly | Sample testing | Internal Audit |
| VL-C02 | Monthly | Sample testing | Internal Audit |
| VL-C03 | Quarterly | Walkthrough | Market Risk |
| VL-C04 | Quarterly | Sample testing | Internal Audit |
| VL-C05 | Semi-annually | Scenario testing | Operational Risk |
| VL-C06 | Quarterly | Sample testing | Internal Audit |
| VL-C07 | Monthly | Status review | Market Risk |
| VL-C08 | Quarterly | Sample testing | Internal Audit |
| VL-C09 | Monthly | Status review | Market Risk |
| VL-C10 | Monthly | Full reconciliation | RAV |
| VL-C11 | Monthly | Trend review | Market Risk |
| VL-C12 | Monthly | Ratio analysis | RAV |
| VL-C13 | Ongoing | Attendance/minutes | MLRC Secretary |
| VL-C14 | On change | Validation | RAV |

---

## 8. Key Risk Indicators (KRIs)

| KRI ID | Indicator | Threshold | Escalation |
|--------|-----------|-----------|------------|
| KRI-VL-01 | Number of VaR limit breaches per month | >5 | MLRC |
| KRI-VL-02 | Number of SVaR limit breaches per month | >3 | MLRC |
| KRI-VL-03 | Average breach remediation time (days) | >5 | MLRC |
| KRI-VL-04 | Outstanding temporary excesses | >3 | RMC |
| KRI-VL-05 | Entities at >80% VaR utilisation | >30% of entities | MLRC |
| KRI-VL-06 | Entities at >80% SVaR utilisation | >30% of entities | MLRC |
| KRI-VL-07 | SVaR/VaR ratio outside normal range | >5 days | Market Risk |
| KRI-VL-08 | Control test failures | Any | CRO |
| KRI-VL-09 | Limit hierarchy reconciliation breaks | >0 | Head of RAV |

---

## 9. Related Controls

| Control ID | Control Name | Relationship |
|------------|--------------|--------------|
| MR-L5-002 | Scenario Stress Limits Controls | Complementary - scenario-based tail risk |
| MR-L5-003 | Sensitivity Limit Controls | Complementary - granular risk factor limits |
| MR-L5-004 | Backtesting Exception Controls | Related - validates VaR/SVaR model |
| MR-L5-006 | Stop-Loss Controls | Complementary - P&L-based limits |
| MR-L5-007 | ECAP Controls | Related - ECAP extends VaR/SVaR to 99.9% for ICAAP |

---

## 10. Document Control

### 10.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |
| 1.1 | 2025-01-15 | Combined VaR and SVaR; updated currency to USD | MLRC |

### 10.2 Review Schedule

- Full review: Annually (January)
- Control effectiveness: Quarterly (via MLRC)
- Post-incident: Following any control failure

---

*End of Document*
