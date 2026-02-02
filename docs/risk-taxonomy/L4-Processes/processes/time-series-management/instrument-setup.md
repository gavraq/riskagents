---
# Process Metadata
process_id: MR-L4-005a
process_name: Instrument Setup
version: 1.0
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Operations / Market Data Control
approving_committee: Operations Committee

# Taxonomy Linkages
parent_process: MR-L4-005  # Time Series Management
l1_requirements:
  - REQ-L1-022  # BCBS 239 - Data Governance
l2_risk_types:
  - MR-L2-001   # Market Risk
l7_systems:
  - SYS-MR-009  # Instrument ODS
---

# Instrument Setup Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-005a |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Time Series Management (MR-L4-005) |
| **Owner** | Head of Operations / Market Data Control |

---

## 1. Purpose

The Instrument Setup process ensures that all tradeable securities have accurate, complete static data in the **Instrument ODS** (Operational Data Store) before trading commences. This data serves as the **golden source** for instrument reference data across Meridian Global Bank, including for time series management.

---

## 2. Scope

### 2.1 In Scope

| Instrument Type | Examples | Key Static Data |
|-----------------|----------|-----------------|
| **Equities** | Listed stocks, ADRs, ETFs | ISIN, ticker, exchange, currency, sector |
| **Fixed Income** | Government bonds, corporate bonds | ISIN, issuer, coupon, maturity, day count |
| **FX** | Spot, forwards, NDFs | Currency pair, settlement convention |
| **Derivatives** | Futures, options, swaps | Underlying, expiry, strike, contract size |
| **Credit** | CDS, credit indices | Reference entity, RED code, maturity |
| **Commodities** | Physical, futures | Commodity type, delivery location, grade |

### 2.2 Out of Scope

- OTC bespoke structures (handled via Trade Capture with embedded terms)
- Risk factor definitions (see MR-L4-005b Risk Factor Setup)
- Price/rate data (see MR-L4-005c Price Collection)

---

## 3. Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           INSTRUMENT SETUP PROCESS                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐
  │ 1. TRIGGER      │
  │                 │
  │ • New instrument│
  │   identified    │
  │ • Static data   │
  │   change        │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ 2. SOURCE       │
  │   IDENTIFICATION│
  │                 │
  │ • Check primary │
  │   sources       │
  │ • Bloomberg,    │
  │   Reuters, etc. │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ 3. DATA         │
  │    EXTRACTION   │
  │                 │
  │ • Pull static   │
  │   data fields   │
  │ • Validate      │
  │   completeness  │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ 4. VALIDATION   │
  │                 │
  │ • Cross-source  │
  │   validation    │
  │ • Business rule │
  │   checks        │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐         ┌─────────────────┐
  │ 5. EXCEPTION?   │── Yes ──│ 6. EXCEPTION    │
  │                 │         │    RESOLUTION   │
  │ • Conflicts?    │         │                 │
  │ • Missing data? │         │ • Manual review │
  └────────┬────────┘         │ • Source query  │
           │                  └────────┬────────┘
           │ No                        │
           ▼                           │
  ┌─────────────────┐                  │
  │ 7. LOAD TO ODS  │◀─────────────────┘
  │                 │
  │ • Insert/update │
  │ • Audit trail   │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ 8. PUBLISH      │
  │                 │
  │ • Notify        │
  │   downstream    │
  │ • Available for │
  │   trading       │
  └─────────────────┘
```

---

## 4. Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| **Operations (Instrument Data Team)** | Day-to-day instrument setup; validation; exception resolution |
| **Market Data Control (MDC)** | Curve/surface instrument definitions; price source configuration |
| **Trading Desk** | Request new instruments; validate trading attributes |
| **Risk Technology** | System maintenance; data quality monitoring |
| **RAV** | Consumer - uses instrument data for risk factor mapping |

---

## 5. Data Specification

### 5.1 Core Static Data Fields

| Field | Description | Mandatory | Source Priority |
|-------|-------------|:---------:|-----------------|
| `instrument_id` | Internal unique identifier | Yes | Generated |
| `isin` | International Securities ID | Conditional | Bloomberg → Reuters → Manual |
| `cusip` | US securities identifier | Conditional | Bloomberg |
| `sedol` | UK securities identifier | Conditional | Bloomberg |
| `ticker` | Trading symbol | Yes | Exchange feed |
| `instrument_name` | Full legal name | Yes | Bloomberg |
| `instrument_type` | Asset class (Equity, Bond, etc.) | Yes | Internal taxonomy |
| `issuer_id` | Link to issuer master | Yes | Internal mapping |
| `currency` | Denomination currency | Yes | Bloomberg |
| `exchange_code` | Primary listing exchange | Conditional | Bloomberg |
| `country_of_risk` | Risk country (may differ from listing) | Yes | Bloomberg + Risk override |
| `sector` | GICS/ICB sector classification | Conditional | Bloomberg |
| `maturity_date` | For dated instruments | Conditional | Bloomberg |
| `coupon_rate` | For fixed income | Conditional | Bloomberg |
| `day_count_convention` | Accrual basis (ACT/360, etc.) | Conditional | Bloomberg |
| `payment_frequency` | Coupon frequency | Conditional | Bloomberg |
| `status` | Active / Matured / Suspended | Yes | Exchange + Internal |

### 5.2 Asset-Class Specific Fields

**Fixed Income Additional Fields:**
- Issue date, first coupon date, settlement convention
- Call/put schedules, sinking fund provisions
- Benchmark spread index

**Equity Additional Fields:**
- Share class, voting rights, dividend policy
- Corporate action flags

**Derivative Additional Fields:**
- Underlying instrument ID, contract size
- Expiry date, strike price, option type
- Delivery/settlement type

---

## 6. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| IS-C01 | ISIN must be unique in ODS | Preventive | Operations |
| IS-C02 | Mandatory fields complete before trading | Preventive | Operations |
| IS-C03 | Cross-source validation (Bloomberg vs. Reuters) | Detective | Operations |
| IS-C04 | Corporate action flags reviewed daily | Detective | Operations |
| IS-C05 | Matured instruments flagged automatically | Detective | System |
| IS-C06 | 4-eyes review for manual data entry | Preventive | Operations |

---

## 7. Service Levels

| Metric | Target | Escalation |
|--------|--------|------------|
| New listed instrument setup | Same day as listing | Operations Manager |
| New OTC instrument setup | T-1 (day before trade) | Operations Manager |
| Static data correction | 2 hours | Operations Team Lead |
| Exception resolution | 4 hours | Operations Manager |

---

## 8. Integration Points

### 8.1 Upstream Systems

| System | Data Provided | Frequency |
|--------|---------------|-----------|
| Bloomberg | Primary static data feed | Real-time + EOD batch |
| Reuters | Secondary/validation source | Real-time |
| Exchanges | Official listings, corporate actions | Real-time |

### 8.2 Downstream Consumers

| System | Data Consumed | Purpose |
|--------|---------------|---------|
| **Trading Systems** | Instrument master | Trade booking |
| **Risk Engine** | Instrument attributes | Risk factor mapping |
| **Time Series Service** | Instrument-to-risk-factor mapping | Price collection |
| **Finance Systems** | Instrument master | P&L, accounting |

---

## 9. Exception Handling

| Exception Type | Resolution Path |
|----------------|-----------------|
| **Missing ISIN** | Query issuer/exchange; assign temporary ID if unavailable |
| **Conflicting data between sources** | Escalate to MDC for judgement call; document decision |
| **New instrument type not in taxonomy** | Escalate to RMA to extend taxonomy |
| **Corporate action ambiguity** | Trading desk confirmation required |

---

## 10. Related Documents

| Document | Relationship |
|----------|--------------|
| [Time Series Management](./time-series-overview.md) | Parent process |
| [Risk Factor Setup](./risk-factor-setup.md) | Downstream - links instruments to risk factors |
| [Price Collection](./price-collection.md) | Uses instrument definitions |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | Operations Committee |

---

*End of Document*
