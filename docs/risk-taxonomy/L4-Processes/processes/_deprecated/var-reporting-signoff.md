---
# Process Metadata
process_id: MR-L4-007
process_name: VaR Reporting and Sign-off
version: 1.1
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Reporting, Analysis & Validation (RAV)
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
  - MR-L3-002   # MLRC Terms of Reference
  - MR-L3-003   # VaR Limit Framework
l5_controls:
  - MR-L5-001   # VaR Limits
  - MR-L5-004   # Backtesting Exception Limits
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-004  # Risk Reporting DataMart
  - SYS-MR-008  # Risk ODS
  - SYS-MR-009  # P&L ODS
---

# VaR Reporting and Sign-off Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-007 |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Market Risk Process Orchestration (MR-L4-001) |
| **Owner** | Head of Reporting, Analysis & Validation (RAV) |

---

## 1. Purpose

The VaR Reporting and Sign-off process ensures that VaR results are:

1. **Quality Controlled** - Validated before release to stakeholders
2. **Analysed** - Material changes explained and understood
3. **Reported** - Distributed to appropriate audiences in required formats
4. **Governed** - Formally signed off with clear accountability
5. **Actioned** - Limit breaches escalated per the VaR Limit Framework

This process is the final gate before VaR numbers are used for limit monitoring, regulatory reporting, and management decisions.

---

## 2. Scope

### 2.1 Reports and Outputs

| Output | Audience | Frequency | Purpose |
|--------|----------|-----------|---------|
| **VaR Dashboard** | Market Risk, Trading, MLRC | Daily | Real-time limit monitoring |
| **Limit Utilisation Report** | Desk Heads, Business Management | Daily | Position management |
| **Exception Report** | Market Risk, MLRC | Daily | Breach notification and escalation |
| **Backtesting Report** | Market Risk, RMA, MLRC | Daily | Model performance monitoring |
| **VaR Explain** | Market Risk, Trading | Daily | Material change analysis |
| **MLRC Risk Pack** | MLRC members | Weekly | Governance oversight |
| **Regulatory Capital Report** | Finance, Regulatory Reporting | Daily | IMA capital calculation |
| **Board Risk Report** | Board Risk Committee | Monthly | Strategic risk oversight |

### 2.2 Key Activities

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     VaR REPORTING AND SIGN-OFF - KEY ACTIVITIES                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  1. QUALITY CONTROL                                                                     │
│     • Completeness checks                                                               │
│     • Reasonableness validation                                                         │
│     • Reconciliation to prior day                                                       │
│                                                                                         │
│  2. BACKTESTING                                                                         │
│     • Clean vs. Dirty P&L comparison                                                    │
│     • Exception identification                                                          │
│     • Regulatory breach monitoring                                                      │
│                                                                                         │
│  3. VaR EXPLAIN                                                                         │
│     • Attribution of VaR changes                                                        │
│     • Material driver identification                                                    │
│     • Commentary preparation                                                            │
│                                                                                         │
│  4. LIMIT MONITORING                                                                    │
│     • Utilisation calculation                                                           │
│     • Breach identification                                                             │
│     • Escalation execution                                                              │
│                                                                                         │
│  5. SIGN-OFF AND DISTRIBUTION                                                           │
│     • Formal quality sign-off                                                           │
│     • Report generation                                                                 │
│     • Stakeholder distribution                                                          │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     VaR REPORTING AND SIGN-OFF PROCESS                                  │
│                     (Daily 04:00 - 07:30 GMT+1)                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [From Risk Engine Calculation (MR-L4-006)]
              │
              │   ┌─────────────────────────────────────────────────────────────────────┐
              │   │  INPUTS                                                             │
              │   │                                                                     │
              │   │  From Risk ODS:                                                     │
              │   │  • VaR by hierarchy (desk, business, entity)                        │
              │   │  • SVaR by hierarchy                                                │
              │   │  • IRC (from IRC Calculation MR-L4-010)                              │
              │   │  • Risk factor contributions                                        │
              │   │  • P&L strips (for investigation)                                   │
              │   │                                                                     │
              │   │  From P&L ODS:                                                      │
              │   │  • Actual P&L (T-1)                                                 │
              │   │  • Hypothetical P&L (T-1)                                           │
              │   │                                                                     │
              │   │  From VaR Limit Framework:                                          │
              │   │  • Limit structure by hierarchy                                     │
              │   │  • Escalation thresholds                                            │
              │   └─────────────────────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         1. QUALITY CONTROL                                               │
│                         (04:00 - 04:45 GMT+1)                                            │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  AUTOMATED QUALITY CHECKS                                                           │ │
│  │                                                                                     │ │
│  │  Check                           │ Threshold        │ Action if Failed              │ │
│  │  ─────────────────────────────────────────────────────────────────────────────────  │ │
│  │  VaR populated for all desks     │ 100%             │ Alert - investigate missing   │ │
│  │  VaR vs. T-1 change              │ ±50%             │ Flag for VaR explain          │ │
│  │  Negative VaR values             │ None allowed     │ Reject - calculation error    │ │
│  │  Entity VaR < Σ(Desk VaR)        │ Must be true     │ Flag - diversification check  │ │
│  │  SVaR/VaR ratio                  │ 1.5x - 4.0x      │ Flag - investigate outlier    │ │
│  │  Calculation batch errors        │ 0 errors         │ Alert - investigate cause     │ │
│  │                                                                                     │ │
│  │  If all checks pass → Proceed to backtesting                                        │ │
│  │  If checks fail → Investigation required before sign-off                            │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         2. BACKTESTING                                                   │
│                         (04:45 - 05:30 GMT+1)                                            │
│                                                                                          │
│  See VaR Backtesting Process (MR-L4-008) for detailed methodology                        │
│  Summary: Compare P&L to VaR, identify exceptions, update zone status                    │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         3. VaR EXPLAIN                                                   │
│                         (05:00 - 06:00 GMT+1)                                            │
│                                                                                          │
│  See Section 5 for detailed methodology                                                  │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         4. LIMIT MONITORING                                              │
│                         (05:30 - 06:30 GMT+1)                                            │
│                                                                                          │
│  See Section 6 for detailed methodology                                                  │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         5. SIGN-OFF AND DISTRIBUTION                                     │
│                         (06:30 - 07:30 GMT+1)                                            │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  SIGN-OFF WORKFLOW                                                                  │ │
│  │                                                                                     │ │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                  │ │
│  │  │ RAV Analyst     │───▶│ RAV Team Lead   │───▶│ Head of RAV     │                  │ │
│  │  │ Prepares        │    │ Reviews         │    │ Signs off       │                  │ │
│  │  │ • QC results    │    │ • Material items│    │ • Final approval│                  │ │
│  │  │ • Backtest      │    │ • VaR explain   │    │ • Release auth  │                  │ │
│  │  │ • VaR explain   │    │ • Breaches      │    │                 │                  │ │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘                  │ │
│  │                                                         │                           │ │
│  │                                                         ▼                           │ │
│  │                                             ┌─────────────────────┐                 │ │
│  │                                             │ RELEASE REPORTS     │                 │ │
│  │                                             │                     │                 │ │
│  │                                             │ • VaR Dashboard     │                 │ │
│  │                                             │ • Limit Report      │                 │ │
│  │                                             │ • Exception Report  │                 │ │
│  │                                             │ • Backtest Report   │                 │ │
│  │                                             │ • Regulatory feed   │                 │ │
│  │                                             └─────────────────────┘                 │ │
│  │                                                                                     │ │
│  │  Sign-off SLA: 07:00 GMT+1                                                          │ │
│  │  Distribution SLA: 07:30 GMT+1                                                      │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                                 [Reports Distributed to Stakeholders]
```

---

## 4. Backtesting

> **Note**: Detailed backtesting methodology, price source alignment, and exception analysis have been extracted to the standalone [VaR Backtesting Process (MR-L4-008)](./backtesting.md). This section provides a summary for the VaR Reporting workflow.

### 4.1 Purpose

Backtesting compares actual/hypothetical P&L to VaR predictions to assess model accuracy and determine the regulatory capital multiplier per the Basel traffic light system.

### 4.2 Daily Backtesting in VaR Reporting

| Step | Activity | Output |
|------|----------|--------|
| **1** | Retrieve VaR (T-1) from Risk Engine | VaR prediction |
| **2** | Retrieve Hypothetical and Actual P&L (T-1) from P&L ODS | P&L for comparison |
| **3** | Compare \|P&L\| to VaR - if exceeded, flag exception | Exception flag |
| **4** | Update rolling 250-day exception count | Zone status |
| **5** | If exception, invoke backtesting process for root cause analysis | Exception report |

### 4.3 Zone Status Summary

| Zone | Exceptions | Capital Multiplier | Implication |
|------|-----------|-------------------|-------------|
| **GREEN** | 0-4 | 3.0x | Normal operations |
| **YELLOW** | 5-9 | 3.4x - 3.85x | Investigation required |
| **RED** | ≥10 | 4.0x | Remediation required |

### 4.4 Reporting

| Recipient | Content | Frequency |
|-----------|---------|-----------|
| **MLRC** | Exception count, zone status, root cause analysis | Weekly pack |
| **RMA** | Model performance, exception trends, remediation progress | Monthly |
| **PRA** | Rolling exception count, zone status, multiplier | Quarterly |

### 4.5 Reference

For detailed methodology including:
- Hypothetical vs. Actual P&L definitions
- Price source alignment and backtesting noise
- Exception classification framework
- Root cause analysis procedures

See: **[VaR Backtesting Process (MR-L4-008)](./backtesting.md)**

---

## 5. VaR Explain

### 5.1 Purpose

VaR Explain provides attribution of VaR changes to help stakeholders understand:
- Why VaR changed from prior day
- Which desks/risk factors drove the change
- Whether the change is expected or anomalous

### 5.2 VaR Change Attribution

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     VaR CHANGE ATTRIBUTION                                               │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  TOTAL VaR CHANGE = New Business + Position Change + Market Data + Methodology           │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                     │ │
│  │  COMPONENT              DESCRIPTION                      TYPICAL DRIVER             │ │
│  │  ─────────────────────────────────────────────────────────────────────────────────  │ │
│  │                                                                                     │ │
│  │  New Business           VaR from new trades entered      Large new position         │ │
│  │  (Trade Effect)         since prior day                  significant deal           │ │
│  │                                                                                     │ │
│  │  Position Change        VaR change from existing         Hedging, rebalancing       │ │
│  │  (Delta Effect)         position changes (non-new)       risk reduction             │ │
│  │                                                                                     │ │
│  │  Market Data            VaR change from updated          Volatility change          │ │
│  │  (Market Effect)        market prices/scenarios          new scenario in window     │ │
│  │                                                                                     │ │
│  │  Methodology            VaR change from model/param      Stressed period change     │ │
│  │  (Model Effect)         updates (rare, documented)       proxy methodology          │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  CALCULATION APPROACH:                                                                   │
│                                                                                          │
│  1. VaR(T-1 positions, T-1 market data) = Baseline VaR                                   │
│  2. VaR(T-1 positions, T market data) = Baseline + Market Effect                         │
│  3. VaR(T positions, T market data) = Baseline + Market Effect + Position Effect         │
│  4. New Business isolated by flagging trades entered on T                                │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Material Change Thresholds

| Change Type | Threshold | Action |
|-------------|-----------|--------|
| **Entity VaR change** | >10% or >$1M | VaR explain required |
| **Desk VaR change** | >20% or >$500k | VaR explain required |
| **Risk factor contribution change** | >30% | Investigate driver |
| **SVaR/VaR ratio change** | >0.5 | Investigate driver |

### 5.4 VaR Explain Report Format

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     DAILY VaR EXPLAIN REPORT                                            │
│                     Date: 15-Jan-2025                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  SUMMARY                                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Entity: Meridian Bank UK                                                               │
│  VaR (T): $8.5M                                                                         │
│  VaR (T-1): $7.8M                                                                       │
│  Change: +$700k (+9%)                                                                   │
│                                                                                         │
│  ATTRIBUTION                                                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  New Business Effect:      +$150k   Large EUR rates trade (EUR-RATES-LON-01)            │
│  Position Change Effect:   -$200k   G10 FX desk reduced USD/JPY exposure                │
│  Market Data Effect:       +$750k   Higher volatility in EUR rates scenarios            │
│  Methodology Effect:       $0       No methodology changes                              │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  TOTAL CHANGE:             +$700k                                                       │
│                                                                                         │
│  TOP DRIVERS (By Desk)                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  1. EUR Rates London:      +$550k   New 10Y swap position + higher vol scenarios        │
│  2. G10 FX London:         -$250k   USD/JPY exposure reduction                          │
│  3. Credit Trading:        +$300k   Credit spread widening in scenarios                 │
│  4. Other (net):           +$100k   Various small changes                               │
│                                                                                         │
│  COMMENTARY                                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  VaR increase driven primarily by higher EUR rates volatility entering the lookback     │
│  window (ECB meeting minutes released 13-Jan). New EUR rates trade adds incremental     │
│  risk, partially offset by FX desk risk reduction.                                      │
│                                                                                         │
│  Prepared by: RAV Team                                                                  │
│  Reviewed by: RAV Team Lead                                                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Limit Monitoring

### 6.1 Limit Structure

VaR limits are set at multiple hierarchy levels per the VaR Limit Framework:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     VaR LIMIT STRUCTURE                                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  HIERARCHY LEVEL        LIMIT TYPE           APPROVING AUTHORITY                        │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  Enterprise             Appetite Limit       Board (via Risk Appetite Statement)        │
│  │                      $25M (illustrative)                                             │
│  │                                                                                      │
│  └─ Legal Entity        Entity Limit         MLRC                                       │
│     │                   Meridian UK: $15M                                               │
│     │                                                                                   │
│     └─ Division         Division Limit       MLRC                                       │
│        │                Global Markets: $12M                                            │
│        │                                                                                │
│        └─ Business      Business Limit       MLRC (delegated to Market Risk)            │
│           │             Rates Trading: $8M                                              │
│           │                                                                             │
│           └─ Desk       Desk Limit           Market Risk (within delegation)            │
│              │          EUR Rates: $4M                                                  │
│              │                                                                          │
│              └─ Book    Book Limit           Desk Head (within desk allocation)         │
│                         EUR-RATES-LON-01: $2M                                           │
│                                                                                         │
│  Note: Limits at higher levels are typically less than sum of children (diversification)│
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Utilisation Calculation

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     LIMIT UTILISATION CALCULATION                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Utilisation % = (VaR ÷ VaR Limit) × 100%                                               │
│                                                                                         │
│  EXAMPLE:                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  EUR Rates London Desk                                                                  │
│  VaR (99%, 1-day): $3.2M                                                                │
│  VaR Limit: $4.0M                                                                       │
│  Utilisation: 80%                                                                       │
│                                                                                         │
│  STATUS INDICATORS:                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │                                                                                     ││
│  │  Utilisation    │  Status    │  Indicator │  Action                                 ││
│  │  ─────────────────────────────────────────────────────────────────────────────      ││
│  │  0% - 80%       │  GREEN     │  ●         │  Normal operations                      ││
│  │  80% - 90%      │  AMBER     │  ●         │  Alert desk head; monitor closely       ││
│  │  90% - 100%     │  RED       │  ●         │  Warning to desk; prepare for breach    ││
│  │  >100%          │  BREACH    │  ⚠         │  Immediate escalation per framework     ││
│  │                                                                                     ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Breach Escalation

| Breach Level | Definition | Escalation | Timeline | Authority |
|--------------|------------|------------|----------|-----------|
| **Book** | Book VaR > Book Limit | Desk Head notified | Immediate | Desk Head can reallocate within desk |
| **Desk** | Desk VaR > Desk Limit | Market Risk + Business Head | Within 1 hour | Market Risk can grant temporary |
| **Business** | Business VaR > Business Limit | MLRC notification | Within 2 hours | MLRC decision required |
| **Entity** | Entity VaR > Entity Limit | MLRC + CRO | Immediate | MLRC emergency meeting |
| **Enterprise** | Enterprise VaR > Appetite | Board Risk Committee | Immediate | CRO escalation to Board |

### 6.4 Breach Response Actions

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     BREACH RESPONSE FRAMEWORK                                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  STEP 1: IMMEDIATE NOTIFICATION (Within 30 minutes of VaR report)                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • RAV notifies Market Risk of breach                                                   │
│  • Market Risk notifies Desk Head and Business Head                                     │
│  • Breach logged in exception tracking system                                           │
│                                                                                         │
│  STEP 2: ROOT CAUSE ANALYSIS (Within 2 hours)                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Identify driver of breach (new trade, market move, methodology)                      │
│  • Assess if breach is temporary or structural                                          │
│  • Prepare options for risk reduction if required                                       │
│                                                                                         │
│  STEP 3: REMEDIATION DECISION (Per escalation authority)                                │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Option A: Temporary Excess Approval                                                    │
│  • Limited duration (1-5 days)                                                          │
│  • Conditions attached (e.g., no new risk)                                              │
│  • Requires MLRC approval for desk+ level                                               │
│                                                                                         │
│  Option B: Risk Reduction                                                               │
│  • Desk instructed to reduce VaR to within limit                                        │
│  • Timeline specified (intraday, EOD, T+1)                                              │
│  • Progress monitored                                                                   │
│                                                                                         │
│  Option C: Limit Increase Request                                                       │
│  • If breach reflects legitimate business need                                          │
│  • Requires formal MLRC approval                                                        │
│  • Supported by business case                                                           │
│                                                                                         │
│  STEP 4: DOCUMENTATION AND FOLLOW-UP                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  • Breach recorded in exception log                                                     │
│  • Daily monitoring until resolved                                                      │
│  • Post-incident review if material or repeated                                         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Sign-off and Distribution

### 7.1 Sign-off Authority

| Sign-off Level | Authority | Scope | Conditions |
|----------------|-----------|-------|------------|
| **Standard** | RAV Team Lead | Normal day, no issues | All QC checks pass |
| **With Issues** | Head of RAV | Minor issues documented | Issues explained, manageable |
| **Escalated** | Head of Market Risk | Material issues | Requires investigation |
| **Emergency** | CRO | Production failure | BCP in effect |

### 7.2 Sign-off Checklist

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     DAILY VAR SIGN-OFF CHECKLIST                                        │
│                     Date: ______________                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  QUALITY CONTROL                                            Status    Initials          │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  □ All desks have VaR calculated                            [ PASS ]  ______            │
│  □ No negative VaR values                                   [ PASS ]  ______            │
│  □ Diversification check passes (Entity < Σ Desk)           [ PASS ]  ______            │
│  □ VaR change vs. T-1 within threshold or explained         [ PASS ]  ______            │
│  □ SVaR/VaR ratio within expected range                     [ PASS ]  ______            │
│  □ Calculation batch completed without errors               [ PASS ]  ______            │
│                                                                                         │
│  BACKTESTING                                                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  □ Backtest performed for T-1                               [ PASS ]  ______            │
│  □ Exception status recorded (Y/N)                          [ NO   ]  ______            │
│  □ Rolling 250-day count: ____                              [ 3    ]  ______            │
│  □ Zone status: GREEN / YELLOW / RED                        [ GREEN]  ______            │
│                                                                                         │
│  VAR EXPLAIN (If material change)                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  □ Attribution analysis completed                           [ PASS ]  ______            │
│  □ Top drivers identified                                   [ PASS ]  ______            │
│  □ Commentary prepared                                      [ PASS ]  ______            │
│                                                                                         │
│  LIMIT MONITORING                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  □ Limit utilisation calculated for all levels              [ PASS ]  ______            │
│  □ Breaches identified and escalated (Y/N)                  [ NO   ]  ______            │
│  □ Amber/Red warnings notified                              [ N/A  ]  ______            │
│                                                                                         │
│  SIGN-OFF                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Prepared by: _________________ (RAV Analyst)      Time: ______                         │
│  Reviewed by: _________________ (RAV Team Lead)    Time: ______                         │
│  Approved by: _________________ (Head of RAV)      Time: ______                         │
│                                                                                         │
│  VaR RELEASE AUTHORISED: □ YES   □ NO (If NO, state reason below)                       │
│                                                                                         │
│  Notes: ___________________________________________________________________             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Report Distribution

| Report | Recipients | Format | Timing | Channel |
|--------|------------|--------|--------|---------|
| **VaR Dashboard** | Trading desks, Market Risk | Interactive web | 07:00 | Risk Portal |
| **Limit Utilisation** | Desk Heads, Business Heads | PDF/Excel | 07:15 | Email |
| **Exception Report** | Market Risk, MLRC | PDF | 07:15 | Email |
| **Backtest Report** | Market Risk, RMA | PDF | 07:15 | Email |
| **Regulatory Feed** | Finance, Regulatory Reporting | Data file | 07:30 | Automated feed |
| **MLRC Pack** | MLRC members | PDF | Weekly (Fri) | Email |

---

## 8. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| RSO-C01 | All QC checks must pass or be explained before sign-off | Preventive | RAV |
| RSO-C02 | Backtesting performed daily with exception tracking | Detective | RAV |
| RSO-C03 | Material VaR changes (>10% or >$1M) require VaR explain | Detective | RAV |
| RSO-C04 | Limit utilisation calculated for all hierarchy levels | Detective | RAV |
| RSO-C05 | Breaches escalated within 1 hour per framework | Detective | Market Risk |
| RSO-C06 | Sign-off obtained before report distribution | Preventive | RAV |
| RSO-C07 | All reports distributed by SLA (07:30) | Detective | RAV |
| RSO-C08 | Exception log maintained with full audit trail | Detective | Market Risk |
| RSO-C09 | Weekly MLRC reporting of VaR trends and exceptions | Detective | RAV |

---

## 9. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| QC complete | 04:45 GMT+1 | 05:00 GMT+1 | RAV Team Lead |
| Backtesting complete | 05:30 GMT+1 | 05:45 GMT+1 | RAV Team Lead |
| VaR explain complete (if required) | 06:00 GMT+1 | 06:15 GMT+1 | RAV Manager |
| Limit monitoring complete | 06:30 GMT+1 | 06:45 GMT+1 | RAV Manager |
| Sign-off obtained | 07:00 GMT+1 | 07:15 GMT+1 | Head of RAV |
| **Reports distributed** | **07:30 GMT+1** | **08:00 GMT+1** | **Head of Market Risk** |
| Breach notification | Within 30 mins | Within 1 hour | Market Risk Manager |

---

## 10. Exception Handling

### 10.1 Process Exceptions

| Exception | Cause | Resolution | Escalation |
|-----------|-------|------------|------------|
| **QC failure** | Data quality issue | Investigate; re-run if needed | RAV Manager |
| **Sign-off delay** | Investigation required | Partial release possible | Head of RAV |
| **Report delay** | System issue | Manual distribution | RAV + IT |
| **Backtest data missing** | P&L ODS issue | Use T-2 data with flag | RAV Team Lead |

### 10.2 Override Authority

In exceptional circumstances, reports may be released with known issues:

| Scenario | Authority | Conditions |
|----------|-----------|------------|
| Minor data quality issue | RAV Team Lead | Issue documented; not material |
| Partial VaR (some desks missing) | Head of RAV | Missing desks <10% of total VaR |
| Delayed sign-off | Head of Market Risk | Preliminary figures released with caveat |
| Full production failure | CRO | BCP figures with confidence interval |

---

## 11. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [Risk Engine Calculation](./risk-engine-calculation.md) | Upstream - provides VaR data |
| [VaR Backtesting](./backtesting.md) | Sub-process - detailed backtesting methodology |
| [VaR Limit Framework](../L3-Governance/policies/var-limit-framework.md) | Governance - limit structure |
| [MLRC Terms of Reference](../L3-Governance/committees/mlrc-terms-of-reference.md) | Governance - committee oversight |
| [Market Risk Policy](../L3-Governance/policies/market-risk-policy.md) | Parent policy |

---

## 12. Document Control

### 12.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |
| 1.1 | 2025-01-15 | Slimmed Section 4 (Backtesting) to reference standalone MR-L4-008 process | MLRC |

---

*End of Document*
