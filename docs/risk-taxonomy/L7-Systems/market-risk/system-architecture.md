---
# System Metadata
document_id: MR-L7-001
document_name: Market Risk System Architecture and Data Feed Inventory
version: 1.3
effective_date: 2025-01-17
next_review_date: 2026-01-15
owner: Head of Risk Technology
approving_committee: MLRC / Technology Steering Committee

# Taxonomy Linkages
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-022  # BCBS 239 (Data Aggregation)
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - GOV-L3-010  # Risk Appetite Statement (EaR/ECAP limits)
  - GOV-L3-011  # Risk Appetite Framework
l4_processes:
  - MR-L4-001   # Market Risk Process Orchestration
  - MR-L4-003   # EOD Market Data Snapshot
  - MR-L4-005   # Time Series Management
  - MR-L4-006   # Risk Engine Calculation
  - MR-L4-014   # Aged Inventory Monitoring
l5_controls:
  - MR-L5-001   # VaR and SVaR Limits
  - MR-L5-007   # ECAP and EaR Controls
l6_models:
  - MR-L6-001   # Historical Simulation VaR
  - MR-L6-002   # ECAP and EaR Methodology
---

# Market Risk System Architecture and Data Feed Inventory

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | MR-L7-001 |
| **Version** | 1.3 |
| **Effective Date** | 17 January 2025 |
| **Owner** | Head of Risk Technology |

---

## 1. Purpose

This document provides a comprehensive overview of the Market Risk technology landscape at Meridian Global Bank, including:

- System architecture and data flows
- Data feed inventory and SLAs
- System dependencies and interfaces
- Business continuity and disaster recovery provisions
- Change management and support arrangements

---

## 2. System Landscape Overview

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     MARKET RISK SYSTEM ARCHITECTURE                                     │
│                     Meridian Global Bank                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  TIER 1: SOURCE SYSTEMS                                                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │     MUREX       │  │   BLOOMBERG     │  │    REUTERS      │  │    EXCHANGE     │     │
│  │  (SYS-MR-001)   │  │  (SYS-MR-012)   │  │  (SYS-MR-013)   │  │    FEEDS        │     │
│  │                 │  │                 │  │                 │  │  (SYS-MR-014)   │     │
│  │  • Trades       │  │  • Prices       │  │  • Prices       │  │                 │     │
│  │  • Positions    │  │  • Curves       │  │  • Curves       │  │  • Settlement   │     │
│  │  • Static data  │  │  • Vol surfaces │  │  • Vol surfaces │  │    prices       │     │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘     │
│           │                    │                    │                    │              │
└───────────┼────────────────────┼────────────────────┼────────────────────┼──────────────┘
            │                    │                    │                    │
            ▼                    ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  TIER 2: DATA INTEGRATION LAYER                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                       ENTERPRISE DATA HUB (EDH)                                   │  │
│  │                       (SYS-MR-015)                                                │  │
│  │  • Data ingestion      • Data transformation      • Data quality checks           │  │
│  │  • Feed monitoring     • Reconciliation           • Audit logging                 │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                           │                                             │
└───────────────────────────────────────────┼─────────────────────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  TIER 3: OPERATIONAL DATA STORES (ODS)                                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  TRADE ODS  │  │ MARKET DATA │  │ VALUATIONS  │  │  HIERARCHY  │  │    P&L      │    │
│  │ (SYS-MR-005)│  │     ODS     │  │    ODS      │  │    ODS      │  │    ODS      │    │
│  │             │  │(SYS-MR-006) │  │(SYS-MR-007) │  │(SYS-MR-011) │  │(SYS-MR-009) │    │
│  │ • Positions │  │             │  │             │  │             │  │             │    │
│  │ • Trades    │  │ • EOD prices│  │ • MTM       │  │ • Book      │  │ • Actual    │    │
│  │ • Static    │  │ • Curves    │  │ • Greeks    │  │   hierarchy │  │ • Hypo      │    │
│  │   data      │  │ • Vol surfs │  │ • Sens      │  │ • Mappings  │  │ • Attr      │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                │                │                │                │           │
│         └────────────────┴────────────────┴────────────────┴────────────────┘           │
│                                           │                                             │
└───────────────────────────────────────────┼─────────────────────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  TIER 4: CALCULATION ENGINES                                                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐               │
│  │      VALUATION ENGINE           │  │        RISK ENGINE              │               │
│  │        (SYS-MR-002)             │  │        (SYS-MR-003)             │               │
│  │                                 │  │                                 │               │
│  │  • Mark-to-market               │  │                                 │               │
│  │  • Greeks calculation           │  │  • VaR calculation              │               │
│  │  • P&L calculation              │  │  • SVaR calculation             │               │
│  │  • Sensitivity calculation      │  │  • IRC calculation              │               │
│  │                                 │  │  • Stress testing               │               │
│  └─────────────────────────────────┘  │  • P&L strip generation         │               │
│                                       │  • Hierarchy aggregation        │               │
│                                       └─────────────────────────────────┘               │
│                                           │                                             │
└───────────────────────────────────────────┼─────────────────────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  TIER 5: RISK DATA AND REPORTING                                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐               │
│  │         RISK ODS                │  │    RISK REPORTING DATAMART      │               │
│  │        (SYS-MR-008)             │  │        (SYS-MR-004)             │               │
│  │                                 │  │                                 │               │
│  │  • VaR results                  │  │  • Dashboards                   │               │
│  │  • SVaR results                 │  │  • Limit monitoring             │               │
│  │  • EaR results (Risk Appetite)  │  │  • Risk Appetite monitoring     │               │
│  │  • ECAP results                 │  │  • Exception reports            │               │
│  │  • P&L strips                   │  │  • MLRC packs                   │               │
│  │  • Risk factor contributions    │  │  • Regulatory reports           │               │
│  │  • Stress test results          │  │  • ICAAP inputs                 │               │
│  │  • Aged inventory flags         │  │                                 │               │
│  └─────────────────────────────────┘  └─────────────────────────────────┘               │
│                                                                                         │
│  ┌─────────────────────────────────┐                                                    │
│  │      TIME SERIES ODS            │                                                    │
│  │        (SYS-MR-010)             │                                                    │
│  │                                 │                                                    │
│  │  • Historical returns           │                                                    │
│  │  • 500+ days per risk factor    │                                                    │
│  │  • Stressed period data         │                                                    │
│  │  • Proxy mappings               │                                                    │
│  └─────────────────────────────────┘                                                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. System Inventory

### 3.1 Core Market Risk Systems

| System ID | System Name | Vendor/Type | Primary Function | Owner |
|-----------|-------------|-------------|------------------|-------|
| **SYS-MR-001** | Murex | Murex 3.1 | Trading system; position management | Front Office Technology |
| **SYS-MR-002** | Valuation Engine | In-house | MTM, Greeks, P&L calculation | Risk Technology |
| **SYS-MR-003** | Risk Engine | In-house | VaR/SVaR/IRC calculation | Risk Technology |
| **SYS-MR-004** | Risk Reporting DataMart | In-house (SQL Server) | Risk dashboards and reports | Risk Technology |
| **SYS-MR-005** | Trade ODS | In-house (Oracle) | Trade and position data | Risk Technology |
| **SYS-MR-006** | Market Data ODS | In-house (Oracle) | EOD market data | Risk Technology |
| **SYS-MR-007** | Valuations ODS | In-house (Oracle) | MTM and sensitivities | Risk Technology |
| **SYS-MR-008** | Risk ODS | In-house (Oracle) | VaR results and P&L strips | Risk Technology |
| **SYS-MR-009** | P&L ODS | In-house (Oracle) | Trading P&L (sub-ledger) | Finance Technology |
| **SYS-MR-010** | Time Series ODS | In-house (Oracle) | Historical returns | Risk Technology |
| **SYS-MR-011** | Hierarchy ODS | In-house (Oracle) | Book hierarchy | Finance Technology |

### 3.2 External Data Sources

| System ID | System Name | Vendor | Data Provided | Owner |
|-----------|-------------|--------|---------------|-------|
| **SYS-MR-012** | Bloomberg Terminal | Bloomberg | Prices, curves, vol surfaces | Market Data Control |
| **SYS-MR-013** | Reuters Eikon | LSEG | Prices, curves, vol surfaces | Market Data Control |
| **SYS-MR-014** | Exchange Feeds | Various | Settlement prices | Market Data Control |
| **SYS-MR-015** | Enterprise Data Hub | In-house (Informatica) | Data integration | Enterprise Data |

---

## 4. Data Feed Inventory

### 4.1 Inbound Feeds (to Market Risk)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        INBOUND DATA FEED INVENTORY                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  FEED   │ SOURCE        │ TARGET     │ FREQUENCY │ SLA      │ VOLUME    │ CRITICAL?     │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  TRADE AND POSITION FEEDS                                                               │
│  ────────────────────────                                                               │
│  TRD-001│ Murex         │ Trade ODS  │ Real-time │ <5 min   │ ~5k/day   │ Yes           │
│  TRD-002│ Murex         │ Trade ODS  │ EOD batch │ 18:30    │ ~50k pos  │ Yes           │
│  TRD-003│ External BOs  │ Trade ODS  │ EOD batch │ 18:00    │ ~2k pos   │ Yes           │
│                                                                                         │
│  MARKET DATA FEEDS                                                                      │
│  ──────────────────                                                                     │
│  MKT-001│ Bloomberg     │ MD ODS     │ Real-time │ <1 sec   │ ~50k/sec  │ Yes           │
│  MKT-002│ Reuters       │ MD ODS     │ Real-time │ <1 sec   │ ~30k/sec  │ Yes           │
│  MKT-003│ Bloomberg     │ MD ODS     │ EOD snap  │ 17:30    │ ~100k pts │ Yes           │
│  MKT-004│ Reuters       │ MD ODS     │ EOD snap  │ 17:30    │ ~80k pts  │ Yes           │
│  MKT-005│ Exchanges     │ MD ODS     │ EOD       │ 18:00    │ ~20k pts  │ Yes           │
│  MKT-006│ Internal marks│ MD ODS     │ EOD       │ 17:00    │ ~5k pts   │ Yes           │
│                                                                                         │
│  REFERENCE DATA FEEDS                                                                   │
│  ─────────────────────                                                                  │
│  REF-001│ Security MDM  │ Trade ODS  │ Daily     │ 06:00    │ ~500k sec │ Yes           │
│  REF-002│ Counterparty  │ Trade ODS  │ Daily     │ 06:00    │ ~100k cpy │ Yes           │
│  REF-003│ Hierarchy     │ Hier ODS   │ Daily     │ 05:00    │ ~10k map  │ Yes           │
│                                                                                         │
│  FINANCE FEEDS                                                                          │
│  ─────────────                                                                          │
│  FIN-001│ Finance GL    │ P&L ODS    │ EOD       │ 21:00    │ ~50k rows │ Yes           │
│  FIN-002│ IPV results   │ Val ODS    │ EOD       │ 18:30    │ ~5k adj   │ Yes           │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Outbound Feeds (from Market Risk)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        OUTBOUND DATA FEED INVENTORY                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  FEED   │ SOURCE     │ TARGET           │ FREQUENCY │ SLA      │ VOLUME    │ CRITICAL?  │
│  ────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                         │
│  RISK REPORTING FEEDS                                                                   │
│  ─────────────────────                                                                  │
│  RPT-001│ Risk ODS   │ Risk DataMart    │ Daily     │ 04:30    │ ~100k rows│ Yes        │
│  RPT-002│ Risk ODS   │ MLRC Dashboard   │ Daily     │ 07:00    │ Summary   │ Yes        │
│  RPT-003│ Risk ODS   │ Limit System     │ Daily     │ 05:00    │ ~500 lim  │ Yes        │
│                                                                                         │
│  REGULATORY FEEDS                                                                       │
│  ─────────────────                                                                      │
│  REG-001│ Risk ODS   │ Capital System   │ Daily     │ 06:00    │ ~50 rows  │ Yes        │
│  REG-002│ Risk ODS   │ COREP Extract    │ Monthly   │ T+5      │ Templates │ Yes        │
│  REG-003│ Risk ODS   │ PRA Portal       │ On demand │ Varies   │ Ad-hoc    │ Yes        │
│                                                                                         │
│  FINANCE FEEDS                                                                          │
│  ─────────────                                                                          │
│  FIN-003│ Val ODS    │ Finance GL       │ Daily     │ 22:00    │ ~50k rows │ Yes        │
│  FIN-004│ Risk ODS   │ Capital Planning │ Monthly   │ T+3      │ ~1k rows  │ Medium     │
│                                                                                         │
│  DOWNSTREAM SYSTEMS                                                                     │
│  ──────────────────                                                                     │
│  DST-001│ Risk ODS   │ Credit Risk      │ Daily     │ 05:00    │ ~10k rows │ Medium     │
│  DST-002│ Risk ODS   │ Treasury         │ Daily     │ 06:00    │ ~500 rows │ Medium     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Feed Criticality Matrix

| Criticality | Definition | Examples | RTO | RPO |
|-------------|------------|----------|-----|-----|
| **Critical** | VaR production blocked without feed | Trade ODS, Market Data, Time Series | 1 hour | 0 |
| **High** | Degraded VaR production | Hierarchy updates, IPV adjustments | 4 hours | 4 hours |
| **Medium** | Reporting impacted | MLRC dashboard, regulatory feeds | 8 hours | 24 hours |
| **Low** | No immediate impact | Archive feeds, ad-hoc reports | 24 hours | 48 hours |

---

## 5. System Interfaces

### 5.1 Interface Specifications

| Interface ID | From System | To System | Protocol | Format | Frequency |
|--------------|-------------|-----------|----------|--------|-----------|
| **IF-001** | Murex | Trade ODS | MQ | XML | Real-time |
| **IF-002** | Murex | Trade ODS | FTP | CSV | Batch (EOD) |
| **IF-003** | Bloomberg | MD ODS | B-PIPE | BLPAPI | Real-time |
| **IF-004** | MD ODS | Time Series ODS | DB Link | SQL | EOD batch |
| **IF-005** | Trade ODS | Valuation Engine | API | JSON | EOD batch |
| **IF-006** | Valuation Engine | Valuations ODS | DB Write | SQL | EOD batch |
| **IF-007** | Valuations ODS | Risk Engine | DB Read | SQL | EOD batch |
| **IF-008** | Time Series ODS | Risk Engine | DB Read | SQL | EOD batch |
| **IF-009** | Hierarchy ODS | Risk Engine | DB Read | SQL | EOD batch |
| **IF-010** | Risk Engine | Risk ODS | DB Write | SQL | EOD batch |
| **IF-011** | Risk ODS | Risk DataMart | ETL | SQL | EOD batch |
| **IF-012** | Risk DataMart | MLRC Dashboard | API | JSON | On-demand |

### 5.2 Interface Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        KEY INTERFACE FLOWS                                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│                                                                                         │
│   MUREX ─────────┬─────────▶ TRADE ODS ──────────────┐                                  │
│       │          │ IF-001/002                        │                                  │
│       │          │                                   │                                  │
│       │    ┌─────┴──────┐                            │                                  │
│       │    │            │                            │                                  │
│   BLOOMBERG ─────────────▶ MARKET DATA ODS           │                                  │
│   IF-003   │            │         │                  │                                  │
│            │            │         │ IF-004           │ IF-005                           │
│   REUTERS ──────────────┤         │                  │                                  │
│                         │         ▼                  ▼                                  │
│                         │   TIME SERIES ODS    VALUATION ENGINE                         │
│                         │         │                  │                                  │
│                         │         │ IF-008           │ IF-006                           │
│                         │         │                  │                                  │
│   HIERARCHY ODS ────────┼─────────┼──────────▶ VALUATIONS ODS                           │
│   IF-009                │         │                  │                                  │
│                         │         │                  │ IF-007                           │
│                         │         │                  │                                  │
│                         │         ▼                  ▼                                  │
│                         │      ┌──────────────────────────┐                             │
│                         │      │      RISK ENGINE         │                             │
│                         │      │                          │                             │
│                         │      └────────────┬─────────────┘                             │
│                         │                   │ IF-010                                    │
│                         │                   ▼                                           │
│                         │             RISK ODS                                          │
│                         │                   │ IF-011                                    │
│                         │                   ▼                                           │
│                         │        RISK REPORTING DATAMART                                │
│                         │                   │ IF-012                                    │
│                         │                   ▼                                           │
│                         │           MLRC DASHBOARD                                      │
│                         │                                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. System Specifications

### 6.1 Risk Engine - SYS-MR-003

| Attribute | Specification |
|-----------|---------------|
| **Type** | In-house developed |
| **Version** | 3.2 |
| **Architecture** | Distributed grid computing |
| **Compute Nodes** | 50 (scalable to 100) |
| **Database** | Oracle 19c RAC |
| **Operating System** | RHEL 8.5 |
| **Memory** | 256 GB per node |
| **Storage** | 50 TB SAN |

**Capabilities**:
- Historical Simulation VaR (99%, 1-day and 10-day)
- Stressed VaR (dynamic stressed period)
- **Earnings at Risk (EaR)** calculation (90%, 1-year scaled) - feeds Risk Appetite monitoring
- **Economic Capital (ECAP)** calculation (99.9%, liquidity-adjusted horizons) - feeds ICAAP
- IRC (Incremental Risk Charge)
- Scenario stress testing
- P&L strip generation
- Hierarchy aggregation
- Risk factor contribution analysis
- Aged inventory identification and ICAAP contribution
- Risk Appetite dashboard feeds (EaR vs limits)

### 6.2 Trade ODS - SYS-MR-005

| Attribute | Specification |
|-----------|---------------|
| **Database** | Oracle 19c |
| **Architecture** | Active-Passive cluster |
| **Storage** | 10 TB |
| **Retention** | 7 years (regulatory) |
| **Records** | ~50,000 positions daily |

**Key Tables**:

| Table | Description | Records |
|-------|-------------|---------|
| TRADE_MASTER | Trade static data | ~500,000 |
| POSITION_EOD | Daily position snapshot | ~50,000/day |
| TRADE_AMENDMENT | Trade amendments | ~5,000/day |
| SECURITY_MASTER | Security reference data | ~500,000 |

### 6.3 Time Series ODS - SYS-MR-010

| Attribute | Specification |
|-----------|---------------|
| **Database** | Oracle 19c |
| **Architecture** | Single instance with standby |
| **Storage** | 5 TB |
| **Risk Factors** | ~5,000 active |
| **History Depth** | 500+ business days per factor |

**Key Tables**:

| Table | Description | Records |
|-------|-------------|---------|
| RISK_FACTOR_MASTER | Risk factor definitions | ~5,000 |
| TIME_SERIES_DATA | Daily returns | ~2.5M |
| STRESSED_PERIOD_DATA | Stressed period returns | ~1.25M |
| PROXY_MAPPING | Proxy relationships | ~500 |

---

## 7. Data Flow Timing

### 7.1 Daily Processing Timeline

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        DAILY PROCESSING TIMELINE (GMT/BST)                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  TIME     │  PROCESS                              │  SYSTEM          │  STATUS          │
│  ─────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                         │
│  MARKET DATA CAPTURE (17:00 - 18:30)                                                    │
│  ─────────────────────────────────                                                      │
│  17:00    │  Internal marks collection begins     │  Murex           │  FO input        │
│  17:30    │  Bloomberg EOD snapshot               │  Bloomberg       │  Automated       │
│  17:30    │  Reuters EOD snapshot                 │  Reuters         │  Automated       │
│  18:00    │  Exchange settlement prices           │  Exchange feeds  │  Automated       │
│  18:00    │  IPV price validation begins          │  MD ODS          │  MDC review      │
│  18:30    │  EOD Market Data Snapshot published   │  MD ODS          │  SLA             │
│                                                                                         │
│  TRADE CAPTURE (17:00 - 19:00)                                                          │
│  ──────────────────────────────                                                         │
│  17:00    │  Trade cut-off (Asia)                 │  Murex           │  FO              │
│  17:30    │  Trade cut-off (London)               │  Murex           │  FO              │
│  18:00    │  EOD trade extract begins             │  Murex           │  Automated       │
│  18:30    │  Trade reconciliation                 │  Trade ODS       │  Ops             │
│  19:00    │  Trade ODS refresh complete           │  Trade ODS       │  SLA             │
│                                                                                         │
│  VALUATION (19:00 - 21:00)                                                              │
│  ────────────────────────────                                                           │
│  19:00    │  Valuation batch begins               │  Val Engine      │  Automated       │
│  20:00    │  MTM validation                       │  Val ODS         │  RAV             │
│  21:00    │  Valuation ODS refresh complete       │  Val ODS         │  SLA             │
│                                                                                         │
│  TIME SERIES (19:00 - 22:00)                                                            │
│  ──────────────────────────                                                             │
│  19:00    │  Time series update begins            │  TS ODS          │  Automated       │
│  20:00    │  Data quality validation              │  TS ODS          │  RAV             │
│  21:00    │  Proxy application (if needed)        │  TS ODS          │  RAV             │
│  22:00    │  Time Series ODS ready                │  TS ODS          │  SLA             │
│                                                                                         │
│  RISK CALCULATION (22:00 - 04:00+1)                                                     │
│  ───────────────────────────────────                                                    │
│  22:00    │  Risk Engine batch begins             │  Risk Engine     │  Automated       │
│  22:15    │  Input validation complete            │  Risk Engine     │  Automated       │
│  01:00+1  │  P&L strip calculation complete       │  Risk Engine     │  Automated       │
│  02:30+1  │  Hierarchy aggregation complete       │  Risk Engine     │  Automated       │
│  03:30+1  │  Percentile calculation complete      │  Risk Engine     │  Automated       │
│  04:00+1  │  Risk ODS refresh complete            │  Risk ODS        │  SLA             │
│                                                                                         │
│  REPORTING (04:00 - 07:30+1)                                                            │
│  ──────────────────────────────                                                         │
│  04:00+1  │  Risk DataMart ETL begins             │  DataMart        │  Automated       │
│  04:30+1  │  VaR validation checks                │  DataMart        │  RAV             │
│  05:00+1  │  Limit breach identification          │  DataMart        │  RAV             │
│  05:30+1  │  Quality sign-off                     │  DataMart        │  RAV             │
│  06:00+1  │  Capital feed published               │  Capital System  │  Automated       │
│  07:00+1  │  VaR Report available                 │  DataMart        │  SLA             │
│  07:30+1  │  MLRC Dashboard updated               │  Dashboard       │  SLA             │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Critical Path

```
Trade ODS (19:00) → Valuation Engine (21:00) → Valuations ODS (21:00)
                                                      │
                                                      ├──────────────────────────▶
                                                      │                          │
Time Series ODS (22:00) ──────────────────────────────┴──▶ Risk Engine (04:00+1) │
                                                                   │             │
Hierarchy ODS (daily refresh) ─────────────────────────────────────┘             │
                                                                                 │
                                                      Risk DataMart (07:00+1) ◀──┘
```

---

## 8. Business Continuity

### 8.1 DR Architecture

| System | Primary Site | DR Site | Replication | RTO | RPO |
|--------|--------------|---------|-------------|-----|-----|
| **Risk Engine** | London DC | Reading DC | Async | 4 hours | 1 hour |
| **Trade ODS** | London DC | Reading DC | Sync | 2 hours | 0 |
| **Time Series ODS** | London DC | Reading DC | Async | 4 hours | 4 hours |
| **Risk ODS** | London DC | Reading DC | Async | 4 hours | 1 hour |
| **Risk DataMart** | London DC | Reading DC | Async | 8 hours | 4 hours |

### 8.2 Failover Scenarios

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        FAILOVER SCENARIOS                                               │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  SCENARIO 1: Single System Failure                                                      │
│  ─────────────────────────────────                                                      │
│  • Automatic failover to standby instance                                               │
│  • Batch restart from last checkpoint                                                   │
│  • RTO: 1-2 hours                                                                       │
│                                                                                         │
│  SCENARIO 2: Data Center Failure (London)                                               │
│  ─────────────────────────────────────────                                              │
│  • Manual failover to Reading DR site                                                   │
│  • Declare DR event; activate DR procedures                                             │
│  • RTO: 4 hours                                                                         │
│  • May require partial re-run from EOD snapshots                                        │
│                                                                                         │
│  SCENARIO 3: Bloomberg/Reuters Outage                                                   │
│  ─────────────────────────────────────────                                              │
│  • Switch to backup data provider                                                       │
│  • Use internal marks where available                                                   │
│  • Flag positions with proxy data                                                       │
│  • RTO: 1 hour                                                                          │
│                                                                                         │
│  SCENARIO 4: Complete Infrastructure Failure                                            │
│  ──────────────────────────────────────────                                             │
│  • Activate manual VaR estimation procedures                                            │
│  • Use T-1 VaR + sensitivity-based adjustment                                           │
│  • Apply 20% conservative buffer                                                        │
│  • Notify MLRC and CRO                                                                  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 8.3 BCP Contact Matrix

| Role | Name | Phone | Escalation |
|------|------|-------|------------|
| Risk Technology Manager | [Name] | [Phone] | 1st level |
| Head of Risk Technology | [Name] | [Phone] | 2nd level |
| Head of Market Risk Analytics | [Name] | [Phone] | 3rd level |
| CRO | [Name] | [Phone] | 4th level |
| IT BCP Coordinator | [Name] | [Phone] | DR activation |

---

## 9. Support Arrangements

### 9.1 Vendor Support

| System | Vendor | Contract | Support Hours | SLA Response |
|--------|--------|----------|---------------|--------------|
| **Risk Engine** | In-house (L3 support) | N/A | 24/7 (on-call) | 1 hour (P1) |
| **Murex** | Murex | Enterprise | 24/7 | 2 hours (P1) |
| **Bloomberg** | Bloomberg | Enterprise | 24/7 | 1 hour (P1) |
| **Oracle** | Oracle | Platinum | 24/7 | 1 hour (P1) |

### 9.2 Internal Support Model

| Tier | Team | Coverage | Responsibilities |
|------|------|----------|------------------|
| **L1** | Risk Operations | 07:00-19:00 GMT | Monitoring, alerts, basic troubleshooting |
| **L2** | Risk Technology | 07:00-22:00 GMT | System issues, batch failures, data issues |
| **L3** | Risk Technology (On-call) | 24/7 | Critical issues, DR activation |
| **L4** | Vendor Support | 24/7 | Product bugs, complex technical issues |

### 9.3 Incident Severity Matrix

| Severity | Definition | Response Time | Resolution Target |
|----------|------------|---------------|-------------------|
| **P1 - Critical** | VaR production blocked | 15 minutes | 2 hours |
| **P2 - High** | VaR production degraded | 30 minutes | 4 hours |
| **P3 - Medium** | Reporting impacted | 2 hours | 8 hours |
| **P4 - Low** | Minor issue | 8 hours | 24 hours |

---

## 10. Change Management

### 10.1 Change Categories

| Category | Definition | Approval | Lead Time |
|----------|------------|----------|-----------|
| **Emergency** | Fix critical production issue | Risk Technology Manager | Immediate |
| **Standard** | Pre-approved change types | Change Manager | 24 hours |
| **Normal** | System changes, upgrades | CAB | 5 business days |
| **Major** | New systems, major upgrades | Technology Steering Committee | 20 business days |

### 10.2 Change Windows

| Window | Time | Scope | Blackout |
|--------|------|-------|----------|
| **Daily maintenance** | 06:00-07:00 GMT | Minor patches | None |
| **Weekend maintenance** | Saturday 06:00 - Sunday 18:00 | Major changes | Month-end, quarter-end |
| **Emergency** | Any time | Critical fixes | Approval required |

### 10.3 Pre-Production Testing

| Environment | Purpose | Data |
|-------------|---------|------|
| **DEV** | Development and unit testing | Synthetic |
| **SIT** | System integration testing | Masked production |
| **UAT** | User acceptance testing | Masked production (T-1) |
| **PRE-PROD** | Final validation | Production copy |

---

## 11. Data Quality Framework

### 11.1 Quality Dimensions

| Dimension | Definition | Metrics |
|-----------|------------|---------|
| **Completeness** | All required data present | % records populated |
| **Accuracy** | Data reflects true values | Reconciliation breaks |
| **Timeliness** | Data available when needed | SLA adherence |
| **Consistency** | Data matches across systems | Cross-system reconciliation |
| **Uniqueness** | No duplicate records | Duplicate count |

### 11.2 Quality Controls

| Control | Frequency | Owner | Threshold |
|---------|-----------|-------|-----------|
| Trade count reconciliation | Daily | Trading Ops | ±1% |
| Market data completeness | Daily | MDC | 100% |
| Time series completeness | Daily | RAV | 100% |
| VaR reasonableness | Daily | RAV | ±50% vs T-1 |
| Hierarchy integrity | Weekly | RAV | 100% |

### 11.3 BCBS 239 Compliance

| Principle | Requirement | Status |
|-----------|-------------|--------|
| **Governance** | Data ownership and accountability | Compliant |
| **Data Architecture** | Single source of truth | Compliant |
| **Accuracy & Integrity** | Validation controls | Compliant |
| **Completeness** | All material risks captured | Compliant |
| **Timeliness** | Meet regulatory deadlines | Compliant |
| **Adaptability** | Flexible reporting | Compliant |

---

## 12. Security

### 12.1 Access Control

| System | Authentication | Authorization | Review Frequency |
|--------|----------------|---------------|------------------|
| **Risk Engine** | Active Directory | Role-based (RBAC) | Quarterly |
| **Trade ODS** | AD + DB accounts | RBAC | Quarterly |
| **Risk DataMart** | AD | Report-level | Quarterly |
| **Dashboards** | AD + MFA | Role-based | Monthly |

### 12.2 Data Classification

| Classification | Examples | Controls |
|----------------|----------|----------|
| **Highly Confidential** | Position data, VaR results | Encryption, access logging |
| **Confidential** | Market data, methodology | Access control |
| **Internal** | Reports, dashboards | Standard security |
| **Public** | Published regulatory reports | N/A |

---

## 13. Glossary of Systems

| Abbreviation | Full Name | Description |
|--------------|-----------|-------------|
| **RE** | Risk Engine | In-house VaR/SVaR calculation system |
| **ODS** | Operational Data Store | Integrated data repository |
| **ETL** | Extract Transform Load | Data integration process |
| **MQ** | Message Queue | IBM messaging middleware |
| **RAC** | Real Application Clusters | Oracle high availability |
| **SAN** | Storage Area Network | Enterprise storage |
| **DR** | Disaster Recovery | Business continuity site |
| **CAB** | Change Advisory Board | Change approval forum |

---

## 13. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Data Dictionary](./data-dictionary.md) | MR-L7-002 | Field-level definitions for all metrics |
| [Feeds Overview](./feeds-overview.md) | MR-L7-003 | Comprehensive feed documentation |
| [VaR/SVaR Methodology](./var-svar-methodology.md) | MR-L6-001 | Risk calculation methodology |
| [ECAP Methodology](./ecap-methodology.md) | MR-L6-002 | Economic capital methodology |
| [Risk Engine Calculation](../../L4-Processes/processes/risk-engine-calculation.md) | MR-L4-006 | Process that uses this architecture |
| [Time Series Management](../../L4-Processes/processes/time-series-management/time-series-overview.md) | MR-L4-005 | Market data sourcing process |

---

## 14. Document Control

### 14.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | Technology Steering Committee |
| 1.1 | 2025-01-16 | Updated Risk Engine to in-house system (removed vendor-specific references) | Risk Technology |
| 1.2 | 2025-01-17 | Added ECAP calculation and aged inventory capabilities; updated metadata linkages to L4/L5/L6 | Risk Technology |
| 1.3 | 2025-01-17 | Added EaR calculation capability; linked to Risk Appetite Statement (GOV-L3-010); updated Risk ODS outputs | Risk Technology |

### 14.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Feed inventory | Quarterly | April 2025 |
| DR test | Semi-annual | July 2025 |
| Security review | Annual | January 2026 |

---

*End of Document*
