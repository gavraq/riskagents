---
# Process Metadata
process_id: MR-L4-003
process_name: EOD Market Data Snapshot
version: 1.0
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Market Data Control (MDC)
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
  - SYS-MR-006  # Market Data ODS
  - SYS-MR-004  # Trading Systems (Murex)
---

# EOD Market Data Snapshot Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | MR-L4-003 |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Parent Process** | Market Risk Process Orchestration (MR-L4-001) |
| **Owner** | Head of Market Data Control (MDC) |

---

## 1. Purpose

The EOD Market Data Snapshot process captures the **official end-of-day prices, rates, and curves** used for:

- Mark-to-Market (MTM) valuations
- Daily P&L calculation
- Time Series construction for VaR (if internal prices selected)
- Regulatory reporting

This process implements Meridian Global Bank's **"One Curve, One Price"** principle - ensuring a single authoritative market data set is used consistently across the Bank for a given business date.

---

## 2. Scope

### 2.1 Data Types Captured

| Data Type | Description | Primary Source |
|-----------|-------------|----------------|
| **Interest Rate Curves** | OIS, IBOR, projection curves | MDC-built curves |
| **FX Rates** | Spot rates, forward points | FX Trading Desk |
| **Credit Spreads** | CDS, bond spreads, indices | Credit Trading / Markit |
| **Equity Prices** | Stocks, indices | Exchange closing prices |
| **Commodity Prices** | Spot, futures | Commodity Trading / Exchange |
| **Volatility Surfaces** | IR, FX, Equity, Credit vol | Trading Desks / Bloomberg |
| **Internal Marks** | Illiquid/bespoke instruments | Trading Desks (post-IPV) |

### 2.2 Regional Scope

The EOD Market Data Snapshot operates globally with regional coordination:

| Region | Snapshot Time | Responsibility | Purpose |
|--------|---------------|----------------|---------|
| **Asia (HK)** | 17:30 HKT | Asia MDC | Regional valuation; feeds global |
| **EMEA (London - HQ)** | 17:30 GMT | Global MDC | **Primary global snapshot** |
| **Americas (NY)** | 17:30 EST | Americas MDC | Regional valuation; feeds global |

The **London snapshot** serves as the official global EOD for VaR and regulatory reporting.

---

## 3. Process Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        EOD MARKET DATA SNAPSHOT PROCESS                                 │
│                        (Daily - London Time)                                            │
└─────────────────────────────────────────────────────────────────────────────────────────┘

15:00 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 PRE-CLOSE PREPARATION                                   │
          │  │                                                                         │
          │  │  • Confirm Asia EOD snapshot received and validated                     │
          │  │  • Review market conditions / known issues                              │
          │  │  • Alert trading desks to mark submission deadline                      │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
16:30 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 TRADER MARK SUBMISSION                                  │
          │  │                                                                         │
          │  │  • Trading desks submit final marks for illiquid instruments            │
          │  │  • FX desk confirms official spot rates                                 │
          │  │  • IR desk confirms official curve levels                               │
          │  │  • Commodity desk confirms official prices                              │
          │  │                                                                         │
          │  │  Deadline: 17:00 GMT                                                    │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
17:00 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 MARKET CLOSE                                            │
          │  │                                                                         │
          │  │  • London markets officially closed                                     │
          │  │  • No further mark changes accepted (except corrections)                │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
17:15 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 CURVE BUILDING                                          │
          │  │                                                                         │
          │  │  MDC builds official EOD curves:                                        │
          │  │  • OIS Curves (EUR, USD, GBP, JPY, etc.)                                │
          │  │  • Projection Curves (SOFR, EURIBOR, SONIA)                             │
          │  │  • Basis Curves                                                         │
          │  │  • Inflation Curves                                                     │
          │  │  • Credit Curves                                                        │
          │  │                                                                         │
          │  │  Using approved inputs from trading desks and external sources          │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
17:30 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 4-EYES REVIEW                                           │
          │  │                                                                         │
          │  │  ┌────────────────────────────────────────────────────────────────────┐ │
          │  │  │  MDC VALIDATION CHECKLIST                                          │ │
          │  │  │                                                                    │ │
          │  │  │  □ All major curves built successfully                             │ │
          │  │  │  □ Curve levels reasonable vs. previous day                        │ │
          │  │  │  □ FX rates aligned with market close                              │ │
          │  │  │  □ Volatility surfaces complete                                    │ │
          │  │  │  □ No unexplained spikes or anomalies                              │ │
          │  │  │  □ All required inputs received                                    │ │
          │  │  │                                                                    │ │
          │  │  │  Reviewer 1: ____________  Reviewer 2: ____________                │ │
          │  │  └────────────────────────────────────────────────────────────────────┘ │
          │  │                                                                         │
          │  │  If issues found → escalate to MDC Manager                              │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
18:00 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 IPV COORDINATION                                        │
          │  │                                                                         │
          │  │  Finance/Product Control validates internal marks:                      │
          │  │  • Compare trader marks vs. external benchmarks                         │
          │  │  • Review model-based prices for reasonableness                         │
          │  │  • Approve or challenge marks                                           │
          │  │                                                                         │
          │  │  IPV-approved marks flagged for time series use                         │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
18:30 GMT ───────────────────────────────────────────────────────────────────────────────
          │
          │  ┌─────────────────────────────────────────────────────────────────────────┐
          │  │                 SNAPSHOT PUBLICATION                                    │
          │  │                                                                         │
          │  │  Official EOD snapshot published to:                                    │
          │  │  • Market Data ODS (for valuation)                                      │
          │  │  • Time Series Service (for VaR)                                        │
          │  │  • Finance Systems (for P&L)                                            │
          │  │                                                                         │
          │  │  Snapshot ID: SNAP-YYYYMMDD-LONDON                                      │
          │  │  Status: OFFICIAL                                                       │
          │  └─────────────────────────────────────────────────────────────────────────┘
          │
          ▼
    [To Time Series Price Collection / Valuation Engine / P&L Process]
```

---

## 4. The "One Curve, One Price" Principle

### 4.1 Principle Statement

> **For each risk factor, there is ONE authoritative price/rate used consistently across the Bank for a given business date.**

### 4.2 Implementation

| Risk Factor Type | Price Setter | Rationale |
|------------------|--------------|-----------|
| **FX Spot** | FX Trading Desk | Market-maker with best liquidity view |
| **Interest Rate Curves** | MDC (built from desk inputs) | Consistent curve construction methodology |
| **Credit Spreads** | Credit Trading / External | Market expertise; external validation |
| **Equity Prices** | Exchange | Official closing prices |
| **Commodity Prices** | Commodity Desk / Exchange | Market expertise; exchange validation |
| **Volatility** | Options Desks | Implied vol specialists |
| **Illiquid Instruments** | Trading Desk (post-IPV) | Desk expertise with independent validation |

### 4.3 Conflict Resolution

When different desks have conflicting views on a price:

1. **MDC mediates** the discussion
2. **Desk with primary trading responsibility** has preference
3. **IPV challenge** escalates to Product Control Head
4. **Final authority**: CFO (for material disputes)

---

## 5. Curve Building Process

### 5.1 Curve Construction Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           CURVE BUILDING WORKFLOW                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│   INPUTS                              PROCESS                           OUTPUT          │
│   ┌────────────────┐                                                ┌────────────────┐  │
│   │ Deposit Rates  │─┐                                              │ OIS Zero Curve │  │
│   └────────────────┘ │                                              └────────────────┘  │
│   ┌────────────────┐ │      ┌─────────────────────────────┐         ┌────────────────┐  │
│   │ Swap Rates     │─┼─────▶│   MDC CURVE BUILDING        │────────▶│ Projection     │  │
│   └────────────────┘ │      │   (Front Office Systems)    │         │ Curves         │  │
│   ┌────────────────┐ │      │                             │         └────────────────┘  │
│   │ Futures Prices │─┤      │   • Bootstrap methodology   │         ┌────────────────┐  │
│   └────────────────┘ │      │   • Interpolation applied   │         │ Basis Curves   │  │
│   ┌────────────────┐ │      │   • Consistency checks      │         └────────────────┘  │
│   │ FX Forwards    │─┘      └─────────────────────────────┘         ┌────────────────┐  │
│   └────────────────┘                                                │ XCCY Curves    │  │
│                                                                     └────────────────┘  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Curve Inventory

| Curve Category | Key Curves | Update Frequency |
|----------------|------------|------------------|
| **OIS Discounting** | EUR_OIS, USD_OIS, GBP_OIS, JPY_OIS | Daily |
| **IBOR/RFR Projection** | EURIBOR_3M, EURIBOR_6M, SOFR, SONIA | Daily |
| **Basis Curves** | EUR_3M_vs_6M, EUR_OIS_vs_3M | Daily |
| **Government Curves** | EUR_GOVT, USD_GOVT, GBP_GOVT | Daily |
| **Credit Index Curves** | ITRAXX_MAIN, CDX_IG | Daily |

---

## 6. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| EOD-C01 | All major curves must be built before snapshot | Preventive | MDC |
| EOD-C02 | 4-eyes review of snapshot before publication | Preventive | MDC |
| EOD-C03 | Trader marks submitted by deadline | Preventive | Trading Desks |
| EOD-C04 | IPV approval for internal marks | Preventive | Product Control |
| EOD-C05 | Snapshot published by 18:30 GMT | Preventive | MDC |
| EOD-C06 | Curve level reasonableness check (vs. T-1) | Detective | MDC |
| EOD-C07 | Cross-source validation for external prices | Detective | MDC |

---

## 7. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| Trader marks received | 17:00 GMT | 17:15 GMT | Desk Head |
| Curve building complete | 17:30 GMT | 17:45 GMT | MDC Manager |
| 4-eyes review complete | 18:00 GMT | 18:15 GMT | MDC Manager |
| IPV validation complete | 18:30 GMT | 18:45 GMT | Product Control Head |
| Snapshot publication | 18:30 GMT | 19:00 GMT | Head of MDC |

---

## 8. Exception Handling

### 8.1 Late Trader Marks

| Scenario | Response | Escalation |
|----------|----------|------------|
| Mark 15 min late | Accept with warning | Desk Head |
| Mark 30+ min late | Use T-1 mark with flag | MDC Manager → MLRC |
| Recurring late submission | Escalate to CRO | Head of Market Risk |

### 8.2 Curve Building Failures

| Scenario | Response | Escalation |
|----------|----------|------------|
| Single curve fails | Investigate and rebuild | MDC Analyst |
| Multiple curves fail | Halt snapshot; investigate | MDC Manager |
| System outage | Invoke BCP procedures | Head of MDC → IT |

### 8.3 IPV Challenges

| Scenario | Response | Escalation |
|----------|----------|------------|
| Minor variance | Adjust mark within tolerance | Product Control |
| Material variance | Desk justification required | Product Control Head |
| Unresolved dispute | CFO determination | CFO |

---

## 9. Regional Coordination

### 9.1 Asia EOD Feed

| Activity | Time (HKT) | Owner |
|----------|------------|-------|
| Asia markets close | 17:00 | N/A |
| Asia snapshot captured | 17:30 | Asia MDC |
| Asia snapshot transmitted to London | 18:00 | IT |
| Asia snapshot validated in London | 08:00 GMT (next day) | Global MDC |

### 9.2 Americas EOD Feed

| Activity | Time (EST) | Owner |
|----------|------------|-------|
| Americas markets close | 17:00 | N/A |
| Americas snapshot captured | 17:30 | Americas MDC |
| Americas snapshot transmitted to London | 18:00 | IT |
| Americas snapshot validated in London | 23:00 GMT (same day) | Global MDC |

### 9.3 Global Consolidation

The **London EOD snapshot** is the official global snapshot, incorporating:
- Direct London market observations
- Validated Asia EOD data
- Americas EOD data (for instruments not traded in London)

Regional differences are addressed in the [Regional EOD Management](./regional-eod-management.md) process.

---

## 10. Integration Points

### 10.1 Upstream Dependencies

| System/Process | Data Provided |
|----------------|---------------|
| **Trading Systems (Murex)** | Trader marks, curve inputs |
| **Bloomberg** | External market data |
| **Exchanges** | Official closing prices |
| **Asia/Americas MDC** | Regional EOD snapshots |

### 10.2 Downstream Consumers

| System/Process | Data Consumed | Purpose |
|----------------|---------------|---------|
| **Valuation Engine** | Official curves and prices | MTM valuation |
| **Time Series Service** | EOD observations | VaR calculation |
| **P&L Systems** | Official prices | Daily P&L |
| **Finance/Regulatory Reporting** | Official snapshot | Regulatory submissions |

---

## 11. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Parent orchestration |
| [Time Series Management](./time-series-management/time-series-overview.md) | Downstream consumer |
| [Regional EOD Management](./regional-eod-management.md) | Regional coordination |
| [Market Risk Policy](../L3-Governance/policies/market-risk-policy.md) | Governance framework |

---

## 12. Document Control

### 12.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | MLRC |

---

*End of Document*
