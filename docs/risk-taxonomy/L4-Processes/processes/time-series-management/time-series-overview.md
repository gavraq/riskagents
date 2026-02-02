---
# Process Metadata
process_id: MR-L4-005
process_name: Time Series Management
version: 1.1
effective_date: 2025-01-16
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
l6_models:
  - MR-L6-001   # Historical Simulation VaR
  - MR-L6-002   # Stressed VaR
l7_systems:
  - SYS-MR-006  # Market Data ODS
  - SYS-MR-009  # Instrument ODS
  - SYS-MR-010  # Time Series Service
  - SYS-MR-003  # Risk Engine

# Sub-Processes
sub_processes:
  - MR-L4-005a  # Instrument Setup
  - MR-L4-005b  # Risk Factor Setup
  - MR-L4-005c  # Price Collection
  - MR-L4-005d  # Cleaning & Validation
  - MR-L4-005e  # Curve Stripping
  - MR-L4-005f  # Proxying Process
---

# Time Series Management Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-005 |
| **Version** | 1.1 |
| **Effective Date** | 16 January 2025 |
| **Parent Process** | Market Risk Process Orchestration (MR-L4-001) |
| **Owner** | Head of Reporting, Analysis & Validation (RAV) |

---

## 1. Executive Summary

### 1.1 Purpose

Time Series Management is a **critical capability** that underpins the integrity of all market risk calculations at Meridian Global Bank. This process ensures that the historical price and rate observations used for Value-at-Risk (VaR), Stressed VaR (SVaR), and stress testing are:

- **Complete**: No gaps in required history
- **Accurate**: Validated against multiple sources
- **Consistent**: Aligned with valuation risk factors
- **Governed**: Subject to appropriate controls and approvals

Without robust time series management, VaR calculations would be unreliable, backtesting would fail, and regulatory capital could be misstated.

### 1.2 Why Time Series Management Matters

| Risk Calculation | Time Series Dependency |
|------------------|------------------------|
| **Historical Simulation VaR** | Requires 500+ days of historical returns for all risk factors |
| **Stressed VaR** | Requires full history back to 2007 to identify worst-case periods |
| **Backtesting** | Time series must align with P&L drivers for meaningful comparison |
| **FRTB Modellability** | Risk factors must have ≥24 observations in 12 months to be "modellable" |
| **Stress Scenario Calibration** | Historical moves inform stress shock magnitudes |

### 1.3 Process Scope

This process covers the **end-to-end lifecycle** of time series data:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         TIME SERIES MANAGEMENT LIFECYCLE                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 1.INSTRUMENT│───▶│ 2. RISK     │───▶│ 3. PRICE    │───▶│ 4. CLEANING │───▶│ 5. TIME     │
│    SETUP    │    │    FACTOR   │    │ COLLECTION  │    │ & VALIDATION│    │    SERIES   │
│             │    │    SETUP    │    │             │    │             │    │ CONSTRUCTION│
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     │                   │                   │                   │                   │
     ▼                   ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Securities  │    │ Curves,     │    │ Daily EOD   │    │ Stale/spike │    │ Attach to   │
│ static data │    │ surfaces,   │    │ observations│    │ checks,     │    │ risk factor │
│ in Instr ODS│    │ spot rates  │    │ from sources│    │ exception   │    │ + proxying  │
│             │    │ + mappings  │    │             │    │ queue       │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                                    │
                                                                                    ▼
                                                                           ┌─────────────┐
                                                                           │ TO RISK     │
                                                                           │ ENGINE      │
                                                                           │ (VaR, SVaR) │
                                                                           └─────────────┘
```

---

## 2. Organisational Context

### 2.1 Meridian Global Bank Operating Model

Meridian Global Bank operates a **global trading business** with three regional hubs:

| Region | Location | Trading Hours (Local) | EOD Snapshot Time |
|--------|----------|----------------------|-------------------|
| **Asia** | Hong Kong | 09:00 - 17:00 HKT | 17:30 HKT |
| **EMEA** | London (HQ) | 08:00 - 17:00 GMT | 17:30 GMT |
| **Americas** | New York | 08:00 - 17:00 EST | 17:30 EST |

**Key Implication for Time Series**: The Bank maintains a **single global time series** based on the **London EOD snapshot** for VaR calculation purposes. This ensures consistency in risk measurement but creates known differences versus regional P&L (addressed in the Regional EOD Management process).

### 2.2 Ownership Model

Time Series Management spans multiple functions. Clear ownership is essential:

| Function | Role in Time Series | Key Responsibilities |
|----------|---------------------|---------------------|
| **Reporting, Analysis & Validation (RAV)** | **Process Owner** | Daily operations, system updates, implementation, exception management |
| **Risk Methodologies & Analytics (RMA)** | Methodology Owner | Methodology approval, proxy approval, stale data thresholds |
| **Market Risk** | Data Owner | Risk factor requirements, proxy analysis, source selection requests |
| **Market Data Control (MDC)** | Upstream Supplier | EOD price snapshots, curve governance |
| **Trading Desks** | Upstream Supplier | Trader marks for illiquid instruments |
| **Finance / Product Control** | Upstream Supplier | IPV validation of internal prices |
| **IT / Risk Technology** | System Owner | Time Series Service, integrations |

**Key Distinctions:**
- **RAV** owns the process and performs system updates (including risk factor setup in the system)
- **RMA** owns the methodology and approves changes to thresholds, proxies, and source configurations
- **Market Risk** defines requirements and performs analysis to inform proxy/source selection decisions

### 2.3 Governance Forums

| Forum | Role in Time Series | Frequency |
|-------|---------------------|-----------|
| **MLRC** | Escalation of material issues; approve methodology changes | Weekly |
| **Proxy & RniV Forum** | Review proxy configurations; monitor non-modellable risk factors | Monthly |
| **Risk Technical Forum** | Technical methodology discussions | As needed |
| **MDC Review** | Daily curve/price validation before publication | Daily |

---

## 3. Sub-Process Overview

Time Series Management comprises six interconnected sub-processes:

### 3.1 Sub-Process Map

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              TIME SERIES SUB-PROCESSES                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                        SETUP (One-Time / As Needed)                               │  │
│  │  ┌─────────────────────────────┐    ┌─────────────────────────────┐               │  │
│  │  │  MR-L4-005a                  │    │  MR-L4-005b                  │               │  │
│  │  │  INSTRUMENT SETUP           │───▶│  RISK FACTOR SETUP          │               │  │
│  │  │                             │    │                             │               │  │
│  │  │  • Security static data     │    │  • Curve definitions        │               │  │
│  │  │  • ISIN, issuer, terms      │    │  • Surface configurations   │               │  │
│  │  │  • Golden source for trading│    │  • Spot rate mappings       │               │  │
│  │  │                             │    │  • Price source config      │               │  │
│  │  │  Owner: Operations/MDC      │    │  Owner: Market Risk (req)   │               │  │
│  │  │                             │    │          RAV (system update)│               │  │
│  │  └─────────────────────────────┘    └──────────────┬──────────────┘               │  │
│  └───────────────────────────────────────────────────┬┼──────────────────────────────┘  │
│                                                      ││                                 │
│  ┌───────────────────────────────────────────────────▼▼──────────────────────────────┐  │
│  │                           DAILY OPERATIONS                                        │  │
│  │  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐              │  │
│  │  │  MR-L4-005c        │  │  MR-L4-005d        │  │  MR-L4-005e        │              │  │
│  │  │  PRICE COLLECTION │─▶│  CLEANING &       │─▶│  CURVE STRIPPING  │              │  │
│  │  │                   │  │  VALIDATION       │  │                   │              │  │
│  │  │  • Source select  │  │  • Stale checks   │  │  • Par to zero    │              │  │
│  │  │  • External feeds │  │  • Spike detect   │  │  • XCCY from FX   │              │  │
│  │  │  • Internal marks │  │  • Exception Q    │  │  • Bootstrap      │              │  │
│  │  │                   │  │                   │  │                   │              │  │
│  │  │  Owner: RAV       │  │  Owner: RAV       │  │  Owner: RAV       │              │  │
│  │  └───────────────────┘  └───────────────────┘  └─────────┬─────────┘              │  │
│  └──────────────────────────────────────────────────────────┼────────────────────────┘  │
│                                                             │                           │
│  ┌──────────────────────────────────────────────────────────▼────────────────────────┐  │
│  │                        GAP MANAGEMENT                                             │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │  MR-L4-005f                                                                  │  │  │
│  │  │  PROXYING PROCESS                                                           │  │  │
│  │  │                                                                             │  │  │
│  │  │  • Identify gaps (new instruments, missing history)                         │  │  │
│  │  │  • Auto-proxy suggestion (correlation, country/issuer match)                │  │  │
│  │  │  • Perform analysis (correlation, volatility, tracking error)               │  │  │
│  │  │  • Select proxy methodology based on analysis (7 approved functions)        │  │  │
│  │  │  • Obtain joint approval (Head of RMA + Head of Market Risk)                │  │  │
│  │  │  • Implement and monitor                                                    │  │  │
│  │  │                                                                             │  │  │
│  │  │  Owner: Market Risk (analysis) / RMA (approval) / RAV (implementation)      │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                      AD-HOC PROCESSES                                             │  │
│  │  • Source Change Request: Market Risk may request time series use different       │  │
│  │    source - requires analysis, RMA approval, RAV implementation                   │  │
│  │  • Risk Factor Reconciliation: Periodic check that risk factors in ODS match      │  │
│  │    trading systems - discrepancies investigated and resolved                      │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                              ┌─────────────────────────────┐
                              │     CONSTRUCTED TIME        │
                              │     SERIES TO RISK ENGINE   │
                              │                             │
                              │  • 500+ days history        │
                              │  • All risk factors covered │
                              │  • Curves stripped to zeros │
                              │  • Proxies applied          │
                              │  • Ready for VaR calc       │
                              └─────────────────────────────┘
```

### 3.2 Sub-Process Summary

| ID | Sub-Process | Purpose | Frequency | Owner | Document |
|----|-------------|---------|-----------|-------|----------|
| MR-L4-005a | **Instrument Setup** | Establish security static data as golden source | As needed (new instruments) | Operations/MDC | [instrument-setup.md](./instrument-setup.md) |
| MR-L4-005b | **Risk Factor Setup** | Define curves, surfaces, spot rates and their price configurations | As needed (new risk factors) | Market Risk (requirements) / RAV (system) | [risk-factor-setup.md](./risk-factor-setup.md) |
| MR-L4-005c | **Price Collection** | Collect daily EOD observations from configured sources | Daily | RAV | [price-collection.md](./price-collection.md) |
| MR-L4-005d | **Cleaning & Validation** | Validate observations, manage exceptions | Daily | RAV | [cleaning-validation.md](./cleaning-validation.md) |
| MR-L4-005e | **Curve Stripping** | Convert par rates to zero rates; construct XCCY curves | Daily | RAV | [curve-stripping.md](./curve-stripping.md) |
| MR-L4-005f | **Proxying Process** | Fill gaps using approved proxy methodologies | As needed | Market Risk/RMA/RAV | [proxying-process.md](./proxying-process.md) |

---

## 4. Key Concepts

### 4.1 Risk Factor Taxonomy

Risk factors are the **anchor points** for time series. Meridian Global Bank maintains an FRTB-aligned risk factor taxonomy:

```
RISK FACTOR TAXONOMY (FRTB-Aligned)
│
├── GIRR - General Interest Rate Risk
│   ├── OIS Curves (discounting) - EUR, USD, GBP, JPY, CHF, AUD, CAD, HKD, SGD
│   ├── IBOR Curves (projection) - SOFR, EURIBOR, SONIA, TONAR, etc.
│   ├── Basis Curves (OIS vs IBOR spreads)
│   └── Inflation Curves (RPI, CPI, HICP)
│
├── CSR - Credit Spread Risk
│   ├── Government Bond Curves (by issuer)
│   ├── Corporate Bond Curves (by rating bucket)
│   ├── Single-Name CDS Curves
│   └── Credit Index Curves (iTraxx, CDX)
│
├── Equity Risk
│   ├── Spot Prices (linked to Instrument ODS)
│   ├── Index Levels (major indices)
│   ├── Dividend Curves
│   └── Repo Rates
│
├── FX Risk
│   ├── FX Spot Rates (vs USD base)
│   └── FX Forward Points (by tenor)
│
├── Commodity Risk
│   ├── Energy (Brent, WTI, Gas)
│   ├── Metals (Gold, Silver, Copper)
│   └── Agriculture (Wheat, Corn, Soy)
│
└── Volatility (cross-cutting)
    ├── IR Swaption Surfaces (expiry × tenor × strike)
    ├── FX Volatility Surfaces (expiry × delta)
    ├── Equity Volatility Surfaces (expiry × strike)
    └── Credit Volatility
```

### 4.2 The "One Curve, One Price" Principle

A fundamental principle at Meridian Global Bank:

> **For each risk factor, there is ONE authoritative price/rate used consistently across the Bank for a given business date.**

This means:
- **FX rates** set by the FX Desk (market-maker with best liquidity view) are used for ALL FX exposures across the Bank
- **Interest rate curves** built by Market Data Control are the single source for discounting and projection
- **Commodity prices** set by the Commodity Desk are used for all commodity exposures

**Implication for Time Series**: The time series must use the same risk factor definitions as the valuation models to ensure VaR aligns with actual P&L drivers.

### 4.3 Relationship: Risk Factors ↔ Valuations ↔ Time Series

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    RISK FACTOR CONSISTENCY REQUIREMENT                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│    RISK FACTOR DEFINITION                                                               │
│    (e.g., EUR 10Y Swap Rate)                                                            │
│              │                                                                          │
│              ├──────────────────────────────────┐                                       │
│              │                                  │                                       │
│              ▼                                  ▼                                       │
│    ┌─────────────────────────┐       ┌─────────────────────────┐                        │
│    │   VALUATION MODELS      │       │   TIME SERIES           │                        │
│    │                         │       │                         │                        │
│    │   Uses EUR 10Y rate to  │       │   Collects daily EUR    │                        │
│    │   discount cash flows   │       │   10Y observations      │                        │
│    │                         │       │                         │                        │
│    │   → Produces MTM        │       │   → Produces returns    │                        │
│    └───────────┬─────────────┘       └───────────┬─────────────┘                        │
│                │                                 │                                      │
│                └─────────────┬───────────────────┘                                      │
│                              │                                                          │
│                              ▼                                                          │
│                    ┌─────────────────────────┐                                          │
│                    │   VaR CALCULATION       │                                          │
│                    │                         │                                          │
│                    │   Applies historical    │                                          │
│                    │   returns to current    │                                          │
│                    │   sensitivities         │                                          │
│                    │                         │                                          │
│                    │   → VaR estimate        │                                          │
│                    └─────────────────────────┘                                          │
│                                                                                         │
│  KEY REQUIREMENT: Same risk factor ID must be used in valuation and time series         │
│  to ensure VaR captures the actual risk drivers of the portfolio                        │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Consistency Goal vs. Practical Constraints**

While **consistency between valuation and time series risk factors is the objective**, this is not always achievable in practice:

| Scenario | Example | Practical Approach |
|----------|---------|-------------------|
| **Valuation more granular** | Front office values 100+ issuer curves; time series tracks 10 rating-bucket curves | Time series uses representative curves; basis risk captured in RniV |
| **Tenor misalignment** | Valuation curve has 50 tenors; time series observes 12 liquid points | Interpolation/extrapolation applied in risk calculation |
| **New instrument** | No time series history exists | Proxy applied until sufficient history builds |
| **Illiquid product** | No observable market for exotic payoff | Model-based internal marks used with IPV validation |

The key is to **understand and document** any differences between valuation and time series risk factors, and to capture the resulting **basis risk** appropriately in the Risk not in VaR (RniV) framework.

### 4.4 Time Series Data Structure

Each time series observation contains:

| Attribute | Type | Description | Mandatory |
|-----------|------|-------------|:---------:|
| `time_series_id` | String | Unique identifier | Yes |
| `risk_factor_id` | String | Link to risk factor definition | Yes |
| `observation_date` | Date | Business date of observation | Yes |
| `observation_value` | Decimal | Observed value (price, rate, spread) | Yes |
| `return_1d` | Decimal | 1-day return (for VaR) | Yes |
| `return_10d` | Decimal | 10-day return (for FRTB liquidity horizons) | No |
| `observation_source` | Enum | External / Internal | Yes |
| `source_system` | String | Bloomberg / Reuters / Internal / etc. | Yes |
| `ipv_status` | Enum | Approved / Exception / NotRequired | Yes |
| `proxy_applied` | Boolean | Whether proxy was used | Yes |
| `proxy_level` | Integer | Proxy level classification (1-4) | Yes |
| `proxy_function` | String | If proxied, which function code | Conditional |
| `proxy_source_rf` | String | If proxied, risk factor ID used as source | Conditional |
| `proxy_source_value` | Decimal | If proxied, the actual source observation value | Conditional |
| `proxy_comment` | String | Audit comment with parameters and approver | Conditional |

### 4.5 Proxy Lineage Field Documentation

When a proxy is applied, the system must capture complete lineage to enable audit trail, impact analysis, and model validation. The following fields document the proxy chain:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        PROXY LINEAGE FIELD SPECIFICATION                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  PROXY_APPLIED (Boolean)                                                                │
│  ─────────────────────────                                                              │
│  • TRUE: Observation derived from proxy function                                        │
│  • FALSE: Observation sourced directly from configured source (Level 1)                 │
│                                                                                         │
│  PROXY_LEVEL (Integer: 1-4)                                                             │
│  ──────────────────────────                                                             │
│  • 1: Actual Data - sourced from primary configured source                              │
│  • 2: Specific Proxy - RFVB or NAR function applied                                     │
│  • 3: Curve/Surface Proxy - LinIntrp, FECS, or FEBS function applied                    │
│  • 4: Generic/Fallback - Generic mapping or Copy Forward applied                        │
│                                                                                         │
│  PROXY_FUNCTION (String)                                                                │
│  ───────────────────────                                                                │
│  Function codes:                                                                        │
│  • "RFVB" - Risk Factor with Variable Basis                                             │
│  • "NAR" - No Arbitrage Return                                                          │
│  • "LinIntrp" - Linear Interpolation                                                    │
│  • "FECS" - Flat Extrapolation on Calendar Spread                                       │
│  • "FEBS" - Flat Extrapolation on Basis Spread                                          │
│  • "Generic" - Generic mapping table proxy                                              │
│  • "CF" - Copy Forward (prior day's value)                                              │
│                                                                                         │
│  PROXY_SOURCE_RF (String)                                                               │
│  ────────────────────────                                                               │
│  • Risk factor ID(s) used as proxy source                                               │
│  • For interpolation: comma-separated list (e.g., "EUR_SWAP_5Y,EUR_SWAP_10Y")           │
│  • For basis proxy: single source ID plus basis source                                  │
│                                                                                         │
│  PROXY_SOURCE_VALUE (Decimal)                                                           │
│  ───────────────────────────                                                            │
│  • The actual observation value from the proxy source risk factor                       │
│  • Enables reconstruction of proxy calculation                                          │
│                                                                                         │
│  PROXY_COMMENT (String)                                                                 │
│  ─────────────────────                                                                  │
│  Format: "<function> applied using <parameters> [<approver>]"                           │
│                                                                                         │
│  Examples:                                                                              │
│  • "RFVB applied using EUR_IG_BBB_5Y + 25bps [J.Smith]"                                 │
│  • "LinIntrp applied using EUR_SWAP_5Y and EUR_SWAP_10Y [M.Jones]"                      │
│  • "CF applied - Prior Days Data Copy Forward [system]"                                 │
│  • "Generic applied using sector mapping table [system]"                                │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 4.5.1 Lineage Use Cases

| Use Case | Required Fields | Purpose |
|----------|-----------------|---------|
| **Audit Trail** | All proxy fields | Regulatory evidence of data derivation |
| **Impact Analysis** | `proxy_source_rf` | Identify downstream impacts when source questioned |
| **Model Validation** | `proxy_source_value`, `observation_value` | Compare proxy vs. actual when available |
| **Proxy Inventory** | `proxy_level`, `proxy_function` | Monthly Proxy & RniV Forum reporting |
| **Data Quality KPIs** | `proxy_level` | Track Level 1 vs. proxied observation rates |

#### 4.5.2 Lineage Retention

| Data Element | Retention Period | Rationale |
|--------------|------------------|-----------|
| Proxy lineage fields | 7 years | Regulatory audit requirement |
| Superseded proxy configurations | 7 years | Historical reconstruction |
| Approval documentation (Jira) | 7 years | Governance evidence |

See [Proxying Process (MR-L4-005f)](./proxying-process.md) for detailed proxy function specifications and approval workflow.

### 4.6 FRTB Modellability

Under FRTB, risk factors must meet **modellability criteria** to use Expected Shortfall calculation:

| Classification | Criteria | Capital Treatment |
|----------------|----------|-------------------|
| **Modellable Risk Factor (MRF)** | ≥24 observable prices in 12 months, no gap >1 month | ES calculation allowed |
| **Non-Modellable Risk Factor (NMRF)** | Fails MRF test | Stressed scenario capital add-on |

Time Series Management must track modellability status for all risk factors and escalate NMRFs to the Proxy & RniV Forum.

---

## 5. Process Timing

> **Note:** The timelines below represent **best-case scenarios** under normal operating conditions. In practice, exceptions such as source failures, unusual market conditions, high exception volumes, or upstream delays may extend processes to the following business day. When this occurs, the escalation procedures in Section 7.2 apply.

### 5.1 Daily Timeline (London Time)

```
TIME SERIES DAILY OPERATIONS
═══════════════════════════════════════════════════════════════════════════════════════

17:00 ─────────────────────────────────────────────────────────────────────────────────
      │
      │  MARKET CLOSE
      │  └── London markets close; final trader marks submitted
      │
17:30 ─────────────────────────────────────────────────────────────────────────────────
      │
      │  EOD MARKET DATA SNAPSHOT
      │  └── MDC captures official EOD prices, curves, surfaces
      │  └── 4-eyes review and approval
      │
18:00 ─────────────────────────────────────────────────────────────────────────────────
      │
      │  IPV PROCESS (Finance/Product Control)
      │  └── Validate internal marks against external benchmarks
      │  └── Approve internal prices for time series use
      │
19:00 ─────────────────────────────────────────────────────────────────────────────────
      │
      │  PRICE COLLECTION BATCH
      │  └── Time Series Service collects from all configured sources
      │  └── External feeds (Bloomberg, Reuters, Exchanges)
      │  └── Internal marks (post-IPV approval)
      │
19:30 ─────────────────────────────────────────────────────────────────────────────────
      │
      │  CLEANING & VALIDATION
      │  └── Automated validation checks (stale, spike, zero)
      │  └── Exceptions placed in queue
      │
20:00 ─────────────────────────────────────────────────────────────────────────────────
      │
      │  EXCEPTION MANAGEMENT
      │  └── RAV team reviews exception queue
      │  └── Validate against alternative sources
      │  └── Apply corrections or confirm observations
      │
21:00 ─────────────────────────────────────────────────────────────────────────────────
      │
      │  TIME SERIES CONSTRUCTION
      │  └── Attach validated observations to risk factors
      │  └── Apply proxies where configured
      │  └── Calculate returns (1-day, 10-day)
      │
22:00 ─────────────────────────────────────────────────────────────────────────────────
      │
      │  PUBLISH TO RISK ENGINE
      │  └── Complete time series available for VaR batch
      │
═══════════════════════════════════════════════════════════════════════════════════════
```

### 5.2 Setup Process Timing (Non-Daily)

| Activity | Trigger | Lead Time | Approval |
|----------|---------|-----------|----------|
| New instrument setup | New trade in instrument not in ODS | T-1 (before trade) | Operations/MDC |
| New risk factor setup | New curve/surface required | 5 business days | RMA + Market Risk |
| New price source config | Risk factor needs source mapping | 2 business days | RAV + Market Risk |
| New proxy configuration | Gap identified in time series | 3-5 business days | Head of RMA + Head of Market Risk |

---

## 6. Data Sources

### 6.1 Source Selection Principles

Time series observations can come from multiple sources. Rather than a rigid hierarchy, Meridian Global Bank applies **judgement-based source selection** considering the following factors:

**Key Factors for Source Selection**

| Factor | Consideration | Example |
|--------|---------------|---------|
| **Liquidity** | Does the source reflect actual tradeable prices? | Exchange prices for liquid futures vs. broker quotes for OTC |
| **Consistency** | Is the source consistent with valuation curves? | Using same FX rate source as front office valuation |
| **Coverage** | Does the source provide complete tenor/strike coverage? | Bloomberg may have full curve; broker only spot |
| **Timeliness** | Is the source available in time for EOD process? | Real-time feeds vs. T+1 batch files |
| **Independence** | Is the source independent from internal marks? | Regulatory preference for external sources |
| **History** | Does the source have sufficient historical depth? | New source may lack 500+ day history |

**Available Source Types**

| Source Type | Characteristics | Typical Use Cases |
|-------------|-----------------|-------------------|
| **Exchange** | Official closing prices; highest independence | Equities, listed futures, options |
| **Bloomberg** | Broad coverage; real-time; industry standard | FX, rates, credit indices |
| **Markit** | Specialist in credit; consensus pricing | CDS spreads, credit indices |
| **Reuters** | Alternative to Bloomberg; validation source | Cross-validation, gap filling |
| **Brokers** | OTC market expertise; less transparency | Illiquid OTC, emerging markets |
| **Internal Marks** | Full coverage; requires IPV validation | Illiquid/bespoke instruments, market-maker curves |

**Source Selection Governance**

- **Initial source selection** is proposed by Market Risk and approved by RMA
- **Changes to source** require analysis justification and RMA approval (see Ad-Hoc Processes in Section 3.1)
- **Internal marks** require IPV approval before use in time series
- **Audit trail** must document the rationale for source selection per risk factor

### 6.2 Internal Prices - When to Use

Internal prices (trader marks) may be used as time series observations when:

| Scenario | Justification | IPV Requirement |
|----------|---------------|-----------------|
| **Market Maker** | Bank has superior liquidity view from bid/offer activity | IPV validates vs broker consensus |
| **Illiquid OTC** | No reliable external source exists | IPV approves model-based pricing |
| **Bespoke Structures** | Externally unobservable | IPV validates model reasonableness |
| **Emerging Markets** | Limited external provider coverage | IPV validates vs available benchmarks |

---

## 7. Controls Framework

### 7.1 Key Controls

| Control ID | Control | Type | Frequency | Owner |
|------------|---------|------|-----------|-------|
| TS-C01 | Risk factor must exist before time series collection | Preventive | On setup | RMA |
| TS-C02 | Source configuration enforced in collection | Preventive | Daily | RAV |
| TS-C03 | Stale data check (observation age > threshold) | Detective | Daily | RAV |
| TS-C04 | Spike detection (move > 3σ flagged) | Detective | Daily | RAV |
| TS-C05 | Zero/negative value rejection | Detective | Daily | RAV |
| TS-C06 | Cross-source validation (variance check) | Detective | Daily | RAV |
| TS-C07 | 4-eyes review of exceptions | Detective | Daily | RAV + Market Risk |
| TS-C08 | Proxy requires joint approval | Preventive | On setup | Head of RMA + Head of MR |
| TS-C09 | Modellability tracking (FRTB MRF/NMRF) | Detective | Monthly | RMA |
| TS-C10 | Time series completeness check before VaR | Detective | Daily | Risk Engine Ops |

**Configurable Control Parameters**

Certain control thresholds are configurable and subject to periodic review:

| Parameter | Current Setting | Governance |
|-----------|----------------|------------|
| **Stale data threshold** | 2 business days | Reviewed and approved annually by Model Forum; may vary by asset class |
| **Spike detection sigma** | 3σ | Approved by RMA; calibrated against backtesting results |
| **Cross-source variance** | 5% relative | Approved by RMA; tighter for liquid markets |

Changes to control parameters require:
1. Analysis demonstrating impact on data quality and VaR accuracy
2. Approval by the Model Forum (for parameters affecting model performance)
3. Documentation in the control parameter register

### 7.2 Exception Escalation

| Exception Type | Severity | Response | Escalation |
|----------------|----------|----------|------------|
| Missing observation (single day) | Low | Apply previous day + flag | RAV team |
| Missing observation (multiple days) | Medium | Investigate source; may need proxy | RAV → Market Risk |
| Spike >5σ | Medium | Validate against alternatives | RAV → Market Risk |
| Systematic source failure | High | Switch to backup source; notify | RAV → IT → MLRC |
| Risk factor not modellable (FRTB) | High | Document rationale; capital add-on | RMA → Proxy & RniV Forum |

---

## 8. Key Performance Indicators

| KPI | Target | Threshold | Frequency |
|-----|--------|-----------|-----------|
| Time series completeness (% risk factors with observation) | 99.5% | 99.0% | Daily |
| Exception queue cleared by 21:00 | 100% | 95% | Daily |
| Stale data rate (observations >1 day old) | <0.5% | <1.0% | Daily |
| Proxy coverage (% gaps filled) | 100% | 98% | Monthly |
| Modellable risk factor ratio | >95% | >90% | Monthly |
| Time series published by 22:00 | 100% | 98% | Daily |

---

## 9. Technology Architecture

### 9.1 System Landscape

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                         TIME SERIES SYSTEM ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  EXTERNAL SOURCES                 INTERNAL SOURCES                                      │
│  ┌─────────┐ ┌─────────┐         ┌─────────────────┐                                    │
│  │Bloomberg│ │ Reuters │         │  EOD Market     │                                    │
│  │ API     │ │ Eikon   │         │  Data Snapshot  │                                    │
│  └────┬────┘ └────┬────┘         │  (post-IPV)     │                                    │
│       │           │              └────────┬────────┘                                    │
│  ┌────┴────┐ ┌────┴────┐                  │                                             │
│  │ Markit  │ │Exchanges│                  │                                             │
│  │ API     │ │ Feeds   │                  │                                             │
│  └────┬────┘ └────┬────┘                  │                                             │
│       │           │                       │                                             │
│       └─────┬─────┴───────────────────────┘                                             │
│             │                                                                           │
│             ▼                                                                           │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │                        TIME SERIES SERVICE                                       │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │   │
│  │  │   COLLECTOR  │─▶│   CLEANER    │─▶│  VALIDATOR   │─▶│  CONSTRUCTOR │          │   │
│  │  │              │  │              │  │              │  │              │          │   │
│  │  │ Source       │  │ Stale check  │  │ Cross-source │  │ Attach to RF │          │   │
│  │  │prioritisation│  │ Spike detect │  │ validation   │  │ Apply proxies│          │   │
│  │  │ Collection   │  │ Zero reject  │  │ Exception Q  │  │ Calc returns │          │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘          │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│             │                                                                           │
│             ▼                                                                           │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │                     DATA LAKEHOUSE (Apache Iceberg)                              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                            │   │
│  │  │ INSTRUMENT   │  │ RISK FACTOR  │  │ TIME SERIES  │                            │   │
│  │  │ ODS          │  │ DEFINITIONS  │  │ ODS          │                            │   │
│  │  │              │  │              │  │              │                            │   │
│  │  │ Security     │  │ Curves,      │  │ Daily obs,   │                            │   │
│  │  │ master       │  │ surfaces,    │  │ returns,     │                            │   │
│  │  │              │  │ mappings     │  │ lineage      │                            │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                            │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│             │                                                                           │
│             ▼                                                                           │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐   │
│  │                           RISK ENGINE                                            │   │
│  │                                                                                  │   │
│  │   Consumes complete time series for VaR, SVaR, stress testing                    │   │
│  │                                                                                  │   │
│  └──────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 System Inventory

| System | Node ID | Purpose | Owner |
|--------|---------|---------|-------|
| **Instrument ODS** | SYS-MR-009 | Security static data golden source | Operations |
| **Time Series Service** | SYS-MR-010 | Collection, cleaning, construction | Risk Technology |
| **Market Data ODS** | SYS-MR-006 | Curves, prices, risk factor definitions | MDC |
| **Time Series ODS** | SYS-MR-011 | Historical observations storage | Risk Technology |
| **Proxy Tracking Tool** | SYS-MR-012 | Jira-based proxy workflow | RMA |

---

## 10. Related Documents

### 10.1 Sub-Process Documents

| Document | Process ID | Purpose |
|----------|------------|---------|
| [Instrument Setup](./instrument-setup.md) | MR-L4-005a | Security static data management |
| [Risk Factor Setup](./risk-factor-setup.md) | MR-L4-005b | Curve/surface/rate configuration |
| [Price Collection](./price-collection.md) | MR-L4-005c | Daily observation collection |
| [Cleaning & Validation](./cleaning-validation.md) | MR-L4-005d | Data quality and exception management |
| [Curve Stripping](./curve-stripping.md) | MR-L4-005e | Par to zero rate conversion; XCCY curve construction |
| [Proxying Process](./proxying-process.md) | MR-L4-005f | Gap filling methodology |

### 10.2 Related Processes

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](../market-risk-process-orchestration.md) | Parent orchestration process |
| [EOD Market Data Snapshot](../eod-market-data-snapshot.md) | Upstream - provides EOD prices |
| [Regional EOD Management](../regional-eod-management.md) | Addresses regional snapshot differences |
| [Risk Engine Calculation](../risk-engine-calculation.md) | Downstream - consumes time series |

### 10.3 Governance Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Policy](../../L3-Governance/policies/market-risk-policy.md) | Parent policy |
| [MLRC Terms of Reference](../../L3-Governance/committees/mlrc-terms-of-reference.md) | Escalation authority |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |
| 1.1 | 2025-01-16 | Enhanced Section 4.4 (added proxy_level, proxy_comment fields); added Section 4.5 Proxy Lineage Field Documentation with detailed field specifications | RMA |

### 11.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full Review | Annual | January 2026 |
| Sub-Process Review | Semi-annual | July 2025 |
| KPI Review | Monthly | Ongoing |

---

*End of Document*
