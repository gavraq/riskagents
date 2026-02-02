---
# Process Metadata
process_id: MR-L4-002
process_name: Trade Capture Controls
version: 1.0
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Trading Operations Manager
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-001  # Market Risk Process Orchestration (orchestration)
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-022  # BCBS 239
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
l7_systems:
  - SYS-MR-001  # Murex (and other front office systems)
  - SYS-MR-005  # Trade ODS (TradeHub)
  - SYS-MR-012  # Snapshot Service
---

# Trade Capture Controls Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-002 |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Market Risk Process Orchestration (MR-L4-001) |
| **Owner** | Trading Operations Manager |

---

## 1. Purpose

The Trade Capture Controls process ensures that all trades executed during the business day are **completely and accurately captured** in the Trade ODS before the VaR calculation batch begins. This process addresses the fundamental question: *"Do we have all the trades?"*

Accurate trade capture is critical because:
- VaR calculated on incomplete positions understates risk
- Missing trades can result in undetected limit breaches
- Regulatory capital calculations require complete position data
- P&L reconciliation depends on trade completeness

---

## 2. Scope

### 2.1 Trade Lifecycle Events Covered

| Event Type | Description | Risk Impact |
|------------|-------------|-------------|
| **New Trades** | New positions opened during the day | Adds new risk |
| **Amendments** | Changes to existing trade terms | Modifies existing risk |
| **Cancellations** | Trade booked in error, reversed | Removes incorrectly captured risk |
| **Novations** | Transfer to new counterparty | Changes counterparty risk |
| **Partial Terminations** | Partial unwind of position | Reduces notional/risk |
| **Full Terminations** | Complete unwind of position | Removes risk |
| **Maturities** | Trades reaching maturity date | Removes expired positions |

### 2.2 Source Systems

| System | Asset Class | Typical Daily Volume |
|--------|-------------|---------------------|
| **Murex** | Interest Rates, Structured Products | ~60,000 events |
| **FX Platform** | FX Spot, Forwards, Options | ~150,000 events |
| **Credit System** | CDS, Credit Indices | ~10,000 events |
| **Equity System** | Equities, Equity Derivatives | ~30,000 events |
| **Commodities System** | Commodity Derivatives | ~5,000 events |

### 2.3 Trade Data Formats

#### Internal Storage

The Trade ODS stores all trade data in an optimised **tabular format using compressed Parquet files**. This approach provides:

| Benefit | Description |
|---------|-------------|
| **Storage Efficiency** | Columnar compression reduces storage by 70-90% |
| **Query Performance** | Columnar format enables fast analytical queries |
| **Schema Evolution** | Parquet supports adding new fields without rewriting data |
| **Partitioning** | Data partitioned by date/book for efficient access |

#### Format Adapters

Source systems may send trade data in various formats. The Trade ODS uses **adapters** to normalise incoming data and to export data in required formats:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           TRADE ODS FORMAT ADAPTERS                                     │
│                                                                                         │
│   INBOUND ADAPTERS                 INTERNAL STORAGE              OUTBOUND ADAPTERS      │
│   (Source → ODS)                                                 (ODS → Consumer)       │
│                                                                                         │
│   ┌─────────────────┐             ┌─────────────────┐           ┌─────────────────┐     │
│   │  FpML Adapter   │────────┐    │                 │    ┌─────▶│  FpML Adapter   │     │
│   │  (OTC deriv)    │        │    │   TRADE ODS     │    │      │  (Regulatory)   │     │
│   └─────────────────┘        │    │                 │    │      └─────────────────┘     │
│   ┌─────────────────┐        │    │  ┌───────────┐  │    │      ┌─────────────────┐     │
│   │  FIX Adapter    │────────┼───▶│  │ Parquet   │  │────┼─────▶│  FIX Adapter    │     │
│   │  (Exchange/FX)  │        │    │  │ Files     │  │    │      │  (Counterparty) │     │
│   └─────────────────┘        │    │  │           │  │    │      └─────────────────┘     │
│   ┌─────────────────┐        │    │  │ Tabular   │  │    │      ┌─────────────────┐     │
│   │  JSON Adapter   │────────┤    │  │ Format    │  │    ├─────▶│  JSON Adapter   │     │
│   │  (API feeds)    │        │    │  └───────────┘  │    │      │  (Internal API) │     │
│   └─────────────────┘        │    │                 │    │      └─────────────────┘     │
│   ┌─────────────────┐        │    │  Partitioned by │    │      ┌─────────────────┐     │
│   │  CSV Adapter    │────────┘    │  • Date         │    └─────▶│  CSV Adapter    │     │
│   │  (Legacy batch) │             │  • Book         │           │  (Reporting)    │     │
│   └─────────────────┘             │  • Asset Class  │           └─────────────────┘     │
│                                   └─────────────────┘                                   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

| Adapter | Inbound Use | Outbound Use |
|---------|-------------|--------------|
| **FpML** | OTC derivatives from Murex, Summit | Regulatory reporting (EMIR), trade repositories |
| **FIX** | Exchange-traded products, FX platforms | Counterparty confirmations, clearing houses |
| **JSON** | Modern API-based source systems | Internal consumers (Risk Engine, Analytics) |
| **CSV** | Legacy batch extracts | Ad-hoc reporting, data extracts |

This architecture decouples internal storage efficiency from external integration requirements.

### 2.4 Out of Scope

- Trade execution (remains in front office systems)
- Pre-trade analytics
- Trade confirmation and settlement (separate Operations process - see Section 6.4)
- Regulatory reporting (separate process)

---

## 3. The Temporal Consistency Challenge

### 3.1 Problem Statement

In a real-time trading environment, determining "what trades were active at EOD" is non-trivial:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    THE TEMPORAL CONSISTENCY CHALLENGE                                   │
│                                                                                         │
│  Question: "At 17:00 GMT, what trades were active?"                                     │
│                                                                                         │
│  Challenge: Messages arrive with delays, amendments occur after the fact                │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐    │
│  │  Timeline                                                                       │    │
│  │  ─────────────────────────────────────────────────────────────────────────────  │    │
│  │                                                                                 │    │
│  │  16:55    Trade T1 executed (business timestamp)                                │    │
│  │  16:58    Trade T1 message arrives at Trade ODS                                 │    │
│  │  17:00    ← EOD SNAPSHOT TIME                                                   │    │
│  │  17:02    Trade T2 executed at 16:59 (message delayed 3 min)                    │    │
│  │  17:05    Amendment to T1 (effective 16:57) arrives                             │    │
│  │  17:10    Cancellation of T3 (was booked in error at 16:30)                     │    │
│  │                                                                                 │    │
│  └─────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│  Without proper handling:                                                               │
│  • T2 would be MISSED (delayed arrival after snapshot time)                             │
│  • T1 would have WRONG STATE (amendment not yet applied)                                │
│  • T3 would be INCORRECTLY INCLUDED (cancellation not yet processed)                    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Solution: Snapshot Service with Buffers

The Trade ODS uses a **Snapshot Service** with configurable buffers to ensure temporal consistency:

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| **Snapshot Timestamp** | Business cut-off time | 17:00 GMT |
| **Latency Buffer** | Time allowance for delayed messages | 5 minutes |
| **Amendment Buffer** | Time allowance for post-snapshot corrections | 30 minutes |

**Effective EOD Position Rule:**
- Include trades where business timestamp ≤ 17:00 GMT
- AND trade was still active at 17:00 (not terminated before)
- AND observation timestamp ≤ 17:05 (snapshot time + latency buffer)
- Apply amendments/cancellations observed by 17:30 (snapshot time + amendment buffer)

---

## 4. Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        TRADE CAPTURE CONTROLS PROCESS                                   │
│                        (Daily - London Time)                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

Throughout Day ─────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 CONTINUOUS TRADE CAPTURE                                │
          │  │                                                                         │
          │  │   FRONT OFFICE SYSTEMS                      TRADE ODS (TRADEHUB)        │
          │  │   ┌─────────────────┐                       ┌─────────────────┐         │
          │  │   │  Murex          │──────────────────────▶│                 │         │
          │  │   └─────────────────┘    Real-time events   │  Normalisation  │         │
          │  │   ┌─────────────────┐                       │  • table format │         │
          │  │   │  FX Platform    │──────────────────────▶│  • Validation   │         │
          │  │   └─────────────────┘                       │  • De-dup       │         │
          │  │   ┌─────────────────┐                       │                 │         │
          │  │   │  Credit System  │──────────────────────▶│  Versioning     │         │
          │  │   └─────────────────┘                       │  • Full history │         │
          │  │   ┌─────────────────┐                       │  • Audit trail  │         │
          │  │   │  Equity System  │──────────────────────▶│                 │         │
          │  │   └─────────────────┘                       └─────────────────┘         │
          │  │                                                                         │
          │  │   SLA: Trade events captured within 60 seconds of execution             │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
16:30 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 PRE-EOD RECONCILIATION                                  │
          │  │                                                                         │
          │  │  Trading Operations performs pre-close checks:                          │
          │  │  • Compare front office trade counts vs. Trade ODS                      │
          │  │  • Identify any reconciliation breaks                                   │
          │  │  • Investigate and resolve breaks before close                          │
          │  │                                                                         │
          │  │  ┌────────────────────────────────────────────────────────────────────┐ │
          │  │  │  PRE-EOD RECON DASHBOARD                                           │ │
          │  │  │                                                                    │ │
          │  │  │  System          FO Count    ODS Count    Variance    Status       │ │
          │  │  │  ───────────────────────────────────────────────────────────────── │ │
          │  │  │  Murex           58,234      58,234       0           ✓ OK         │ │
          │  │  │  FX Platform     148,902     148,899      -3          ⚠ BREAK      │ │
          │  │  │  Credit System   9,876       9,876        0           ✓ OK         │ │
          │  │  │  Equity System   29,445      29,445       0           ✓ OK         │ │
          │  │  │                                                                    │ │
          │  │  └────────────────────────────────────────────────────────────────────┘ │
          │  │                                                                         │
          │  │  Breaks must be resolved before 17:00 GMT or escalated                  │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
17:00 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 EOD CUT-OFF                                             │
          │  │                                                                         │
          │  │  • London markets officially closed for risk purposes                   │
          │  │  • Snapshot timestamp set to 17:00 GMT                                  │
          │  │  • Late trades flagged for review (accepted if business timestamp       │
          │  │    was before 17:00)                                                    │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
17:05 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 LATENCY BUFFER CLOSE                                    │
          │  │                                                                         │
          │  │  • Latency buffer (5 min) expires                                       │
          │  │  • All delayed messages with business timestamp ≤ 17:00 included        │
          │  │  • Trade count for snapshot baseline established                        │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
17:30 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 AMENDMENT BUFFER CLOSE                                  │
          │  │                                                                         │
          │  │  • Amendment buffer (30 min) expires                                    │
          │  │  • All amendments/cancellations effective at 17:00 applied              │
          │  │  • Final snapshot positions frozen                                      │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
18:00 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 FINAL RECONCILIATION                                    │
          │  │                                                                         │
          │  │  Trading Operations performs post-close reconciliation:                 │
          │  │  • Final trade count comparison (FO vs. Trade ODS)                      │
          │  │  • Position-level reconciliation for material desks                     │
          │  │  • Late booking analysis (trades after 17:00)                           │
          │  │  • Confirmation status review                                           │
          │  │                                                                         │
          │  │  ┌────────────────────────────────────────────────────────────────────┐ │
          │  │  │  FINAL EOD RECON REPORT                                            │ │
          │  │  │                                                                    │ │
          │  │  │  Snapshot ID: SNAP-20250115-1700-GMT                               │ │
          │  │  │  Snapshot Timestamp: 2025-01-15 17:00:00 GMT                       │ │
          │  │  │  Query Timestamp: 2025-01-15 17:35:00 GMT                          │ │
          │  │  │                                                                    │ │
          │  │  │  Total Trades in Snapshot: 246,457                                 │ │
          │  │  │  Late Arrivals (latency buffer): 234                               │ │
          │  │  │  Amendments Applied (amendment buffer): 89                         │ │
          │  │  │  Cancellations Applied: 12                                         │ │
          │  │  │                                                                    │ │
          │  │  │  Reconciliation Status: ✓ RECONCILED                               │ │
          │  │  │                                                                    │ │
          │  │  └────────────────────────────────────────────────────────────────────┘ │
          │  │                                                                         │
          │  │  Sign-off: Trading Operations Manager                                   │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
19:00 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 POSITION SNAPSHOT PUBLICATION                           │
          │  │                                                                         │
          │  │  Trade ODS publishes official EOD position snapshot:                    │
          │  │  • Position data frozen for downstream consumption                      │
          │  │  • Snapshot ID published to consumers                                   │
          │  │  • Valuation Engine, Risk Engine notified                               │
          │  │                                                                         │
          │  │  Downstream consumers:                                                  │
          │  │  • Valuation Engine → MTM calculation                                   │
          │  │  • Risk Engine → VaR calculation                                        │
          │  │  • Finance → P&L calculation                                            │
          │  │  • Regulatory Reporting → Position reports                              │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
          ▼
    [To Valuation Engine / Risk Engine]
```

---

## 5. Trade Data Model

### 5.1 Key Entities

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           TRADE ODS DATA MODEL                                          │
│                                                                                         │
│  ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐                │
│  │  Counterparty   │──────▶│      Trade      │◀──────│      Book       │                │
│  │  (Party ODS)    │       │                 │       │ (Hierarchy ODS) │                │
│  └─────────────────┘       └────────┬────────┘       └─────────────────┘                │
│                                     │                                                   │
│                                     │ 1:N                                               │
│                                     ▼                                                   │
│  ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐                │
│  │     Product     │◀──────│    Trade Leg    │──────▶│   Cash Flows    │                │
│  │  (Product ODS)  │       │                 │       │                 │                │
│  └─────────────────┘       └─────────────────┘       └─────────────────┘                │
│                                     │                                                   │
│                                     │ 1:N                                               │
│                                     ▼                                                   │
│                            ┌─────────────────┐                                          │
│                            │  Trade Version  │                                          │
│                            │  (Full History) │                                          │
│                            └─────────────────┘                                          │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Core Trade Attributes

| Attribute | Type | Description | Mandatory |
|-----------|------|-------------|-----------|
| `trade_id` | String | Unique trade identifier | Yes |
| `uti` | String | Unique Transaction Identifier (EMIR) | Yes* |
| `trade_date` | Date | Trade execution date | Yes |
| `effective_date` | Date | Trade start date | Yes |
| `maturity_date` | Date | Trade end date | Yes |
| `counterparty_id` | String | External counterparty | Yes |
| `book_id` | String | Trading book | Yes |
| `product_type` | String | Product classification | Yes |
| `trade_status` | Enum | Active/Terminated/Novated | Yes |
| `source_system` | String | Originating FO system | Yes |
| `version` | Integer | Trade version number | Yes |
| `version_timestamp` | DateTime | Version creation time | Yes |
| `observation_timestamp` | DateTime | When ODS received message | Yes |

*UTI mandatory for EMIR-reportable trades

### 5.3 Trade Lifecycle Events

| Event | Description | Version Impact |
|-------|-------------|----------------|
| **NEW** | New trade booked | Creates version 1 |
| **AMEND** | Trade terms modified | Creates new version |
| **CANCEL** | Trade cancelled (error) | Sets status to Cancelled |
| **NOVATE** | Transfer to new counterparty | Creates new trade, terminates old |
| **PARTIAL_TERMINATE** | Partial unwind | Reduces notional, new version |
| **TERMINATE** | Full unwind | Sets status to Terminated |
| **MATURE** | Trade reached maturity | Sets status to Matured |

---

## 6. Reconciliation Framework

### 6.1 Reconciliation Levels

| Level | Description | Frequency | Tolerance |
|-------|-------------|-----------|-----------|
| **Trade Count** | Number of trades per system | Pre-EOD, Post-EOD | Zero tolerance |
| **Position** | Net position per book/product | Post-EOD | ±0.01% of notional |
| **Notional** | Total notional per book | Post-EOD | ±$100k |
| **Risk Sensitivity** | DV01/CS01/Vega per book | Weekly | ±5% |

### 6.2 Reconciliation Points

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           RECONCILIATION ARCHITECTURE                                   │
│                                                                                         │
│   FRONT OFFICE SYSTEMS                TRADE ODS                  RISK ENGINE            │
│   ┌─────────────────┐                ┌─────────────────┐        ┌─────────────────┐     │
│   │  Trade Count:   │                │  Trade Count:   │        │  Position       │     │
│   │  246,457        │◀──────────────▶│  246,457        │◀──────▶│  Snapshot:      │     │
│   │                 │   RECON #1     │                 │        │  246,457        │     │
│   │                 │                │                 │        │                 │     │
│   │  Position:      │                │  Position:      │        │  Valuation:     │     │
│   │  EUR IRS DV01   │◀──────────────▶│  EUR IRS DV01   │◀──────▶│  EUR IRS DV01   │     │
│   │  $2.5m          │   RECON #2     │  $2.5m          │        │  $2.5m          │     │
│   └─────────────────┘                └─────────────────┘        └─────────────────┘     │
│                                                                                         │
│   RECON #1: Trade Count Reconciliation (daily, zero tolerance)                          │
│   RECON #2: Position Reconciliation (daily, ±0.01%)                                     │
│   RECON #3: Risk-to-Trade reconciliation (weekly, ±5%)                                  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Break Investigation

| Break Type | Common Causes | Resolution |
|------------|---------------|------------|
| **Trade count mismatch** | Interface failure, delayed message | Check message queues; re-extract |
| **Position break** | Amendment not applied, calculation difference | Review trade versions; reconcile legs |
| **Notional break** | Currency conversion, partial termination | Check FX rates; review lifecycle events |
| **Duplicate trades** | System error, double-booking | Cancel duplicate; audit trail |

### 6.4 Confirmations Feedback Loop

Trade Operations maintains a separate **Confirmations Process** that validates trade terms with counterparties. This process provides a critical feedback loop to Trade Capture Controls:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        CONFIRMATIONS FEEDBACK LOOP                                      │
│                                                                                         │
│   TRADE CAPTURE                    CONFIRMATIONS                    TRADE ODS           │
│   ┌─────────────────┐             ┌─────────────────┐             ┌─────────────────┐   │
│   │  Trade booked   │────────────▶│  Confirmation   │             │                 │   │
│   │  in FO system   │             │  sent to        │             │  Trade stored   │   │
│   │                 │             │  counterparty   │             │  in ODS         │   │
│   └─────────────────┘             └────────┬────────┘             └─────────────────┘   │
│                                            │                                            │
│                                            ▼                                            │
│                                   ┌─────────────────┐                                   │
│                                   │  Counterparty   │                                   │
│                                   │  Response       │                                   │
│                                   └────────┬────────┘                                   │
│                                            │                                            │
│                         ┌──────────────────┼──────────────────┐                         │
│                         │                  │                  │                         │
│                         ▼                  ▼                  ▼                         │
│                ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐              │
│                │    MATCHED      │ │   UNMATCHED     │ │   DISPUTED      │              │
│                │                 │ │                 │ │                 │              │
│                │ Trade confirmed │ │ Terms differ    │ │ Counterparty    │              │
│                │ as agreed       │ │ from our record │ │ disputes trade  │              │
│                └────────┬────────┘ └────────┬────────┘ └────────┬────────┘              │
│                         │                   │                   │                       │
│                         │                   ▼                   ▼                       │
│                         │          ┌─────────────────────────────────────┐              │
│                         │          │      INVESTIGATION REQUIRED         │              │
│                         │          │                                     │              │
│                         │          │  • Compare terms with counterparty  │              │
│                         │          │  • Identify booking error           │              │
│                         │          │  • Determine correct terms          │              │
│                         │          └────────────────┬────────────────────┘              │
│                         │                           │                                   │
│                         │                           ▼                                   │
│                         │          ┌─────────────────────────────────────┐              │
│                         │          │      AMENDMENT/CANCELLATION         │              │
│                         │          │                                     │              │
│                         │          │  • Amend trade to correct terms     │              │
│                         │          │  • Cancel if trade doesn't exist    │              │
│                         │          │  • Book new trade if missing        │              │
│                         │          └────────────────┬────────────────────┘              │
│                         │                           │                                   │
│                         │                           ▼                                   │
│                         │          ┌─────────────────────────────────────┐              │
│                         └─────────▶│      TRADE ODS UPDATED              │◀─────────────┘
│                                    │                                     │              │
│                                    │  Amended/new trades flow through    │              │
│                                    │  normal capture process             │              │
│                                    └─────────────────────────────────────┘              │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Confirmation Status Categories:**

| Status | Description | Risk Impact |
|--------|-------------|-------------|
| **Confirmed** | Counterparty agrees all terms | No action required |
| **Unmatched** | Terms differ (rate, notional, dates) | Potential booking error - investigate |
| **Disputed** | Counterparty denies trade exists | Material risk - may need cancellation |
| **Pending** | Awaiting counterparty response | Monitor aging |

**Feedback to Risk:**

| Scenario | Action | Timing |
|----------|--------|--------|
| **Unmatched - material difference** | Flag trade in Risk Engine; apply conservative assumption | Same day |
| **Disputed - trade may not exist** | Exclude from VaR pending resolution | Same day |
| **Amendment from confirmation** | Process through normal amendment flow | Within amendment buffer if possible |
| **Aged unconfirmed (>5 days)** | Escalate to Market Risk; potential reserve | Weekly review |

**Note:** While Trade Confirmation is a separate Operations process, unmatched or disputed trades represent a data quality risk for VaR. Trading Operations must notify Market Risk of any material confirmation breaks that could affect position accuracy.

---

## 7. Late Booking Handling

### 7.1 Definition

A **late booking** is a trade with:
- Business timestamp > 17:00 GMT (after EOD snapshot time), OR
- Observation timestamp > 17:05 GMT (after latency buffer closes)

### 7.2 Late Booking Categories

| Category | Description | Treatment |
|----------|-------------|-----------|
| **Within Amendment Buffer** | Trade/amendment arrives 17:05-17:30 | Included in EOD snapshot if business timestamp ≤ 17:00 |
| **After Amendment Buffer** | Trade/amendment arrives after 17:30 | NOT included in EOD snapshot; captured in T+1 |
| **Post-EOD Trade** | Business timestamp after 17:00 | NOT included in EOD; captured in T+1 |

### 7.3 Late Booking Escalation

| Volume | Response | Escalation |
|--------|----------|------------|
| 1-5 late trades | Log and monitor | Trading Operations |
| 6-20 late trades | Investigate cause | Trading Operations Manager |
| >20 late trades | System issue suspected | IT + Risk Engine Ops |
| Material desk affected | VaR impact assessment | Market Risk |

### 7.4 Late Booking Report

Daily report of late bookings distributed to:
- Trading desk heads
- Trading Operations
- Market Risk
- MLRC (weekly summary)

---

## 8. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| TC-C01 | All source systems must publish trade events within 60 seconds | Preventive | IT |
| TC-C02 | Pre-EOD reconciliation must complete by 16:45 GMT | Preventive | Trading Ops |
| TC-C03 | Trade count reconciliation must show zero variance | Preventive | Trading Ops |
| TC-C04 | Post-EOD reconciliation must be signed off by 18:30 GMT | Preventive | Trading Ops |
| TC-C05 | Late bookings logged and investigated | Detective | Trading Ops |
| TC-C06 | Position reconciliation (±0.01% tolerance) | Detective | Trading Ops |
| TC-C07 | Full trade version history maintained | Detective | Trade ODS |
| TC-C08 | Regulatory identifiers (UTI/USI) validated | Preventive | Trade ODS |
| TC-C09 | Unmatched/disputed confirmations reported to Market Risk | Detective | Trading Ops |
| TC-C10 | Aged unconfirmed trades (>5 days) escalated weekly | Detective | Trading Ops |

---

## 9. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| Trade capture latency | <60 seconds | <120 seconds | IT |
| Pre-EOD recon complete | 16:45 GMT | 16:55 GMT | Trading Ops Manager |
| Post-EOD recon complete | 18:30 GMT | 19:00 GMT | Trading Ops Manager |
| Reconciliation breaks | Zero | <5 | Trading Ops Manager |
| Late booking rate | <0.1% | <0.5% | Trading desk heads |
| Position snapshot published | 19:00 GMT | 19:15 GMT | Trade ODS |

---

## 10. Exception Handling

### 10.1 Interface Failures

| Scenario | Response | Escalation |
|----------|----------|------------|
| **Single system interface down <30 min** | Queue messages; auto-replay | IT |
| **Single system interface down >30 min** | Manual extract from source | IT + Trading Ops Manager |
| **Multiple systems affected** | Halt processing; invoke BCP | IT + Head of Trading Ops |
| **Trade ODS unavailable** | Direct Murex extract; manual process | IT + Risk Engine Ops |

### 10.2 Reconciliation Breaks

| Scenario | Response | Escalation |
|----------|----------|------------|
| **Minor break (<5 trades)** | Investigate and resolve | Trading Operations |
| **Significant break (5-50 trades)** | Root cause analysis required | Trading Ops Manager |
| **Major break (>50 trades)** | System issue suspected; halt VaR | IT + Market Risk |
| **Unresolved by 19:00 GMT** | Proceed with known gap; flag VaR | Market Risk → MLRC |

---

## 11. Monitoring and Reporting

### 11.1 Real-Time Monitoring

- **Trade Flow Dashboard**: Live trade counts by source system
- **Recon Status**: Pre/post EOD reconciliation progress
- **Late Booking Monitor**: Trades arriving after cut-off
- **Interface Health**: Connectivity and message queue status

### 11.2 Daily Reports

| Report | Recipients | Content |
|--------|------------|---------|
| **Trade Capture Summary** | Trading Ops, Risk Engine Ops | Trade counts, recon status |
| **Late Booking Report** | Desk heads, Trading Ops | Late trades, root cause |
| **Reconciliation Report** | Trading Ops, RAV | Break analysis, resolution |

### 11.3 Weekly/Monthly Reports

| Report | Recipients | Content |
|--------|------------|---------|
| **Trade Capture KPIs** | MLRC | SLA performance, trends |
| **Interface Performance** | IT, Trading Ops | Latency, availability |
| **Data Quality Scorecard** | CDO, Trading Ops | Completeness, accuracy |

---

## 12. Integration Points

### 12.1 Upstream Dependencies

| System/Process | Data Provided | Impact if Delayed |
|----------------|---------------|-------------------|
| **Murex** | IR/Structured trade events | Missing interest rate positions |
| **FX Platform** | FX trade events | Missing FX positions |
| **Credit System** | Credit trade events | Missing credit positions |
| **Equity System** | Equity trade events | Missing equity positions |

### 12.2 Downstream Consumers

| System/Process | Data Consumed | Purpose |
|----------------|---------------|---------|
| **Valuation Engine** | Position snapshot | MTM calculation |
| **Risk Engine (MR-L4-006)** | Position snapshot | VaR calculation |
| **P&L ODS** | Trade events | P&L attribution |
| **Finance** | Position snapshot | Official P&L |
| **Regulatory Reporting** | Trade data | EMIR, MiFID reporting |

---

## 13. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [EOD Market Data Snapshot](./eod-market-data-snapshot.md) | Parallel process (market data) |
| [Risk Engine Calculation](./risk-engine-calculation.md) | Downstream consumer |
| [Market Risk Policy](../L3-Governance/policies/market-risk-policy.md) | Governance framework |

---

## 14. Document Control

### 14.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |

---

*End of Document*
