---
# Process Metadata
process_id: MR-L4-005b
process_name: Risk Factor Setup
version: 1.0
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Market Risk (requirements) / Head of RAV (system)
approving_committee: MLRC

# Taxonomy Linkages
parent_process: MR-L4-005  # Time Series Management
l1_requirements:
  - REQ-L1-001  # CRR
  - REQ-L1-003  # FRTB
l2_risk_types:
  - MR-L2-001   # Market Risk
l3_governance:
  - MR-L3-001   # Market Risk Policy
l7_systems:
  - SYS-MR-006  # Market Data ODS
  - SYS-MR-010  # Time Series Service
---

# Risk Factor Setup Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-005b |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Time Series Management (MR-L4-005) |
| **Owner** | Head of Market Risk (requirements) / Head of RAV (system) |

---

## 1. Purpose

The Risk Factor Setup process ensures that all market risk factors required for VaR, Stressed VaR, and stress testing are properly defined, configured with appropriate price sources, and ready for time series collection. This process bridges the gap between **what the Bank trades** (instruments) and **how risk is measured** (risk factors).

---

## 2. Scope

### 2.1 Risk Factor Types

| Risk Factor Type | Description | Examples |
|------------------|-------------|----------|
| **Interest Rate Curves** | Yield curves for discounting and projection | EUR OIS, USD SOFR, GBP SONIA |
| **Credit Spread Curves** | Issuer or bucket-level credit spreads | Corporate IG/HY by rating, sovereign curves |
| **FX Rates** | Spot exchange rates | EUR/USD, USD/JPY, GBP/USD |
| **FX Forward Points** | Tenor-based forward differentials | EUR/USD 1M, 3M, 6M, 1Y points |
| **Equity Prices** | Individual stock and index levels | AAPL, FTSE 100, S&P 500 |
| **Volatility Surfaces** | Option-implied volatilities | EUR swaption vol, FX vol smiles |
| **Commodity Prices** | Spot and forward commodity prices | Brent crude, Gold spot |
| **Basis Curves** | OIS vs IBOR, XCCY basis | EUR 3M EURIBOR vs OIS |
| **Inflation Curves** | Real rate and breakeven curves | UK RPI, EUR HICP |

### 2.2 Ownership Model

| Activity | Owner | Approver |
|----------|-------|----------|
| **Define risk factor requirements** | Market Risk | RMA |
| **Configure risk factor in system** | RAV | Market Risk (validation) |
| **Assign price sources** | RAV | RMA |
| **Approve new risk factors for VaR** | RMA | MLRC (material changes) |

---

## 3. Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           RISK FACTOR SETUP PROCESS                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                              1. TRIGGER                                                  │
│  • New trading activity requiring unmapped risk factors                                  │
│  • New curve/surface requested by Trading or Market Risk                                 │
│  • Regulatory change requiring additional risk factor granularity (e.g., FRTB)           │
│  • Source change request from Market Risk                                                │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     2. REQUIREMENTS DEFINITION (Market Risk)                             │
│                                                                                          │
│  • Define risk factor name and type (curve, surface, spot)                               │
│  • Specify required tenors/strikes/dimensions                                            │
│  • Identify relationship to valuation models                                             │
│  • Determine required history depth (500 days + stressed period)                         │
│  • Submit request via Jira workflow                                                      │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                       3. SOURCE SELECTION (RAV + Market Risk)                            │
│                                                                                          │
│  • Evaluate available sources against selection factors (see Overview 6.1)               │
│  • Assess history availability and coverage                                              │
│  • Document source selection rationale                                                   │
│  • If internal marks needed, initiate IPV coordination                                   │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                       4. SYSTEM CONFIGURATION (RAV)                                      │
│                                                                                          │
│  • Create risk factor definition in Market Data ODS                                      │
│  • Configure source mapping and priority                                                 │
│  • Set up curve construction parameters (interpolation, extrapolation)                   │
│  • Link to instrument(s) in Instrument ODS                                               │
│  • Configure any required curve stripping parameters                                     │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                       5. HISTORY POPULATION                                              │
│                                                                                          │
│  • Backfill historical observations (minimum 500 days)                                   │
│  • For new curves with no history: identify proxy requirements                           │
│  • Validate historical data quality                                                      │
│  • Calculate returns and validate reasonableness                                         │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                       6. APPROVAL (RMA)                                                  │
│                                                                                          │
│  • Review risk factor specification                                                      │
│  • Validate source selection                                                             │
│  • Confirm alignment with valuation models                                               │
│  • Approve for production use                                                            │
│  • Material changes escalated to MLRC                                                    │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                       7. ACTIVATION                                                      │
│                                                                                          │
│  • Risk factor marked as "Active" in system                                              │
│  • Included in daily price collection                                                    │
│  • Available for VaR calculation                                                         │
│  • Notify Market Risk of go-live                                                         │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Risk Factor Taxonomy

Meridian Global Bank maintains an **FRTB-aligned risk factor taxonomy** to ensure regulatory compliance and consistent risk measurement:

### 4.1 GIRR - General Interest Rate Risk

```
GIRR Risk Factors
│
├── Discounting Curves (OIS)
│   ├── EUR_OIS (tenors: ON, 1W, 1M, 3M, 6M, 1Y, 2Y, 5Y, 10Y, 15Y, 20Y, 30Y)
│   ├── USD_OIS
│   ├── GBP_OIS
│   └── [Other currencies...]
│
├── Projection Curves (IBOR/RFR)
│   ├── EUR_EURIBOR_3M
│   ├── EUR_EURIBOR_6M
│   ├── USD_SOFR
│   ├── GBP_SONIA
│   └── [Other rates...]
│
├── Basis Curves
│   ├── EUR_OIS_vs_3M
│   ├── EUR_3M_vs_6M
│   └── [Other basis...]
│
└── Inflation Curves
    ├── EUR_HICP
    ├── GBP_RPI
    └── USD_CPI
```

### 4.2 CSR - Credit Spread Risk

```
CSR Risk Factors
│
├── Sovereign Curves (by issuer)
│   ├── DE_GOVT (Germany)
│   ├── FR_GOVT (France)
│   ├── US_GOVT (USA)
│   └── [Other sovereigns...]
│
├── Corporate Curves (by rating bucket)
│   ├── EUR_IG_AAA
│   ├── EUR_IG_AA
│   ├── EUR_IG_A
│   ├── EUR_IG_BBB
│   ├── EUR_HY
│   └── [Other buckets/currencies...]
│
└── Credit Indices
    ├── ITRAXX_MAIN
    ├── ITRAXX_XOVER
    ├── CDX_IG
    └── CDX_HY
```

### 4.3 FX Risk

```
FX Risk Factors
│
├── Spot Rates (vs USD base)
│   ├── EUR/USD
│   ├── GBP/USD
│   ├── USD/JPY
│   └── [Other pairs...]
│
└── Forward Points (by tenor)
    ├── EUR/USD (1M, 3M, 6M, 9M, 1Y, 2Y, 3Y, 5Y)
    └── [Other pairs...]
```

### 4.4 Equity Risk

```
Equity Risk Factors
│
├── Spot Prices (linked to Instrument ODS)
│   └── [Individual equities by ISIN]
│
├── Index Levels
│   ├── SPX (S&P 500)
│   ├── SX5E (Euro Stoxx 50)
│   ├── UKX (FTSE 100)
│   └── [Other indices...]
│
├── Dividend Curves
│   └── [By index/stock...]
│
└── Repo Rates
    └── [By issuer/bucket...]
```

### 4.5 Volatility Risk

```
Volatility Risk Factors
│
├── IR Swaption Surfaces (expiry × tenor × strike)
│   ├── EUR_SWAPTION_VOL
│   ├── USD_SWAPTION_VOL
│   └── [Other currencies...]
│
├── FX Volatility Surfaces (expiry × delta)
│   ├── EURUSD_VOL
│   ├── USDJPY_VOL
│   └── [Other pairs...]
│
├── Equity Volatility Surfaces (expiry × strike)
│   ├── SPX_VOL
│   ├── SX5E_VOL
│   └── [Other indices/stocks...]
│
└── Credit Volatility
    └── [Index vol by expiry...]
```

---

## 5. Risk Factor Definition Specification

### 5.1 Core Fields

| Field | Description | Mandatory |
|-------|-------------|:---------:|
| `risk_factor_id` | Unique identifier | Yes |
| `risk_factor_name` | Descriptive name | Yes |
| `risk_class` | FRTB class (GIRR, CSR, Equity, FX, Commodity) | Yes |
| `risk_type` | Specific type (Curve, Surface, Spot, Spread) | Yes |
| `currency` | Denomination currency | Yes |
| `geography` | Country/region classification | Yes |
| `dimensions` | Tenor, strike, expiry grids | Conditional |
| `status` | Active / Inactive / Pending | Yes |
| `modellability` | MRF / NMRF (FRTB classification) | Yes |

### 5.2 Source Configuration Fields

| Field | Description | Mandatory |
|-------|-------------|:---------:|
| `primary_source` | Main price source | Yes |
| `backup_source` | Fallback source | No |
| `source_ticker` | Vendor-specific identifier | Yes |
| `collection_time` | EOD snapshot time | Yes |
| `interpolation_method` | Linear, cubic spline, etc. | Conditional |
| `extrapolation_method` | Flat, log-linear, etc. | Conditional |

### 5.3 Valuation Link Fields

| Field | Description | Mandatory |
|-------|-------------|:---------:|
| `valuation_curve_id` | Link to front office curve | Yes |
| `consistency_check` | Validation against valuation | Yes |
| `basis_risk_flag` | If differs from valuation curve | No |

---

## 6. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| RF-C01 | Risk factor must have approved source before collection | Preventive | RMA |
| RF-C02 | New risk factor requires minimum 500 days history (or proxy) | Preventive | RAV |
| RF-C03 | Risk factor must be linked to valuation curve | Preventive | RMA |
| RF-C04 | NMRF status triggers escalation to Proxy & RniV Forum | Detective | RMA |
| RF-C05 | Source changes require re-approval | Preventive | RMA |
| RF-C06 | Annual review of inactive risk factors | Detective | Market Risk |

---

## 7. Service Levels

| Activity | Target | Escalation |
|----------|--------|------------|
| New risk factor setup (with history) | 5 business days | Head of RAV |
| New risk factor setup (proxy required) | 10 business days | Head of RMA |
| Source change implementation | 2 business days | RAV Manager |
| Urgent risk factor (regulatory) | 24 hours | MLRC |

---

## 8. Ad-Hoc Processes

### 8.1 Source Change Request

Market Risk may request a change to the price source for an existing risk factor:

1. **Request**: Market Risk submits Jira with rationale and supporting analysis
2. **Impact Assessment**: RAV assesses historical data availability and continuity
3. **Analysis**: Market Risk provides comparison (correlation, tracking error) between old and new source
4. **Approval**: RMA reviews and approves
5. **Implementation**: RAV updates source configuration
6. **Validation**: Post-change monitoring for 5 business days

### 8.2 Risk Factor Reconciliation

Periodic reconciliation ensures alignment between:
- **ODS risk factors** (what time series tracks)
- **Trading system risk factors** (what valuations use)

| Check | Frequency | Owner |
|-------|-----------|-------|
| Risk factor count reconciliation | Weekly | RAV |
| Tenor/strike grid alignment | Monthly | Market Risk |
| Unmapped trade review | Daily | Market Risk |

---

## 9. Related Documents

| Document | Relationship |
|----------|--------------|
| [Time Series Management](./time-series-overview.md) | Parent process |
| [Instrument Setup](./instrument-setup.md) | Upstream - provides instrument data |
| [Price Collection](./price-collection.md) | Downstream - collects prices for risk factors |
| [Curve Stripping](./curve-stripping.md) | Downstream - processes par rates to zeros |
| [Proxying Process](./proxying-process.md) | Related - handles gaps in history |

---

## 10. Document Control

### 10.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |

---

*End of Document*
