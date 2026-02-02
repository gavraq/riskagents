---
# Process Metadata
process_id: MR-L4-001
process_name: Market Risk Process Orchestration
version: 3.3
effective_date: 2025-01-16
next_review_date: 2026-01-16
owner: Head of Market Risk
approving_committee: MLRC

# Taxonomy Linkages
parent_policy: MR-L3-001  # Market Risk Policy
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
  - GOV-L3-010  # Risk Appetite Statement (EaR thresholds)
  - GOV-L3-011  # Risk Appetite Framework
l5_controls:
  - MR-L5-001   # VaR Limits
  - MR-L5-004   # Backtesting Exception Limits
l6_models:
  - MR-L6-001   # Historical Simulation VaR
  - MR-L6-002   # Stressed VaR
  - MR-L6-003   # IRC Model
l7_systems:
  - SYS-MR-001  # Murex
  - SYS-MR-002  # Valuation Engine
  - SYS-MR-003  # Risk Engine
  - SYS-MR-004  # Risk Reporting DataMart
  - SYS-MR-005  # Trade ODS
  - SYS-MR-006  # Market Data ODS
  - SYS-MR-007  # Valuations ODS
  - SYS-MR-008  # Risk ODS
  - SYS-MR-009  # P&L ODS (Trading Sub-Ledger)
  - SYS-MR-011  # Hierarchy ODS

# Sub-Processes (Orchestrated)
sub_processes:
  - MR-L4-002   # Trade Capture Controls
  - MR-L4-003   # EOD Market Data Snapshot
  - MR-L4-004   # Regional EOD Management
  - MR-L4-005   # Time Series Management
  - MR-L4-006   # Risk Engine Calculation
  - MR-L4-007   # Market Risk Reporting and Sign-off
  - MR-L4-008   # VaR Backtesting
  - MR-L4-009   # Market Risk Regulatory Reporting
  - MR-L4-010   # IRC Calculation
  - MR-L4-011   # Market Risk Stress Testing
  - MR-L4-012   # Trading Desk Mandate Management
  - MR-L4-013   # Market Risk Limits Management
  - MR-L4-014   # Aged Inventory Monitoring
---

# Market Risk Process Orchestration

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-001 |
| **Version** | 3.3 |
| **Effective Date** | 16 January 2025 |
| **Parent Policy** | Market Risk Policy (MR-L3-001) |
| **Owner** | Head of Market Risk |
| **Document Type** | **Master Orchestration Process** |

---

## 1. Executive Summary

### 1.1 Purpose

This document serves as the **master orchestration process** for all Market Risk processes at Meridian Global Bank. It describes how the component sub-processes work together to deliver:

- **Daily Risk Metrics**: VaR, SVaR, ECAP, EaR, Stress P&L, sensitivities
- **Limit Monitoring**: Real-time and end-of-day limit utilisation and breach escalation
- **Regulatory Capital**: IMA capital components (VaR, SVaR, IRC)
- **Risk Appetite Monitoring**: EaR vs Risk Appetite Statement thresholds
- **Stress Testing**: Pillar stress scenarios, Point of Weakness analysis
- **Governance**: Trading desk mandates, designated dealers, regulatory reporting
- **MLRC Oversight**: Risk committee reporting and decision support

### 1.2 Document Type: Orchestration

This is an **orchestration document** - it coordinates multiple detailed sub-processes rather than containing all procedural detail itself. Each sub-process has its own comprehensive documentation:

| Sub-Process | Process ID | Purpose | Document Link |
|-------------|------------|---------|---------------|
| **Trade Capture Controls** | MR-L4-002 | Ensure trade completeness and reconciliation | [trade-capture-controls.md](./trade-capture-controls.md) |
| **EOD Market Data Snapshot** | MR-L4-003 | Capture official EOD prices, curves, volatilities | [eod-market-data-snapshot.md](./eod-market-data-snapshot.md) |
| **Regional EOD Management** | MR-L4-004 | Manage timing differences across Asia/London/NY | [regional-eod-management.md](./regional-eod-management.md) |
| **Time Series Management** | MR-L4-005 | Manage historical data for VaR calculation | [time-series-management/](./time-series-management/time-series-overview.md) |
| **Risk Engine Calculation** | MR-L4-006 | Execute VaR, SVaR, ECAP, EaR calculations | [risk-engine-calculation.md](./risk-engine-calculation.md) |
| **Market Risk Reporting and Sign-off** | MR-L4-007 | Quality control, reporting, and governance | [market-risk-reporting-signoff.md](./market-risk-reporting-signoff.md) |
| **VaR Backtesting** | MR-L4-008 | Validate VaR model accuracy, Basel traffic light | [backtesting.md](./backtesting.md) |
| **Regulatory Reporting** | MR-L4-009 | PRA notifications, COREP submissions | [regulatory-reporting.md](./regulatory-reporting.md) |
| **IRC Calculation** | MR-L4-010 | Incremental Risk Charge for credit positions | [irc-calculation.md](./irc-calculation.md) |
| **Stress Testing** | MR-L4-011 | Stress scenario development, FO consultation, parameterisation | [stress-testing.md](./stress-testing.md) |
| **Desk Mandate Management** | MR-L4-012 | Trading desk mandates, designated dealers, CRR 104b | [desk-mandate-management.md](./desk-mandate-management.md) |
| **Limits Management** | MR-L4-013 | Limit setup, monitoring, breach management, annual review | [market-risk-limits-management.md](./market-risk-limits-management.md) |
| **Aged Inventory Monitoring** | MR-L4-014 | Quarterly inventory review, ICAAP illiquidity input | [aged-inventory-monitoring.md](./aged-inventory-monitoring.md) |

### 1.3 Scope

Daily VaR Production covers:
- **VaR** (99%, 1-day Historical Simulation)
- **Scaled 10-day VaR** for regulatory capital
- **Stressed VaR** (dynamic stress period selection)
- **Incremental Risk Charge (IRC)** for credit positions (see [IRC Calculation (MR-L4-010)](./irc-calculation.md))
- VaR by hierarchy (Entity → Division → Business Unit → Desk → Book)
- Limit utilisation reporting
- Exception identification and escalation

---

## 2. End-to-End Process Overview

### 2.1 High-Level Orchestration Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     DAILY VaR PRODUCTION - ORCHESTRATION VIEW                           │
│                     (End-to-End Process Flow)                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              INPUTS (By 17:00 GMT)                                     │
│                                                                                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                      │
│  │  TRADING SYSTEMS │  │  MARKET DATA     │  │  TIME SERIES     │                      │
│  │  (e.g. Murex)    │  │  SOURCES         │  │  HISTORY         │                      │
│  │                  │  │                  │  │                  │                      │
│  │  • Positions     │  │  • Bloomberg     │  │  • 500+ days     │                      │
│  │  • Trades        │  │  • Reuters       │  │  • Validated     │                      │
│  │  • Amendments    │  │  • Exchanges     │  │  • Proxies       │                      │
│  │                  │  │  • Internal marks│  │    applied       │                      │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘                      │
│           │                     │                     │                                │
└───────────┼─────────────────────┼─────────────────────┼────────────────────────────────┘
            │                     │                     │
            ▼                     ▼                     ▼
┌───────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1: DATA CAPTURE (17:00 - 19:00 GMT)                                            │
│  ═══════════════════════════════════════════                                          │
│                                                                                       │
│  ┌─────────────────────────────┐    ┌─────────────────────────────┐                   │
│  │  MR-L4-002                  │    │  MR-L4-003                  │                   │
│  │  TRADE CAPTURE CONTROLS     │    │  EOD MARKET DATA SNAPSHOT   │                   │
│  │                             │    │                             │                   │
│  │  • EOD trade extract        │    │  • Curve building           │                   │
│  │  • Trade reconciliation     │    │  • 4-eyes review            │                   │
│  │  • Completeness checks      │    │  • IPV coordination         │                   │
│  │  • Confirmations status     │    │  • Snapshot publication     │                   │
│  │                             │    │                             │                   │
│  │  Owner: Trading Operations  │    │  Owner: Market Data Control │                   │
│  └──────────────┬──────────────┘    └──────────────┬──────────────┘                   │
│                 │                                  │                                  │
│                 └──────────────┬───────────────────┘                                  │
│                                │                                                      │
│                 ┌──────────────┴──────────────┐                                       │
│                 │  MR-L4-004                  │                                       │
│                 │  REGIONAL EOD MANAGEMENT    │                                       │
│                 │                             │                                       │
│                 │  • Asia/London/NY snapshots │                                       │
│                 │  • Fictitious P&L tracking  │                                       │
│                 │  • Global consolidation     │                                       │
│                 │                             │                                       │
│                 │  Owner: Product Control     │                                       │
│                 └──────────────┬──────────────┘                                       │
│                                │                                                      │
└────────────────────────────────┼──────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌───────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 2: VALUATION & P&L (19:00 - 21:00 GMT)                                         │
│  ════════════════════════════════════════════                                         │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐  │
│  │                    VALUATION ENGINE + P&L ENGINE                                │  │
│  │                                                                                 │  │
│  │   TRADE ODS ─────┐                                                              │  │
│  │                  │      ┌──────────────────────────────────┐                    │  │
│  │                  ├─────▶│  Mark-to-Market Calculation      │                    │  │
│  │                  │      │  • Full revaluation (T and T-1)  │                    │  │
│  │   EOD MARKET ────┘      │  • Greeks/sensitivities          │                    │  │
│  │   SNAPSHOT              │  • P&L calculation               │                    │  │
│  │                         └──────────────┬───────────────────┘                    │  │
│  │                                        │                                        │  │
│  │           ┌────────────────────────────┼────────────────────────────┐           │  │
│  │           │                            │                            │           │  │
│  │           ▼                            ▼                            ▼           │  │
│  │  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐      │  │
│  │  │   VALUATIONS ODS    │  │      P&L ODS        │  │   HIERARCHY ODS     │      │  │
│  │  │                     │  │ (Trading Sub-Ledger)│  │                     │      │  │
│  │  │  • MTM by position  │  │                     │  │  • Book → Desk      │      │  │
│  │  │  • Sensitivities    │  │  • Actual P&L       │  │  • Desk → Business  │      │  │
│  │  │    (DV01, CS01,     │  │  • Hypothetical P&L │  │  • Business → Legal │      │  │
│  │  │    Vega, Delta)     │  │    (for backtesting)│  │    Entity           │      │  │
│  │  │                     │  │  • P&L attribution  │  │  • Entity →         │      │  │
│  │  │                     │  │                     │  │    Enterprise       │      │  │
│  │  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘      │  │
│  │                                                                                 │  │
│  │   Owner: Risk Engine Operations / Product Control (P&L sign-off)                │  │
│  └─────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌───────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 3: TIME SERIES PREPARATION (19:00 - 22:00 GMT)                                 │
│  ════════════════════════════════════════════════════                                 │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐  │
│  │  MR-L4-005                                                                      │  │
│  │  TIME SERIES MANAGEMENT                                                         │  │
│  │                                                                                 │  │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐     │  │
│  │  │ MR-L4-005a    │  │ MR-L4-005b    │  │ MR-L4-005c    │  │ MR-L4-005d    │     │  │
│  │  │ Price         │─▶│ Cleaning &    │─▶│ Curve         │─▶│ Proxying      │     │  │
│  │  │ Collection    │  │ Validation    │  │ Stripping     │  │ Process       │     │  │
│  │  └───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘     │  │
│  │                                                                                 │  │
│  │  Output: Complete time series (500+ days) for all risk factors                  │  │
│  │  Owner: RAV (process) / RMA (methodology)                                       │  │
│  └─────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌───────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 4: RISK CALCULATION (22:00 GMT - 04:00 GMT+1)                                  │
│  ═══════════════════════════════════════════════════                                  │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐  │
│  │  MR-L4-006                                                                      │  │
│  │  RISK ENGINE CALCULATION (3-Step VaR Calculation Chain)                         │  │
│  │                                                                                 │  │
│  │  ═══════════════════════════════════════════════════════════════════════════    │  │
│  │  STEP 1: P&L STRIP CALCULATION (per Trade × per Scenario Date)                  │  │
│  │  ═══════════════════════════════════════════════════════════════════════════    │  │
│  │                                                                                 │  │
│  │   VALUATIONS ────┐                                                              │  │
│  │   ODS            │      ┌──────────────────────────────────────────────────┐    │  │
│  │                  │      │  RISK ENGINE - P&L Strip Calculator              │    │  │
│  │                  ├─────▶│                                                  │    │  │
│  │                  │      │  For each trade × each historical scenario date: │    │  │
│  │   TIME SERIES ───┘      │  P&L_strip(t,d) = MTM(today's prices shocked by  │    │  │
│  │   ODS                   │                   returns from date d)           │    │  │
│  │                         │                   - MTM(today's prices)          │    │  │
│  │                         │                                                  │    │  │
│  │                         │  Output: Matrix of P&L strips                    │    │  │
│  │                         │  Rows = Trades, Columns = 500+ scenario dates    │    │  │
│  │                         └──────────────────────────────────────────────────┘    │  │
│  │                                        │                                        │  │
│  │                                        ▼                                        │  │
│  │  ┌───────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │  P&L STRIPS (per Trade, per Scenario Date)                                │  │  │
│  │  │                                                                           │  │  │
│  │  │  Trade TRD-001:  [-50, +20, -30, +15, -80, +45, -25, ...]   (500+ days)   │  │  │
│  │  │  Trade TRD-002:  [+10, -15, +25, -40, +30, -20, +55, ...]   (500+ days)   │  │  │
│  │  │  Trade TRD-003:  [-25, +35, -10, +5,  -15, +10, -30, ...]   (500+ days)   │  │  │
│  │  │  ...                                                                      │  │  │
│  │  └───────────────────────────────────────────────────────────────────────────┘  │  │
│  │                                        │                                        │  │
│  │  ═══════════════════════════════════════════════════════════════════════════    │  │
│  │  STEP 2: HIERARCHY AGGREGATION (Sum P&L Strips up the Book Hierarchy)           │  │
│  │  ═══════════════════════════════════════════════════════════════════════════    │  │
│  │                                        │                                        │  │
│  │                                        ▼                                        │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐ │  │
│  │  │  HIERARCHY ODS ──▶  AGGREGATION ENGINE                                     │ │  │
│  │  │                                                                            │ │  │
│  │  │  Book → Desk → Business Unit → Division → Legal Entity → Enterprise        │ │  │
│  │  │                                                                            │ │  │
│  │  │  For each hierarchy node, for each scenario date:                          │ │  │
│  │  │  Aggregated_P&L(node, d) = Σ P&L_strip(t, d) for all trades t in node      │ │  │
│  │  │                                                                            │ │  │
│  │  │  ┌─────────────────────────────────────────────────────────────────────┐   │ │  │
│  │  │  │  Book Level:     [-60, +40, -15, +0, -65, +65, +0, ...]  (500+ days)│   │ │  │
│  │  │  │  Desk Level:     [-120, +80, -45, +20, -130, +95, -25, ...]         │   │ │  │
│  │  │  │  Business Level: [-200, +150, -80, +35, -180, +140, -50, ...]       │   │ │  │
│  │  │  │  Division Level: [-450, +320, -150, +80, -400, +280, -100, ...]     │   │ │  │
│  │  │  │  Entity Level:   [-800, +600, -300, +150, -750, +550, -200, ...]    │   │ │  │
│  │  │  └─────────────────────────────────────────────────────────────────────┘   │ │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘ │  │
│  │                                        │                                        │  │
│  │  ═══════════════════════════════════════════════════════════════════════════    │  │
│  │  STEP 3: PERCENTILE CALCULATION (VaR = 99th Percentile Loss)                    │  │
│  │  ═══════════════════════════════════════════════════════════════════════════    │  │
│  │                                        │                                        │  │
│  │                                        ▼                                        │  │
│  │  ┌────────────────────────────────────────────────────────────────────────────┐ │  │
│  │  │  PERCENTILE CALCULATOR                                                     │ │  │
│  │  │                                                                            │ │  │
│  │  │  For each hierarchy node:                                                  │ │  │
│  │  │  1. Sort aggregated P&L strip: [-800, -750, -450, -300, ..., +600]         │ │  │
│  │  │  2. Find 99th percentile (1% worst): 5th worst out of 500 observations     │ │  │
│  │  │  3. VaR (99%, 1-day) = absolute value of 99th percentile loss              │ │  │
│  │  │                                                                            │ │  │
│  │  │  Example: 5th worst = -750  →  VaR = $750k                                 │ │  │
│  │  │                                                                            │ │  │
│  │  │  Also calculates:                                                          │ │  │
│  │  │  • SVaR using stressed period time series                                  │ │  │
│  │  │  • IRC using credit migration scenarios                                    │ │  │
│  │  │  • Risk factor contributions (marginal VaR)                                │ │  │
│  │  └────────────────────────────────────────────────────────────────────────────┘ │  │
│  │                                        │                                        │  │
│  │                                        ▼                                        │  │
│  │                         ┌──────────────────────────────────┐                    │  │
│  │                         │         RISK ODS                 │                    │  │
│  │                         │  • VaR by hierarchy level        │                    │  │
│  │                         │  • SVaR by hierarchy level       │                    │  │
│  │                         │  • ECAP by hierarchy level       │                    │  │
│  │                         │  • EaR by hierarchy (Risk App)   │                    │  │
│  │                         │  • IRC                           │                    │  │
│  │                         │  • P&L strips (stored for audit) │                    │  │
│  │                         │  • Risk factor contributions     │                    │  │
│  │                         └──────────────────────────────────┘                    │  │
│  │                                                                                 │  │
│  │   Owner: Risk Engine Operations                                                 │  │
│  └─────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌───────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 5: QUALITY CONTROL & REPORTING (04:00 - 07:30 GMT+1)                           │
│  ══════════════════════════════════════════════════════════                           │
│                                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐  │
│  │  MR-L4-007                                                                      │  │
│  │  VaR REPORTING AND SIGN-OFF                                                     │  │
│  │                                                                                 │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                  │  │
│  │  │ Quality Control │  │ Limit           │  │ Reporting &     │                  │  │
│  │  │                 │  │ Monitoring      │  │ Governance      │                  │  │
│  │  │ • Completeness  │  │                 │  │                 │                  │  │
│  │  │ • Reasonableness│  │ • Utilisation   │  │ • Dashboard     │                  │  │
│  │  │ • Backtesting   │  │ • Breaches      │  │ • Sign-off      │                  │  │
│  │  │ • Data quality  │  │ • Escalation    │  │ • Distribution  │                  │  │
│  │  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘                  │  │
│  │           │                    │                    │                           │  │
│  │           └────────────────────┴────────────────────┘                           │  │
│  │                                │                                                │  │
│  │                                ▼                                                │  │
│  │                 ┌──────────────────────────────────┐                            │  │
│  │                 │    RISK REPORTING DATAMART       │                            │  │
│  │                 │  • VaR Dashboard                 │                            │  │
│  │                 │  • Limit utilisation report      │                            │  │
│  │                 │  • Exception report              │                            │  │
│  │                 │  • MLRC pack                     │                            │  │
│  │                 └──────────────────────────────────┘                            │  │
│  │                                                                                 │  │
│  │   Owner: RAV Team / Market Risk                                                 │  │
│  └─────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                              OUTPUTS (By 07:30 GMT+1)                                 │
│                                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐                     │
│  │  LIMIT MONITORING│  │  REGULATORY      │  │  MANAGEMENT      │                     │
│  │                  │  │  REPORTING       │  │  REPORTING       │                     │
│  │  • Desk alerts   │  │                  │  │                  │                     │
│  │  • Breach        │  │  • IMA capital   │  │  • MLRC dashboard│                     │
│  │    escalation    │  │  • Stress test   │  │  • CRO report    │                     │
│  │  • Utilisation   │  │    inputs        │  │  • Board pack    │                     │
│  │    reports       │  │                  │  │                  │                     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘                     │
│                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Critical Path and Dependencies

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           CRITICAL PATH DEPENDENCIES                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Trade Capture ──────┐                                                                  │
│  (MR-L4-002)         │                                                                  │
│                      ├───▶ Valuation Engine ───▶ Risk Engine ───▶ Reporting             │
│  EOD Market Data ────┤         │                 (MR-L4-006)     (MR-L4-007)            │
│  (MR-L4-003)         │         │                      ▲                                 │
│                      │         │                      │                                 │
│  Regional EOD ───────┘         │                      │                                 │
│  (MR-L4-004)                   │                      │                                 │
│                                │                      │                                 │
│                                └──────────────────────┘                                 │
│                                                                                         │
│  Time Series Management ──────────────────────────────┘                                 │
│  (MR-L4-005)                                                                            │
│                                                                                         │
│  CRITICAL PATH: Trade Capture + EOD Snapshot → Valuation → Risk Engine → Reporting      │
│                                                                                         │
│  PARALLEL PATH: Time Series runs in parallel with Valuation, must complete before       │
│                 Risk Engine                                                             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Process Timing

### 3.1 Master Timeline (London Time)

| Phase | Start | End | Duration | Sub-Process | Owner |
|-------|-------|-----|----------|-------------|-------|
| **1. Data Capture** | 17:00 T | 19:00 T | 2 hours | MR-L4-002, MR-L4-003, MR-L4-004 | Trading Ops, MDC |
| **2. Valuation** | 19:00 T | 21:00 T | 2 hours | (Valuation Engine) | Risk Engine Ops |
| **3. Time Series** | 19:00 T | 22:00 T | 3 hours | MR-L4-005 | RAV |
| **4. Risk Calculation** | 22:00 T | 04:00 T+1 | 6 hours | MR-L4-006 | Risk Engine Ops |
| **5. QC & Reporting** | 04:00 T+1 | 07:30 T+1 | 3.5 hours | MR-L4-007 | RAV, Market Risk |

### 3.2 Key Milestones and SLAs

| Milestone | Target Time | SLA | Escalation |
|-----------|-------------|-----|------------|
| EOD Market Data Snapshot published | 18:30 T | Must complete | Head of MDC |
| Trade ODS refresh complete | 19:00 T | Must complete | Trading Ops Manager |
| Valuation Engine complete | 21:00 T | 95% on-time | Risk Engine Ops Manager |
| Time Series ready | 22:00 T | Must complete | RAV Manager |
| Risk Engine batch start | 22:00 T | Must complete | Risk Engine Ops Manager |
| VaR calculation complete | 04:00 T+1 | 95% on-time | Risk Engine Ops Manager |
| Quality checks complete | 05:30 T+1 | Must complete | RAV Team Lead |
| **VaR report available** | **07:00 T+1** | **Regulatory SLA** | **Head of Market Risk** |
| MLRC dashboard updated | 07:30 T+1 | Internal SLA | Market Risk Analytics |

### 3.3 Regional Timing Considerations

The process must accommodate Meridian Global Bank's three regional hubs:

| Region | Local Close | Feed to London | Impact on VaR |
|--------|-------------|----------------|---------------|
| **Asia (HK)** | 17:30 HKT | 18:00 HKT | Asia positions valued at London EOD |
| **London (HQ)** | 17:30 GMT | N/A (primary) | Official global snapshot |
| **Americas (NY)** | 17:30 EST | 18:00 EST | NY positions valued at London EOD |

See [Regional EOD Management (MR-L4-004)](./regional-eod-management.md) for handling of timing differences and fictitious P&L.

---

## 4. Sub-Process Integration Points

### 4.1 Data Flow Between Sub-Processes

| From Process | To Process | Data Exchanged | Format | Timing |
|--------------|------------|----------------|--------|--------|
| **Trade Capture (MR-L4-002)** | Valuation Engine | Positions, trades | Trade ODS tables | 19:00 T |
| **EOD Snapshot (MR-L4-003)** | Valuation Engine | Prices, curves, vol | Market Data ODS | 18:30 T |
| **EOD Snapshot (MR-L4-003)** | Time Series (MR-L4-005) | EOD observations | Price records | 18:30 T |
| Valuation Engine | P&L ODS | Actual P&L, Hypothetical P&L, attribution | P&L ODS tables | 21:00 T |
| Valuation Engine | Risk Engine (MR-L4-006) | MTM, sensitivities | Valuations ODS | 21:00 T |
| **Hierarchy ODS** | Risk Engine (MR-L4-006) | Book hierarchy structure | Hierarchy ODS | Static (daily refresh) |
| **Time Series (MR-L4-005)** | Risk Engine (MR-L4-006) | Historical returns | Time Series ODS | 22:00 T |
| **Risk Engine (MR-L4-006)** | Risk ODS | P&L strips, aggregated P&L | Risk ODS | 03:00 T+1 |
| **Risk Engine (MR-L4-006)** | Reporting (MR-L4-007) | VaR, SVaR, ECAP, EaR, IRC | Risk ODS | 04:00 T+1 |
| **P&L ODS** | Backtesting (MR-L4-007) | Hypothetical P&L (T-1) | P&L ODS tables | 04:00 T+1 |

### 4.2 Quality Gates

Each phase transition has a quality gate that must pass before proceeding:

| Gate | Phase Transition | Criteria | Fallback |
|------|------------------|----------|----------|
| **QG1** | Data Capture → Valuation | Trade count ±1% of T-1; Market data complete | Investigate; use T-1 if needed |
| **QG2** | Valuation → Risk Engine | MTM reconciles to Finance (±$125k); All desks populated | Fix breaks; partial run |
| **QG3** | Time Series → Risk Engine | All risk factors have observations; Proxies applied | Apply emergency proxies |
| **QG4** | Risk Engine → Reporting | VaR calculated for all desks; No calc errors | Investigate; partial release |
| **QG5** | Reporting → Distribution | All checks passed; Sign-off obtained | Escalate to Head of MR |

---

## 5. Roles and Responsibilities

### 5.1 Process Ownership

| Role | Process | Responsibilities |
|------|---------|------------------|
| **Head of Market Risk Analytics** | Overall VaR Production | End-to-end accountability; escalation point |
| **Head of MDC** | EOD Market Data Snapshot | Price integrity; "One Curve, One Price" |
| **Trading Operations Manager** | Trade Capture Controls | Trade completeness; reconciliation |
| **RAV Manager** | Time Series Management | Data quality; proxy governance |
| **Risk Engine Ops Manager** | Risk Engine Calculation | Batch execution; system availability |
| **RAV Team Lead** | VaR Reporting & Sign-off | Quality control; sign-off authority |

### 5.2 RACI Matrix (Orchestration Level)

| Sub-Process | Trading Ops | MDC | Risk Engine Ops | RAV | Market Risk | MLRC |
|-------------|:-----------:|:---:|:---------------:|:---:|:-----------:|:----:|
| Trade Capture (MR-L4-002) | R/A | - | I | I | I | - |
| EOD Snapshot (MR-L4-003) | - | R/A | I | I | I | - |
| Regional EOD (MR-L4-004) | C | C | - | I | R/A | I |
| Time Series (MR-L4-005) | - | C | I | R/A | C | - |
| Risk Engine (MR-L4-006) | - | - | R/A | I | I | - |
| Reporting & Sign-off (MR-L4-007) | I | I | I | R | A | I |
| **Overall VaR Production** | C | C | C | C | R/A | A |

**R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed

---

## 6. Exception Handling

### 6.1 Exception Escalation by Sub-Process

| Sub-Process | Exception Type | First Response | Escalation |
|-------------|----------------|----------------|------------|
| **Trade Capture** | Missing trades | Trading Ops re-extract | Trading Ops → Risk Engine Ops |
| **Trade Capture** | Reconciliation break | Investigate cause | Trading Ops → RAV → Market Risk |
| **EOD Snapshot** | Missing market data | Use T-1 + proxy flag | MDC → RAV → Market Risk |
| **EOD Snapshot** | IPV challenge | Desk justification | Product Control → CFO |
| **Time Series** | Source failure | Backup source | RAV → Market Risk |
| **Time Series** | Proxy gap | Emergency proxy | RAV → RMA (same day approval) |
| **Risk Engine** | Calculation failure | Re-run affected desks | Risk Engine Ops → Quants |
| **Risk Engine** | VaR spike >50% | Investigate cause | RAV → Market Risk → MLRC |
| **Reporting** | Limit breach | Immediate escalation | Market Risk → MLRC/CRO |

### 6.2 Re-run Authority

| Scenario | Authority | Max Delay | Notification |
|----------|-----------|-----------|--------------|
| Single desk data correction | RAV Team Lead | +1 hour | Risk Engine Ops |
| Multiple desk data correction | RAV Manager | +2 hours | Market Risk |
| Full re-run (data issue) | Head of Market Risk Analytics | +4 hours | MLRC |
| Full re-run (system issue) | Risk Engine Ops Manager | +4 hours | CRO |
| Methodology change | MLRC approval required | N/A | Parallel run |

---

## 7. Business Continuity

### 7.1 BCP Triggers

| Scenario | BCP Level | Response | Authority |
|----------|-----------|----------|-----------|
| Risk Engine unavailable <4 hours | Level 1 | Delayed production; notify stakeholders | Risk Engine Ops |
| Risk Engine unavailable >4 hours | Level 2 | Manual VaR estimation; sensitivity-based | Head of MR Analytics |
| Market Data unavailable | Level 1 | Use T-1 data with proxy flag | MDC |
| Trade ODS unavailable | Level 2 | Murex direct extract; manual process | Trading Ops |
| Time Series Service unavailable | Level 2 | Use T-1 time series | RAV |
| Complete infrastructure failure | Level 3 | DR site activation; CRO notification | CRO |

### 7.2 Manual VaR Estimation

When automated VaR cannot be produced:

1. **Estimate VaR** using T-1 VaR ± sensitivity-based adjustment for known market moves
2. **Apply conservative buffer** of 20% to estimated VaR for limit monitoring
3. **Notify MLRC** of estimation methodology used
4. **Restrict new risk-taking** at affected desks until full production restored
5. **Document** all manual processes for audit trail

---

## 8. Controls and KPIs

### 8.1 Orchestration-Level Controls

| Control ID | Control | Type | Frequency | Owner |
|------------|---------|------|-----------|-------|
| VAR-C01 | All sub-processes complete before downstream dependency | Preventive | Daily | Risk Engine Ops |
| VAR-C02 | Quality gate criteria met at each transition | Detective | Daily | RAV |
| VAR-C03 | End-to-end process completes by SLA | Detective | Daily | Market Risk Analytics |
| VAR-C04 | All exceptions logged and escalated per framework | Detective | Daily | Market Risk |
| VAR-C05 | Monthly process performance review | Detective | Monthly | MLRC |

### 8.2 Key Performance Indicators

| KPI | Target | Threshold | Frequency | Owner |
|-----|--------|-----------|-----------|-------|
| VaR report delivery time | 07:00 T+1 | 07:30 T+1 | Daily | Market Risk Analytics |
| End-to-end process completion | 95% on-time | 90% | Monthly | Risk Engine Ops |
| Sub-process delays (any) | <5% of days | <10% | Monthly | Process owners |
| Quality gate failures | <2% of days | <5% | Monthly | RAV |
| Re-runs required | <5% of days | <10% | Monthly | Risk Engine Ops |
| Backtesting exceptions (rolling 250d) | <5 | <10 | Weekly | RMA |
| Limit breach response time | <1 hour | <2 hours | As needed | Market Risk |

---

## 9. Governance

### 9.1 Governance Forums

| Forum | Role in VaR Production | Frequency |
|-------|------------------------|-----------|
| **MLRC** | Oversight; breach decisions; methodology approval | Weekly |
| **Risk Technical Forum** | Methodology discussions; model issues | As needed |
| **Proxy & RniV Forum** | Proxy approvals; NMRF monitoring | Monthly |
| **Operations Steering Committee** | Process performance; system issues | Monthly |

### 9.2 Reporting to MLRC

Weekly MLRC receives:
- VaR trends and limit utilisation summary
- Backtesting exception analysis
- Process KPI dashboard
- Breach escalation log
- Upcoming process changes

---

## 10. Sub-Process Documentation

### 10.1 Detailed Process Documents

| Document | Process ID | Status | Description |
|----------|------------|--------|-------------|
| [Trade Capture Controls](./trade-capture-controls.md) | MR-L4-002 | ✅ Complete | Trade completeness; reconciliation |
| [EOD Market Data Snapshot](./eod-market-data-snapshot.md) | MR-L4-003 | ✅ Complete | Official EOD capture; "One Curve, One Price" |
| [Regional EOD Management](./regional-eod-management.md) | MR-L4-004 | ✅ Complete | Asia/London/NY timing; fictitious P&L |
| [Time Series Management](./time-series-management/time-series-overview.md) | MR-L4-005 | ✅ Complete | Historical data management (6 sub-processes) |
| [Risk Engine Calculation](./risk-engine-calculation.md) | MR-L4-006 | ✅ Complete | VaR/SVaR/ECAP/EaR calculation |
| [Market Risk Reporting and Sign-off](./market-risk-reporting-signoff.md) | MR-L4-007 | ✅ Complete | QC, reporting, governance |
| [VaR Backtesting](./backtesting.md) | MR-L4-008 | ✅ Complete | Model validation; Basel traffic light; price source |
| [Regulatory Reporting](./regulatory-reporting.md) | MR-L4-009 | ✅ Complete | PRA notifications; COREP; CRR Article 366 |
| [IRC Calculation](./irc-calculation.md) | MR-L4-010 | ✅ Complete | Incremental Risk Charge for credit positions |
| [Stress Testing](./stress-testing.md) | MR-L4-011 | ✅ Complete | Scenario development; FO consultation; parameterisation |
| [Desk Mandate Management](./desk-mandate-management.md) | MR-L4-012 | ✅ Complete | Trading desk mandates; designated dealers; CRR 104b |
| [Market Risk Limits Management](./market-risk-limits-management.md) | MR-L4-013 | ✅ Complete | Limit setup, monitoring, breach management, annual review |
| [Aged Inventory Monitoring](./aged-inventory-monitoring.md) | MR-L4-014 | ✅ Complete | Quarterly inventory review, ICAAP illiquidity input |

### 10.2 Related Governance Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Policy](../L3-Governance/policies/market-risk-policy.md) | Parent policy |
| [VaR Limit Framework](../L3-Governance/policies/var-limit-framework.md) | Limit structure and escalation |
| [MLRC Terms of Reference](../L3-Governance/committees/mlrc-terms-of-reference.md) | Governance oversight |
| [Risk Appetite Statement](../../L3-Governance/risk-appetite-statement.md) | EaR thresholds and breach escalation |
| [Risk Appetite Framework](../../L3-Governance/risk-appetite-framework.md) | Risk Appetite governance |

### 10.3 Cross-Functional Dependencies

| Document | Owner | Relationship |
|----------|-------|--------------|
| [Hierarchy Management](./hierarchy-management.md) | Finance | Provides book hierarchy and trading book classification |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version as Daily VaR Production | MLRC |
| 2.0 | 2025-01-15 | Restructured as orchestration document; linked sub-processes | MLRC |
| 2.1 | 2025-01-15 | Added VaR Backtesting (MR-L4-008) as sub-process | MLRC |
| 2.2 | 2025-01-15 | Added Market Risk Regulatory Reporting (MR-L4-009) as sub-process | MLRC |
| 2.3 | 2025-01-16 | Added IRC Calculation (MR-L4-010) as standalone sub-process | MLRC |
| 2.4 | 2025-01-16 | Added Stress Testing (MR-L4-011) as standalone sub-process | MLRC |
| 2.5 | 2025-01-16 | Added Desk Mandate Management (MR-L4-012) as standalone sub-process | MLRC |
| 3.0 | 2025-01-16 | **Renamed to Market Risk Process Orchestration** to reflect comprehensive scope beyond VaR; 12 sub-processes now covered | MLRC |
| 3.1 | 2025-01-16 | Renamed VaR Reporting to Market Risk Reporting and Sign-off (expanded to cover all three streams); added Market Risk Limits Management (MR-L4-013) as standalone sub-process; now 13 sub-processes | MLRC |
| 3.2 | 2025-01-16 | Added Aged Inventory Monitoring (MR-L4-014) as standalone sub-process; now 14 sub-processes | MLRC |
| 3.3 | 2025-01-17 | Added ECAP/EaR to daily risk metrics; added Risk Appetite linkages (GOV-L3-010/011); updated Risk ODS outputs and data flows | MLRC |

### 11.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full Review | Annual | January 2026 |
| Process Metrics Review | Monthly | Ongoing |
| Post-Incident Review | As needed | N/A |
| Sub-Process Alignment | Quarterly | April 2025 |

---

*End of Document*
