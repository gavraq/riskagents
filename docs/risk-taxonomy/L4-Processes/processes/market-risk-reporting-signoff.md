---
# Process Metadata
process_id: MR-L4-007
process_name: Market Risk Reporting and Sign-off
version: 2.2
effective_date: 2025-01-17
next_review_date: 2026-01-17
owner: Head of Reporting, Analysis & Validation (RAV)
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-001  # Market Risk Process Orchestration
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
  - GOV-L3-010  # Risk Appetite Statement (EaR/ECAP limits)
  - GOV-L3-011  # Risk Appetite Framework
l5_controls:
  - MR-L5-001   # VaR Limits
  - MR-L5-002   # Stress Limits
  - MR-L5-003   # Sensitivity Limits
  - MR-L5-004   # Backtesting Exception Limits
  - MR-L5-007   # ECAP and EaR Controls
l7_systems:
  - SYS-MR-003  # Risk Engine
  - SYS-MR-004  # Risk Reporting DataMart
  - SYS-MR-008  # Risk ODS
  - SYS-MR-009  # P&L ODS
---

# Market Risk Reporting and Sign-off Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-007 |
| **Version** | 2.2 |
| **Effective Date** | 17 January 2025 |
| **Parent Process** | Market Risk Process Orchestration (MR-L4-001) |
| **Owner** | Head of Reporting, Analysis & Validation (RAV) |

---

## 1. Purpose

The Market Risk Reporting and Sign-off process ensures that **all market risk metrics** from the three Risk Engine calculation streams are:

1. **Quality Controlled** - Validated before release to stakeholders
2. **Analysed** - Material changes explained and understood
3. **Reported** - Distributed to appropriate audiences in required formats
4. **Governed** - Formally signed off with clear accountability

This process covers reporting and sign-off for:
- **Stream 1: Sensitivities & Position Reporting** (intraday)
- **Stream 2: VaR/SVaR Reporting** (daily)
- **Stream 3: Stress Testing Reporting** (daily/weekly)

> **Note**: Limit monitoring and breach management have been extracted to [Market Risk Limits Management (MR-L4-013)](./market-risk-limits-management.md), which covers the full limits lifecycle from setup through monitoring.

---

## 2. Scope

### 2.1 Three Reporting Streams

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     MARKET RISK REPORTING - THREE STREAMS                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │                    STREAM 1: SENSITIVITIES & POSITION REPORTING                     ││
│  │                                                                                     ││
│  │  FREQUENCY: Intraday (hourly refresh)                                               ││
│  │  SOURCE: Risk Engine - Sensitivities Aggregation                                    ││
│  │                                                                                     ││
│  │  REPORTS:                                                                           ││
│  │  • Sensitivity Dashboard (DV01, CS01, Vega, Delta by desk/entity)                   ││
│  │  • Position Reporting (notional, Greeks by product/currency)                        ││
│  │  • Concentration Report (by issuer, curve, currency, sector)                        ││
│  │  • Intraday Limit Utilisation (sensitivity limits)                                  ││
│  │                                                                                     ││
│  │  PRIMARY CONSUMERS: FO Traders, Desk Heads, Market Risk (intraday monitoring)       ││
│  │  SIGN-OFF: Automated validation; manual review only for exceptions                  ││
│  │                                                                                     ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │                    STREAM 2: VaR / SVaR REPORTING                                   ││
│  │                                                                                     ││
│  │  FREQUENCY: Daily (T+1 overnight batch)                                             ││
│  │  SOURCE: Risk Engine - VaR/SVaR Calculation                                         ││
│  │                                                                                     ││
│  │  REPORTS:                                                                           ││
│  │  • VaR Dashboard (VaR/SVaR by hierarchy with trend)                                 ││
│  │  • Risk Factor Contribution Report                                                  ││
│  │  • VaR Explain Report (material changes)                                            ││
│  │  • Backtesting Report (P&L vs VaR, exception tracking)                              ││
│  │  • Regulatory Capital Report (IMA capital components)                               ││
│  │  • MLRC Risk Pack (weekly consolidation)                                            ││
│  │                                                                                     ││
│  │  PRIMARY CONSUMERS: Market Risk, MLRC, Regulatory Reporting, Board                  ││
│  │  SIGN-OFF: Full RAV sign-off workflow (see Section 7)                               ││
│  │                                                                                     ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐│
│  │                    STREAM 3: STRESS TESTING REPORTING                               ││
│  │                                                                                     ││
│  │  FREQUENCY: Daily (overnight batch) + Weekly (full suite)                           ││
│  │  SOURCE: Risk Engine - Stress Testing Calculation                                   ││
│  │                                                                                     ││
│  │  REPORTS:                                                                           ││
│  │  • Stress Dashboard (P&L by scenario and hierarchy)                                 ││
│  │  • Stress Limit Utilisation Report                                                  ││
│  │  • Worst Scenario Analysis                                                          ││
│  │  • Stress vs VaR Comparison Report                                                  ││
│  │  • Pillar Stress Report (firm-wide scenarios)                                       ││
│  │  • Point of Weakness Report (portfolio-specific scenarios)                          ││
│  │  • ICAAP/Capital Planning Pack (quarterly)                                          ││
│  │                                                                                     ││
│  │  PRIMARY CONSUMERS: Market Risk, MLRC, Capital Planning, Board, Regulators          ││
│  │  SIGN-OFF: Full RAV sign-off workflow (see Section 7)                               ││
│  │                                                                                     ││
│  └─────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Report Inventory

| Report | Stream | Frequency | Audience | Format |
|--------|--------|-----------|----------|--------|
| **Sensitivity Dashboard** | 1 | Intraday | FO, Market Risk | Web portal |
| **Position Report** | 1 | Intraday | FO, Market Risk | Web/Excel |
| **Concentration Report** | 1 | Daily | Market Risk, MLRC | PDF/Excel |
| **VaR Dashboard** | 2 | Daily | Market Risk, FO, MLRC | Web portal |
| **VaR Explain Report** | 2 | Daily (if material) | Market Risk, Trading | PDF |
| **Risk Factor Contribution** | 2 | Daily | Market Risk, RMA | Excel |
| **Backtesting Report** | 2 | Daily | Market Risk, RMA | PDF |
| **Regulatory Capital Report** | 2 | Daily | Finance, Regulatory | Data feed |
| **EaR Report** | 2 | Daily | ExCo, ALCO, BRMC (vs Risk Appetite) | Web portal/Data feed |
| **ECAP Report** | 2 | Daily | Capital Planning, ALCO | Data feed |
| **Stress Dashboard** | 3 | Daily | Market Risk, MLRC | Web portal |
| **Stress Limit Report** | 3 | Daily | Market Risk, Trading | PDF |
| **Pillar Stress Report** | 3 | Weekly | MLRC, Board | PDF |
| **PoW Stress Report** | 3 | Weekly | Market Risk, Trading | PDF |
| **MLRC Risk Pack** | All | Weekly | MLRC members | PDF |
| **Board Risk Report** | All | Monthly | Board Risk Committee | PDF |
| **ICAAP Pack** | 2, 3 | Quarterly | Capital Planning, PRA | PDF |

---

## 3. Process Flow - Daily Reporting Cycle

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     DAILY MARKET RISK REPORTING CYCLE                                   │
│                     (04:00 - 08:00 GMT+1)                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [From Risk Engine Calculation Streams]
              │
              │   ┌─────────────────────────────────────────────────────────────────────┐
              │   │  INPUTS (from Risk ODS)                                             │
              │   │                                                                     │
              │   │  Stream 1: Aggregated sensitivities by hierarchy                    │
              │   │  Stream 2: VaR/SVaR by hierarchy, risk factor contributions         │
              │   │  Stream 3: Stress P&L by scenario and hierarchy                     │
              │   │  P&L ODS: Actual and Hypothetical P&L (for backtesting)             │
              │   └─────────────────────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         1. QUALITY CONTROL - ALL STREAMS                                 │
│                         (04:00 - 04:45 GMT+1)                                            │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │  AUTOMATED QC CHECKS                                                                │ │
│  │                                                                                     │ │
│  │  STREAM 2 (VaR/SVaR):                          STREAM 3 (Stress):                   │ │
│  │  • VaR populated for all desks (100%)          • Stress P&L for all scenarios       │ │
│  │  • No negative VaR values                      • All hierarchy levels populated     │ │
│  │  • VaR vs T-1 change (±50% threshold)          • Stress vs T-1 change (±30%)        │ │
│  │  • Entity VaR < Σ(Desk VaR)                    • Worst scenario identified          │ │
│  │  • SVaR/VaR ratio (1.5x - 4.0x)                • Scenario completeness check        │ │
│  │  • No calculation batch errors                 • No calculation batch errors        │ │
│  │                                                                                     │ │
│  │  If checks pass → Proceed to analysis                                               │ │
│  │  If checks fail → Investigation required; escalate to RAV Team Lead                 │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         2. BACKTESTING (Stream 2)                                        │
│                         (04:45 - 05:30 GMT+1)                                            │
│                                                                                          │
│  See VaR Backtesting Process (MR-L4-008) for detailed methodology                        │
│  Summary: Compare P&L to VaR, identify exceptions, update zone status                    │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         3. EXPLAIN ANALYSIS - ALL STREAMS                                │
│                         (05:00 - 06:00 GMT+1)                                            │
│                                                                                          │
│  See Section 5 for VaR Explain methodology                                               │
│  See Section 6 for Stress Explain methodology                                            │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         4. SIGN-OFF AND DISTRIBUTION                                     │
│                         (06:00 - 07:30 GMT+1)                                            │
│                                                                                          │
│  See Section 7 for sign-off workflow                                                     │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                                 [Reports Distributed to Stakeholders]
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         5. LIMIT MONITORING (Continuous)                                 │
│                         (From 07:30 onwards)                                             │
│                                                                                          │
│  Limit monitoring is a continuous process managed separately.                            │
│  See Market Risk Limits Management (MR-L4-013) for:                                      │
│  • Limit setup and amendments                                                            │
│  • Daily limit utilisation monitoring                                                    │
│  • Breach escalation and management                                                      │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Quality Control

### 4.1 Stream 1 QC (Sensitivities)

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Sensitivities populated for all desks | 100% | Alert - investigate missing |
| No missing risk factor mappings | 0 gaps | Flag positions without Greeks |
| Intraday refresh on schedule | Hourly | Alert IT - system issue |
| Aggregation integrity | Sum of children = parent | Investigate calculation |

### 4.2 Stream 2 QC (VaR/SVaR)

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| VaR populated for all desks | 100% | Alert - investigate missing |
| VaR vs. T-1 change | ±50% | Flag for VaR explain |
| Negative VaR values | None allowed | Reject - calculation error |
| Entity VaR < Σ(Desk VaR) | Must be true | Flag - diversification check |
| SVaR/VaR ratio | 1.5x - 4.0x | Flag - investigate outlier |
| Calculation batch errors | 0 errors | Alert - investigate cause |

### 4.3 Stream 3 QC (Stress)

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Stress P&L for all scenarios | 100% | Alert - investigate missing |
| Stress P&L vs. T-1 change | ±30% | Flag for Stress explain |
| All hierarchy levels populated | 100% | Alert - aggregation issue |
| Worst scenario consistent | Same or explained | Flag for analysis |
| Scenario parameter reconciliation | Match Golden Source | Alert - param mismatch |

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
│                     Date: 16-Jan-2025                                                   │
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

## 6. Stress Explain

### 6.1 Purpose

Stress Explain provides attribution of stress P&L changes across scenarios to help stakeholders understand:
- Why stress results changed from prior day/week
- Which scenarios show increasing/decreasing risk
- What drove changes in worst-case outcomes

### 6.2 Stress Change Attribution

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     STRESS P&L CHANGE ATTRIBUTION                                        │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  TOTAL STRESS P&L CHANGE (per scenario) = Position Change + Scenario Parameter Change    │
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                     │ │
│  │  COMPONENT              DESCRIPTION                      TYPICAL DRIVER             │ │
│  │  ─────────────────────────────────────────────────────────────────────────────────  │ │
│  │                                                                                     │ │
│  │  Position Change        Stress P&L change from           New trades, hedging        │ │
│  │  (Same scenario)        position movements               risk reduction             │ │
│  │                                                                                     │ │
│  │  Scenario Parameter     Stress P&L change from           Annual review, MLRC        │ │
│  │  Change                 updated scenario shocks          approval of new params     │ │
│  │                                                                                     │ │
│  │  New Scenario           Addition of new scenario         PoW identified, regulatory │ │
│  │                         to monitoring suite              requirement                │ │
│  │                                                                                     │ │
│  └─────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                          │
│  UNLIKE VaR: No "Market Data Effect" because stress scenarios use predefined shocks     │
│  (from MLRC-approved Golden Source) not rolling historical windows                       │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Material Change Thresholds (Stress)

| Change Type | Threshold | Action |
|-------------|-----------|--------|
| **Entity Stress P&L change (any scenario)** | >15% or >$5M | Stress explain required |
| **Worst scenario change** | Different scenario | Investigate and document |
| **Stress limit utilisation change** | >10% | Monitor closely |
| **New scenario breaching limit** | Any | Immediate escalation |

### 6.4 Stress Explain Report Format

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     DAILY STRESS EXPLAIN REPORT                                         │
│                     Date: 16-Jan-2025                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ENTITY SUMMARY: Meridian Bank UK                                                       │
│                                                                                         │
│  STRESS RESULTS BY SCENARIO                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Scenario                  │ T Stress P&L │ T-1 Stress P&L │ Change  │ % Limit │ Status│
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Global Financial Crisis   │    -$125M    │     -$118M     │  -$7M   │   83%   │ 🟡    │
│  COVID-19 Shock            │     -$88M    │      -$92M     │  +$4M   │   88%   │ 🟡    │
│  Rates +200bp              │     -$65M    │      -$62M     │  -$3M   │   81%   │ 🟡    │
│  EM Crisis                 │     -$52M    │      -$55M     │  +$3M   │   69%   │ 🟢    │
│  EUR Breakup (PoW)         │     -$45M    │      -$40M     │  -$5M   │   N/A   │ New   │
│                                                                                         │
│  WORST SCENARIO: Global Financial Crisis (-$125M)                                       │
│  WORST SCENARIO T-1: Global Financial Crisis (-$118M)                                   │
│  CHANGE IN WORST: +$7M increase in loss (position-driven)                               │
│                                                                                         │
│  ATTRIBUTION - GLOBAL FINANCIAL CRISIS                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Position Change Effect:   -$7M    Increased EUR rates exposure (new 10Y swap)          │
│  Scenario Parameter:       $0M     No parameter changes                                 │
│                                                                                         │
│  TOP DRIVERS (GFC Scenario)                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  1. EUR Rates London:      -$4M    New swap position sensitive to rate falls            │
│  2. Credit Trading:        -$2M    Spread widening impact on IG book                    │
│  3. G10 FX:                -$1M    EUR depreciation impact                              │
│                                                                                         │
│  NEW SCENARIO ANALYSIS: EUR Breakup (Point of Weakness)                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Scenario added following Top Risk Analysis identifying EUR redenomination as           │
│  material idiosyncratic risk for current portfolio. MLRC approved 15-Jan-2025.          │
│  Stress P&L: -$45M (no limit assigned - monitoring phase)                               │
│                                                                                         │
│  Prepared by: RAV Team                                                                  │
│  Reviewed by: RAV Team Lead                                                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Sign-off Workflow

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
│                     DAILY MARKET RISK SIGN-OFF CHECKLIST                                │
│                     Date: ______________                                                │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  STREAM 2: VaR/SVaR/EaR/ECAP                                 Status    Initials         │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  □ All desks have VaR calculated                            [ PASS ]  ______            │
│  □ No negative VaR values                                   [ PASS ]  ______            │
│  □ Diversification check passes (Entity < Σ Desk)           [ PASS ]  ______            │
│  □ VaR change vs. T-1 within threshold or explained         [ PASS ]  ______            │
│  □ SVaR/VaR ratio within expected range                     [ PASS ]  ______            │
│  □ EaR calculated for all entities                          [ PASS ]  ______            │
│  □ EaR vs Risk Appetite limits checked (Green/Amber/Red)    [ PASS ]  ______            │
│  □ ECAP calculated for all entities                         [ PASS ]  ______            │
│  □ ECAP vs. Regulatory Capital reconciliation performed     [ PASS ]  ______            │
│  □ Backtest performed; exception status recorded            [ PASS ]  ______            │
│  □ VaR explain completed (if material change)               [ PASS ]  ______            │
│                                                                                         │
│  STREAM 3: STRESS                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  □ All scenarios calculated                                 [ PASS ]  ______            │
│  □ All hierarchy levels populated                           [ PASS ]  ______            │
│  □ Stress change vs. T-1 within threshold or explained      [ PASS ]  ______            │
│  □ Worst scenario identified and documented                 [ PASS ]  ______            │
│  □ Scenario parameters reconciled to Golden Source          [ PASS ]  ______            │
│  □ Stress explain completed (if material change)            [ PASS ]  ______            │
│                                                                                         │
│  SIGN-OFF                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│  Prepared by: _________________ (RAV Analyst)      Time: ______                         │
│  Reviewed by: _________________ (RAV Team Lead)    Time: ______                         │
│  Approved by: _________________ (Head of RAV)      Time: ______                         │
│                                                                                         │
│  RELEASE AUTHORISED: □ YES   □ NO (If NO, state reason below)                           │
│                                                                                         │
│  Notes: ___________________________________________________________________             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Sign-off Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     SIGN-OFF WORKFLOW                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐                      │
│  │ RAV Analyst     │───▶│ RAV Team Lead   │───▶│ Head of RAV     │                      │
│  │ Prepares        │    │ Reviews         │    │ Signs off       │                      │
│  │ • QC results    │    │ • Material items│    │ • Final approval│                      │
│  │ • Backtest      │    │ • VaR explain   │    │ • Release auth  │                      │
│  │ • VaR explain   │    │ • Stress explain│    │                 │                      │
│  │ • Stress explain│    │ • Completeness  │    │                 │                      │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘                      │
│                                                         │                               │
│                                                         ▼                               │
│                                             ┌─────────────────────┐                     │
│                                             │ RELEASE REPORTS     │                     │
│                                             │                     │                     │
│                                             │ Stream 2:           │                     │
│                                             │ • VaR Dashboard     │                     │
│                                             │ • Risk Factor Rpt   │                     │
│                                             │ • Backtest Report   │                     │
│                                             │ • Regulatory Feed   │                     │
│                                             │                     │                     │
│                                             │ Stream 3:           │                     │
│                                             │ • Stress Dashboard  │                     │
│                                             │ • Pillar Stress Rpt │                     │
│                                             │ • PoW Stress Rpt    │                     │
│                                             └─────────────────────┘                     │
│                                                                                         │
│  Sign-off SLA: 07:00 GMT+1                                                              │
│  Distribution SLA: 07:30 GMT+1                                                          │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Report Distribution

### 8.1 Distribution Schedule

| Report | Recipients | Format | Timing | Channel |
|--------|------------|--------|--------|---------|
| **VaR Dashboard** | Trading desks, Market Risk | Interactive web | 07:00 | Risk Portal |
| **Stress Dashboard** | Market Risk, Trading | Interactive web | 07:00 | Risk Portal |
| **VaR Explain Report** | Market Risk, Trading | PDF | 07:15 | Email |
| **Stress Explain Report** | Market Risk, Trading | PDF | 07:15 | Email |
| **Backtesting Report** | Market Risk, RMA | PDF | 07:15 | Email |
| **Regulatory Feed** | Finance, Regulatory Reporting | Data file | 07:30 | Automated |
| **MLRC Risk Pack** | MLRC members | PDF | Weekly (Fri) | Email |
| **Pillar Stress Report** | MLRC, Board | PDF | Weekly (Mon) | Email |
| **Board Risk Report** | Board Risk Committee | PDF | Monthly | Board Portal |

### 8.2 MLRC Risk Pack Contents

The weekly MLRC Risk Pack consolidates all three streams:

| Section | Content | Source Stream |
|---------|---------|---------------|
| **Executive Summary** | Key metrics, limit status, material changes | All |
| **VaR Trends** | Entity VaR trend, VaR explain summary | Stream 2 |
| **SVaR Analysis** | SVaR vs VaR, stressed period assessment | Stream 2 |
| **EaR vs Risk Appetite** | Entity EaR vs RAS thresholds (Green/Amber/Red), by risk type | Stream 2 |
| **ECAP vs Regulatory** | Economic capital vs IMA capital reconciliation | Stream 2 |
| **Backtesting** | Exception count, zone status, root cause | Stream 2 |
| **Stress Results** | Pillar scenarios, worst scenarios, PoW | Stream 3 |
| **Limit Utilisation** | VaR limits, Stress limits, Sensitivity limits, EaR appetite | All |
| **Concentration** | Top issuers, curves, currencies, sectors | Stream 1 |
| **Action Items** | Open items, remediation progress | All |

---

## 9. Backtesting Summary

> **Note**: Detailed backtesting methodology has been extracted to [VaR Backtesting Process (MR-L4-008)](./backtesting.md).

### 9.1 Daily Backtesting in Reporting Workflow

| Step | Activity | Output |
|------|----------|--------|
| **1** | Retrieve VaR (T-1) from Risk Engine | VaR prediction |
| **2** | Retrieve Hypothetical and Actual P&L (T-1) from P&L ODS | P&L for comparison |
| **3** | Compare \|P&L\| to VaR - if exceeded, flag exception | Exception flag |
| **4** | Update rolling 250-day exception count | Zone status |
| **5** | If exception, invoke backtesting process for root cause | Exception report |

### 9.2 Zone Status

| Zone | Exceptions | Capital Multiplier | Implication |
|------|-----------|-------------------|-------------|
| **GREEN** | 0-4 | 3.0x | Normal operations |
| **YELLOW** | 5-9 | 3.4x - 3.85x | Investigation required |
| **RED** | ≥10 | 4.0x | Remediation required |

---

## 10. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| RSO-C01 | All QC checks must pass or be explained before sign-off | Preventive | RAV |
| RSO-C02 | Backtesting performed daily with exception tracking | Detective | RAV |
| RSO-C03 | Material VaR changes (>10% or >$1M) require VaR explain | Detective | RAV |
| RSO-C04 | Material Stress changes (>15% or >$5M) require Stress explain | Detective | RAV |
| RSO-C05 | Sign-off obtained before report distribution | Preventive | RAV |
| RSO-C06 | All reports distributed by SLA (07:30) | Detective | RAV |
| RSO-C07 | Scenario parameters reconciled to MLRC Golden Source | Detective | RAV |
| RSO-C08 | Weekly MLRC pack includes all three streams | Detective | RAV |
| RSO-C09 | Exception log maintained with full audit trail | Detective | Market Risk |
| RSO-C10 | EaR calculated and checked against Risk Appetite Statement thresholds | Detective | RAV |
| RSO-C11 | EaR breach (Amber/Red) escalated per Risk Appetite Framework | Preventive | RAV |

---

## 11. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| QC complete (all streams) | 04:45 GMT+1 | 05:00 GMT+1 | RAV Team Lead |
| Backtesting complete | 05:30 GMT+1 | 05:45 GMT+1 | RAV Team Lead |
| VaR explain complete (if required) | 06:00 GMT+1 | 06:15 GMT+1 | RAV Manager |
| Stress explain complete (if required) | 06:00 GMT+1 | 06:15 GMT+1 | RAV Manager |
| Sign-off obtained | 07:00 GMT+1 | 07:15 GMT+1 | Head of RAV |
| **Reports distributed** | **07:30 GMT+1** | **08:00 GMT+1** | **Head of Market Risk** |

---

## 12. Exception Handling

### 12.1 Process Exceptions

| Exception | Cause | Resolution | Escalation |
|-----------|-------|------------|------------|
| **QC failure (VaR)** | Data quality issue | Investigate; re-run if needed | RAV Manager |
| **QC failure (Stress)** | Scenario or calculation issue | Investigate; verify params | RAV Manager |
| **Sign-off delay** | Investigation required | Partial release possible | Head of RAV |
| **Report delay** | System issue | Manual distribution | RAV + IT |
| **Backtest data missing** | P&L ODS issue | Use T-2 data with flag | RAV Team Lead |

### 12.2 Override Authority

In exceptional circumstances, reports may be released with known issues:

| Scenario | Authority | Conditions |
|----------|-----------|------------|
| Minor data quality issue | RAV Team Lead | Issue documented; not material |
| Partial VaR (some desks missing) | Head of RAV | Missing desks <10% of total VaR |
| Partial Stress (some scenarios missing) | Head of RAV | Core Pillar scenarios available |
| Delayed sign-off | Head of Market Risk | Preliminary figures released with caveat |
| Full production failure | CRO | BCP figures with confidence interval |

---

## 13. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [Risk Engine Calculation](./risk-engine-calculation.md) | Upstream - provides VaR/SVaR data |
| [Stress Testing](./stress-testing.md) | Upstream - provides Stress P&L data |
| [VaR Backtesting](./backtesting.md) | Sub-process - detailed backtesting methodology |
| [Market Risk Limits Management](./market-risk-limits-management.md) | Related - limits lifecycle and monitoring |
| [VaR Limit Framework](../L3-Governance/policies/var-limit-framework.md) | Governance - limit structure |
| [MLRC Terms of Reference](../L3-Governance/committees/mlrc-terms-of-reference.md) | Governance - committee oversight |
| [Market Risk Policy](../L3-Governance/policies/market-risk-policy.md) | Parent policy |

---

## 14. Document Control

### 14.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version (VaR Reporting and Sign-off) | MLRC |
| 1.1 | 2025-01-15 | Slimmed Section 4 (Backtesting) to reference standalone MR-L4-008 process | MLRC |
| 2.0 | 2025-01-16 | Major restructure: Renamed to Market Risk Reporting and Sign-off; expanded to cover all three Risk Engine streams (Sensitivities, VaR/SVaR, Stress); added Stress Explain methodology; extracted limits to standalone MR-L4-013 process | MLRC |
| 2.1 | 2025-01-16 | Added ECAP to sign-off checklist, report inventory, and MLRC Risk Pack contents | MLRC |
| 2.2 | 2025-01-17 | Added EaR (Earnings at Risk) reporting aligned to Risk Appetite Statement (GOV-L3-010); added EaR sign-off checks, Risk Appetite controls (RSO-C10/C11), and MLRC pack section | MLRC |

---

*End of Document*
