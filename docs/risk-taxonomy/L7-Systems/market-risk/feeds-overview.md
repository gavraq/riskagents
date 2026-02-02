---
# System Metadata
document_id: MR-L7-003
document_name: Market Risk Feeds Overview
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
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
l4_processes:
  - MR-L4-001   # Market Risk Process Orchestration
  - MR-L4-006   # Risk Engine Calculation
l5_controls:
  - MR-L5-001   # VaR and SVaR Limits
l6_models:
  - MR-L6-001   # Historical Simulation VaR
  - MR-L6-002   # ECAP and EaR Methodology
l7_systems:
  - MR-L7-001   # System Architecture
  - MR-L7-002   # Data Dictionary
---

# Market Risk Feeds Overview

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | MR-L7-003 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Risk Technology |

---

## 1. Executive Summary

This document provides a comprehensive overview of the data feeds that support the Market Risk process at Meridian Global Bank. It describes the feed categories, documentation standards, and governance framework that ensures data quality and auditability for regulatory and management reporting.

The Murex trading and risk management system is the primary source of risk data feeds, producing outputs that flow downstream to the Risk Engine, Risk Data Warehouse, and regulatory reporting systems.

---

## 2. Feed Architecture Overview

### 2.1 High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     MARKET RISK FEED ARCHITECTURE                                       │
│                     Meridian Global Bank                                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  UPSTREAM SOURCES                                                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │    MUREX        │  │   BOOKMAN       │  │   BLOOMBERG     │  │    REUTERS      │     │
│  │   (Trading)     │  │   (Hierarchy)   │  │  (Market Data)  │  │  (Market Data)  │     │
│  │                 │  │                 │  │                 │  │                 │     │
│  │  • Trades       │  │  • Portfolio    │  │  • Prices       │  │  • Prices       │     │
│  │  • Positions    │  │    hierarchy    │  │  • Curves       │  │  • Curves       │     │
│  │  • Valuations   │  │  • Book         │  │  • Vol surfaces │  │  • Vol surfaces │     │
│  │  • Sensitivities│  │    mappings     │  │  • Credit       │  │                 │     │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘     │
│           │                    │                    │                    │              │
└───────────┼────────────────────┼────────────────────┼────────────────────┼──────────────┘
            │                    │                    │                    │
            ▼                    ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  MUREX DATAMART                                                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │                           EOD BATCH PROCESSING                                    │  │
│  │                                                                                   │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │  │
│  │  │ Valuation   │  │ Sensitivity │  │ Risk Matrix │  │   Stress    │               │  │
│  │  │   Batch     │  │    Batch    │  │    Batch    │  │    Batch    │               │  │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘               │  │
│  │         │                │                │                │                      │  │
│  │         ▼                ▼                ▼                ▼                      │  │
│  │  ┌─────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │                     DATAMART FEEDERS (ANT Scripts)                          │  │  │
│  │  │                                                                             │  │  │
│  │  │  • Data extraction from Murex calculation results                           │  │  │
│  │  │  • Field mapping and transformation                                         │  │  │
│  │  │  • Aggregation to reporting hierarchies                                     │  │  │
│  │  │  • Data quality validation                                                  │  │  │
│  │  │  • Output file generation                                                   │  │  │
│  │  └─────────────────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                           │                                             │
└───────────────────────────────────────────┼─────────────────────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│  DOWNSTREAM CONSUMERS                                                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │   RISK ENGINE   │  │   RISK DATA     │  │   REGULATORY    │  │   MANAGEMENT    │     │
│  │   (SYS-MR-003)  │  │   WAREHOUSE     │  │   REPORTING     │  │   REPORTING     │     │
│  │                 │  │  (SYS-MR-004)   │  │                 │  │                 │     │
│  │  • VaR calc     │  │  • Time series  │  │  • IMA/FRTB     │  │  • Dashboards   │     │
│  │  • SVaR calc    │  │  • Historical   │  │  • COREP        │  │  • MLRC packs   │     │
│  │  • IRC calc     │  │    analysis     │  │  • Pillar 3     │  │  • Limit mon    │     │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘     │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Feed Processing Summary

| Process Stage | Timing (GMT) | Description |
|---------------|--------------|-------------|
| **Trade Capture** | 17:00-18:30 | EOD trade extraction from Murex |
| **Market Data** | 17:30-18:30 | EOD market data snapshot |
| **Valuation** | 19:00-21:00 | MTM and sensitivity calculations |
| **Risk Calculation** | 22:00-04:00 | VaR, SVaR, stress tests |
| **Data Extraction** | 04:00-05:30 | Datamart feeder execution |
| **Feed Delivery** | 05:30-07:00 | Feed files published to downstream |

---

## 3. Feed Categories

Murex produces the following categories of feeds to support the Market Risk process:

### 3.1 Feed Category Summary

| # | Feed Category | Description | Frequency | Primary Consumer |
|---|---------------|-------------|-----------|------------------|
| 1 | **Sensitivities** | Position-level Greeks and sensitivities | Daily | Risk Engine, VaR calculation |
| 2 | **Risk Matrices** | Pre-calculated risk metrics by hierarchy | Daily | Risk Reporting |
| 3 | **VaR (P&L Strips)** | Position-level P&L vectors for scenarios | Daily | Risk Engine, VaR aggregation |
| 4 | **Stress Results** | Position-level stress test impacts | Daily | Stress Testing Engine |
| 5 | **IRC** | Incremental Risk Charge components | Daily | IRC calculation |
| 6 | **SIMM** | Initial Margin sensitivities | Daily | SIMM calculation |
| 7 | **FRTB** | FRTB-SA and FRTB-IMA inputs | Daily | Regulatory Capital |
| 8 | **PLA** | P&L Attribution data | Daily | Back-testing, RTPL |
| 9 | **Trades** | Trade and position data | Daily | Reconciliation, Reporting |

### 3.2 Feed Category Details

#### 3.2.1 Sensitivities Feed

**Purpose**: Provides position-level sensitivity metrics (Greeks) for VaR calculation and risk aggregation.

| Attribute | Value |
|-----------|-------|
| **Feed ID** | SENS-001 |
| **Source System** | Murex (SYS-MR-001) |
| **Target System** | Risk Engine (SYS-MR-003) |
| **Frequency** | Daily |
| **SLA** | 05:30 GMT |
| **Volume** | ~50,000 position records |
| **Format** | CSV |

**Key Sensitivity Types**:

| Sensitivity | Description | Unit |
|-------------|-------------|------|
| **DV01** | Interest rate sensitivity per basis point | USD |
| **CS01** | Credit spread sensitivity per basis point | USD |
| **Delta** | FX/Equity price sensitivity | USD |
| **Gamma** | Delta sensitivity (2nd order) | USD |
| **Vega** | Volatility sensitivity | USD |
| **Theta** | Time decay | USD |
| **Rho** | Interest rate sensitivity | USD |

**Reference Documentation**:
- [Sensitivities BRD](./feeds/sensitivities/sensitivities-brd.md)
- [Sensitivities IT Config](./feeds/sensitivities/sensitivities-config.md)
- [Sensitivities IDD](./feeds/sensitivities/sensitivities-idd.md)

#### 3.2.2 Risk Matrices Feed

**Purpose**: Provides pre-aggregated risk metrics at hierarchy levels for dashboard reporting.

| Attribute | Value |
|-----------|-------|
| **Feed ID** | RMAT-001 |
| **Source System** | Murex (SYS-MR-001) |
| **Target System** | Risk DataMart (SYS-MR-004) |
| **Frequency** | Daily |
| **SLA** | 06:00 GMT |
| **Volume** | ~5,000 hierarchy records |
| **Format** | CSV |

#### 3.2.3 VaR Feed (P&L Strips)

**Purpose**: Provides position-level P&L vectors under historical scenarios for VaR aggregation.

| Attribute | Value |
|-----------|-------|
| **Feed ID** | VAR-001 |
| **Source System** | Murex (SYS-MR-001) |
| **Target System** | Risk Engine (SYS-MR-003) |
| **Frequency** | Daily |
| **SLA** | 04:30 GMT |
| **Volume** | ~50,000 positions × 500+ scenarios |
| **Format** | Binary (optimized) |

#### 3.2.4 Stress Results Feed

**Purpose**: Provides position-level P&L impacts under defined stress scenarios.

| Attribute | Value |
|-----------|-------|
| **Feed ID** | STRS-001 |
| **Source System** | Murex (SYS-MR-001) |
| **Target System** | Risk Engine (SYS-MR-003) |
| **Frequency** | Daily |
| **SLA** | 05:00 GMT |
| **Volume** | ~50,000 positions × 50+ scenarios |
| **Format** | CSV |

#### 3.2.5 IRC Feed

**Purpose**: Provides Incremental Risk Charge components for trading book credit risk.

| Attribute | Value |
|-----------|-------|
| **Feed ID** | IRC-001 |
| **Source System** | Murex (SYS-MR-001) |
| **Target System** | Capital System |
| **Frequency** | Daily |
| **SLA** | 06:00 GMT |
| **Volume** | ~10,000 positions |
| **Format** | CSV |

#### 3.2.6 SIMM Feed

**Purpose**: Provides ISDA SIMM sensitivities for initial margin calculation.

| Attribute | Value |
|-----------|-------|
| **Feed ID** | SIMM-001 |
| **Source System** | Murex (SYS-MR-001) |
| **Target System** | Margin Calculation System |
| **Frequency** | Daily |
| **SLA** | 05:30 GMT |
| **Volume** | ~20,000 netting set records |
| **Format** | CSV |

#### 3.2.7 FRTB Feed

**Purpose**: Provides inputs for FRTB Standardised Approach (SA) and Internal Models Approach (IMA).

| Attribute | Value |
|-----------|-------|
| **Feed ID** | FRTB-001 |
| **Source System** | Murex (SYS-MR-001) |
| **Target System** | Capital System |
| **Frequency** | Daily |
| **SLA** | 06:00 GMT |
| **Volume** | ~30,000 risk factor records |
| **Format** | CSV |

#### 3.2.8 PLA Feed

**Purpose**: Provides P&L Attribution data for back-testing and risk/theoretical P&L comparison.

| Attribute | Value |
|-----------|-------|
| **Feed ID** | PLA-001 |
| **Source System** | Murex (SYS-MR-001) |
| **Target System** | Back-testing System |
| **Frequency** | Daily |
| **SLA** | 06:30 GMT |
| **Volume** | ~50,000 position records |
| **Format** | CSV |

#### 3.2.9 Trades Feed

**Purpose**: Provides trade and position data for reconciliation and downstream reporting.

| Attribute | Value |
|-----------|-------|
| **Feed ID** | TRD-001 |
| **Source System** | Murex (SYS-MR-001) |
| **Target System** | Trade ODS (SYS-MR-005) |
| **Frequency** | Daily |
| **SLA** | 19:00 GMT |
| **Volume** | ~50,000 position records |
| **Format** | CSV |

---

## 4. Documentation Standards

### 4.1 Feed Documentation Structure

For each feed category, three key documents are produced to provide transparency and auditability:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     FEED DOCUMENTATION FRAMEWORK                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │  1. BUSINESS REQUIREMENTS DOCUMENT (BRD)                                          │  │
│  │  ─────────────────────────────────────────                                        │  │
│  │                                                                                   │  │
│  │  PURPOSE: States the business requirements specified by the Market Risk Manager   │  │
│  │           in terms of what the calculation should output.                         │  │
│  │                                                                                   │  │
│  │  CONTENTS:                                                                        │  │
│  │  • Business objectives and use cases                                              │  │
│  │  • Data requirements (inputs and outputs)                                         │  │
│  │  • Calculation specifications                                                     │  │
│  │  • Aggregation and reporting requirements                                         │  │
│  │  • Data quality requirements                                                      │  │
│  │  • Timeliness requirements (SLAs)                                                 │  │
│  │                                                                                   │  │
│  │  OWNER: Head of Market Risk Analytics                                             │  │
│  │  APPROVER: MLRC                                                                   │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                         │
│                                           │                                             │
│                                           ▼                                             │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │  2. IT CONFIGURATION DOCUMENT                                                     │  │
│  │  ────────────────────────────────                                                 │  │
│  │                                                                                   │  │
│  │  PURPOSE: States the IT implementation on the Murex system, including specific    │  │
│  │           system settings and configuration parameters that enable the            │  │
│  │           requirements specified by the Market Risk Manager to be calculated.     │  │
│  │                                                                                   │  │
│  │  CONTENTS:                                                                        │  │
│  │  • Murex workflow configuration                                                   │  │
│  │  • Batch job parameters                                                           │  │
│  │  • Calculation engine settings                                                    │  │
│  │  • Portfolio scoping rules                                                        │  │
│  │  • Market data set assignments                                                    │  │
│  │  • Filtering and exclusion rules                                                  │  │
│  │                                                                                   │  │
│  │  OWNER: Risk Technology                                                           │  │
│  │  APPROVER: Technology Steering Committee                                          │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                         │
│                                           │                                             │
│                                           ▼                                             │
│                                                                                         │
│  ┌───────────────────────────────────────────────────────────────────────────────────┐  │
│  │  3. INTERFACE DEFINITION DOCUMENT (IDD)                                           │  │
│  │  ──────────────────────────────────────                                           │  │
│  │                                                                                   │  │
│  │  PURPOSE: States the final Datamart tables and extraction process to populate     │  │
│  │           the final feeds, including field name mapping from Murex datamart       │  │
│  │           tables to field names included in the feeds sent downstream.            │  │
│  │                                                                                   │  │
│  │  CONTENTS:                                                                        │  │
│  │  • Source table definitions                                                       │  │
│  │  • Target file/table specifications                                               │  │
│  │  • Field mapping (source to target)                                               │  │
│  │  • Data transformations and derivations                                           │  │
│  │  • Data type conversions                                                          │  │
│  │  • File format specifications (delimiters, encoding)                              │  │
│  │  • Filtering rules and completeness controls                                      │  │
│  │                                                                                   │  │
│  │  OWNER: Risk Technology                                                           │  │
│  │  APPROVER: Head of Risk Technology                                                │  │
│  └───────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Documentation Inventory

| Feed Category | BRD | IT Config | IDD | Status |
|---------------|-----|-----------|-----|--------|
| Sensitivities | SENS-BRD-001 | SENS-CFG-001 | SENS-IDD-001 | Planned |
| Risk Matrices | RMAT-BRD-001 | RMAT-CFG-001 | RMAT-IDD-001 | Planned |
| VaR (P&L Strips) | VAR-BRD-001 | VAR-CFG-001 | VAR-IDD-001 | Planned |
| Stress Results | STRS-BRD-001 | STRS-CFG-001 | STRS-IDD-001 | Planned |
| IRC | IRC-BRD-001 | IRC-CFG-001 | IRC-IDD-001 | Planned |
| SIMM | SIMM-BRD-001 | SIMM-CFG-001 | SIMM-IDD-001 | Planned |
| FRTB | FRTB-BRD-001 | FRTB-CFG-001 | FRTB-IDD-001 | Planned |
| PLA | PLA-BRD-001 | PLA-CFG-001 | PLA-IDD-001 | Planned |
| Trades | TRD-BRD-001 | TRD-CFG-001 | TRD-IDD-001 | Planned |

---

## 5. Murex Operating Model

### 5.1 Global Operating Model Overview

The Murex Global Operating Model (GOM) provides the framework for trade booking, valuation, and risk calculation across all regions.

#### 5.1.1 Key Components

| Component | Description | Relevance to Feeds |
|-----------|-------------|-------------------|
| **Trade Booking** | Standardized booking conventions across asset classes | Determines position structure in feeds |
| **Portfolio Hierarchy** | 7-level structure from Root to Portfolio | Controls aggregation in risk feeds |
| **Market Data Sets** | Official EOD prices vs. VaR calculation prices | Different feeds use different price sets |
| **EOD Processing** | Batch orchestration for valuations and risk | Determines feed timing and dependencies |
| **Datamart Feeders** | ANT scripts extracting data to downstream | Core extraction mechanism for all feeds |

#### 5.1.2 Portfolio Hierarchy Structure

The Bookman hierarchy system manages the 7-level portfolio structure:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     PORTFOLIO HIERARCHY (BOOKMAN)                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Level 1: ROOT                                                                          │
│  └── Level 2: PROCESSING CENTRE (e.g., LONDON, NEW YORK, HONG KONG)                     │
│      └── Level 3: DIVISION (e.g., Global Markets, Treasury)                             │
│          └── Level 4: BUSINESS UNIT (e.g., Rates, Credit, FX)                           │
│              └── Level 5: ENTITY SET (e.g., Trading, Banking Book)                      │
│                  └── Level 6: CLOSING ENTITY (Legal entity for booking)                 │
│                      └── Level 7: AGGREGATION NODE                                      │
│                          └── Level 8: PORTFOLIO (Lowest level for position)             │
│                                                                                         │
│  EXAMPLE:                                                                               │
│  ROOT                                                                                   │
│  └── LONDON                                                                             │
│      └── GLOBAL_MARKETS                                                                 │
│          └── RATES                                                                      │
│              └── TRADING                                                                │
│                  └── MERIDIAN_UK                                                        │
│                      └── RATES_SWAPS                                                    │
│                          └── RATES_SWAPS_USD                                            │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 5.1.3 Market Data Sets

| Set Type | Name | Usage | Feed Relevance |
|----------|------|-------|----------------|
| **Official EOD** | NYCLOSE | NY market close prices | Trade feeds, P&L |
| **Official EOD** | LNCLOSE | London market close prices | Trade feeds, P&L |
| **Official EOD** | HKCLOSE | Hong Kong market close prices | Trade feeds, P&L |
| **VaR Calculation** | NYVARVAL | NY close for VaR (with adjustments) | Sensitivity feeds |
| **VaR Calculation** | LNVARVAL | London close for VaR | Sensitivity feeds |
| **VaR Calculation** | HKVARVAL | Hong Kong close for VaR | Sensitivity feeds |
| **Stress Testing** | STRESS | Stressed market data | Stress feeds |

### 5.2 EOD Processing Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     EOD PROCESSING FLOW                                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  17:00 ─────────────────────────────────────────────────────────────────────────────    │
│  │  • Trade cut-off for Asia                                                            │
│  │  • Internal marks collection begins                                                  │
│  │                                                                                      │
│  17:30 ─────────────────────────────────────────────────────────────────────────────    │
│  │  • Trade cut-off for London                                                          │
│  │  • Bloomberg/Reuters EOD snapshot capture                                            │
│  │                                                                                      │
│  18:00 ─────────────────────────────────────────────────────────────────────────────    │
│  │  • Exchange settlement prices received                                               │
│  │  • EOD trade extraction from Murex begins                                            │
│  │                                                                                      │
│  18:30 ─────────────────────────────────────────────────────────────────────────────    │
│  │  • Trade reconciliation                                                              │
│  │  • Market data validation complete                                                   │
│  │                                                                                      │
│  19:00 ─────────────────────────────────────────────────────────────────────────────    │
│  │  • TRADE FEED PUBLISHED                                                              │
│  │  • Valuation batch begins                                                            │
│  │                                                                                      │
│  21:00 ─────────────────────────────────────────────────────────────────────────────    │
│  │  • MTM validation complete                                                           │
│  │  • Valuation ODS refresh complete                                                    │
│  │                                                                                      │
│  22:00 ─────────────────────────────────────────────────────────────────────────────    │
│  │  • Risk Engine batch begins                                                          │
│  │  • Sensitivity calculation begins                                                    │
│  │                                                                                      │
│  01:00+1 ────────────────────────────────────────────────────────────────────────────   │
│  │  • P&L strip calculation complete                                                    │
│  │                                                                                      │
│  04:00+1 ────────────────────────────────────────────────────────────────────────────   │
│  │  • Risk calculation complete                                                         │
│  │  • Datamart feeder execution begins                                                  │
│  │                                                                                      │
│  04:30+1 ────────────────────────────────────────────────────────────────────────────   │
│  │  • VAR (P&L STRIPS) FEED PUBLISHED                                                   │
│  │                                                                                      │
│  05:00+1 ────────────────────────────────────────────────────────────────────────────   │
│  │  • STRESS RESULTS FEED PUBLISHED                                                     │
│  │                                                                                      │
│  05:30+1 ────────────────────────────────────────────────────────────────────────────   │
│  │  • SENSITIVITIES FEED PUBLISHED                                                      │
│  │  • SIMM FEED PUBLISHED                                                               │
│  │                                                                                      │
│  06:00+1 ────────────────────────────────────────────────────────────────────────────   │
│  │  • RISK MATRICES FEED PUBLISHED                                                      │
│  │  • IRC FEED PUBLISHED                                                                │
│  │  • FRTB FEED PUBLISHED                                                               │
│  │                                                                                      │
│  06:30+1 ────────────────────────────────────────────────────────────────────────────   │
│  │  • PLA FEED PUBLISHED                                                                │
│  │                                                                                      │
│  07:00+1 ────────────────────────────────────────────────────────────────────────────   │
│  │  • All feeds complete                                                                │
│  │  • Risk reporting available                                                          │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Data Quality Controls

### 6.1 Feed-Level Controls

Each feed includes built-in controls to ensure data completeness and accuracy:

| Control Type | Description | Frequency |
|--------------|-------------|-----------|
| **Record Count** | Compare extracted vs. expected record counts | Per feed |
| **Completeness** | Validate all required fields populated | Per feed |
| **Cross-Reference** | Validate hierarchy and reference data joins | Per feed |
| **Range Checks** | Validate values within expected ranges | Per feed |
| **Reconciliation** | Cross-feed consistency checks | Daily |

### 6.2 Filtering and Scoping

Documentation outlines specific filtering rules to ensure data completeness:

| Filter Type | Description | Documentation Reference |
|-------------|-------------|------------------------|
| **Portfolio Scope** | Which portfolios are in/out of scope | IT Config Document |
| **Product Scope** | Which product types are included | IT Config Document |
| **Calculation Scope** | Which calculations are run | IT Config Document |
| **Hierarchy Mapping** | How positions map to hierarchy | IDD |
| **Exception Handling** | How unmapped items are treated | IDD |

### 6.3 Reconciliation Framework

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     FEED RECONCILIATION FRAMEWORK                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  LEVEL 1: SOURCE RECONCILIATION                                                         │
│  ─────────────────────────────────                                                      │
│  • Trade feed count vs. Murex position count                                            │
│  • Sensitivity feed count vs. valuation batch output                                    │
│  • Risk feed count vs. risk engine output                                               │
│                                                                                         │
│  LEVEL 2: CROSS-FEED RECONCILIATION                                                     │
│  ─────────────────────────────────────                                                  │
│  • Trade feed positions = Sensitivity feed positions                                    │
│  • Sensitivity feed positions = P&L strip positions                                     │
│  • Stress positions = Sensitivity positions                                             │
│                                                                                         │
│  LEVEL 3: DOWNSTREAM RECONCILIATION                                                     │
│  ───────────────────────────────────                                                    │
│  • Feed positions = Risk Engine positions loaded                                        │
│  • Feed aggregates = Data Warehouse aggregates                                          │
│                                                                                         │
│  ESCALATION:                                                                            │
│  • Tolerance: ±1% on counts, ±0.1% on values                                            │
│  • Breaks escalated to RAV team                                                         │
│  • Material breaks (>$1M VaR impact) escalated to Head of Market Risk Analytics         │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Feed Change Management

### 7.1 Change Categories

| Category | Definition | Approval | Lead Time |
|----------|------------|----------|-----------|
| **Field Addition** | Add new field to existing feed | IT + Business | 10 business days |
| **Field Removal** | Remove field from feed | IT + Business + Downstream | 20 business days |
| **Format Change** | Change data type or format | IT + Downstream | 10 business days |
| **New Feed** | Create entirely new feed | MLRC | 30 business days |
| **Feed Retirement** | Decommission feed | MLRC + Downstream | 60 business days |

### 7.2 Change Process

1. **Request**: Submit change request via IT Service Management
2. **Impact Assessment**: Assess impact on downstream consumers
3. **Design**: Update BRD, IT Config, and IDD as appropriate
4. **Test**: Execute in SIT and UAT environments
5. **Approve**: Obtain required approvals
6. **Implement**: Deploy to production with rollback plan
7. **Validate**: Confirm feed functioning as expected
8. **Document**: Update all related documentation

---

## 8. Feed Monitoring and Alerting

### 8.1 Monitoring Dashboard

| Metric | Description | Threshold | Alert |
|--------|-------------|-----------|-------|
| **Feed Latency** | Time from SLA to delivery | >30 min | Warning |
| **Feed Latency** | Time from SLA to delivery | >60 min | Critical |
| **Record Count** | Deviation from T-1 | >10% | Warning |
| **Record Count** | Deviation from T-1 | >25% | Critical |
| **Feed Failure** | Feed not delivered | Missing | Critical |
| **Data Quality** | Quality check failures | >0 | Warning |

### 8.2 Escalation Matrix

| Severity | Response Time | Escalation Path |
|----------|---------------|-----------------|
| **Critical** | 15 minutes | Risk Technology → Head of Risk Technology → CRO |
| **Warning** | 30 minutes | Risk Technology → RAV Team |
| **Information** | Next business day | Risk Technology |

---

## 9. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [System Architecture](./system-architecture.md) | MR-L7-001 | Parent system context |
| [Data Dictionary](./data-dictionary.md) | MR-L7-002 | Field-level definitions |
| [Sensitivities Feed BRD](./feeds/sensitivities/sensitivities-brd.md) | SENS-BRD-001 | Detailed feed spec |
| [VaR/SVaR Methodology](../L6-Models/market-risk/var-svar-methodology.md) | MR-L6-001 | Risk methodology |
| [Risk Engine Calculation](../L4-Processes/processes/risk-engine-calculation.md) | MR-L4-006 | Process using feeds |

---

## 10. Document Control

### 10.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-02 | Initial version | Risk Technology |

### 10.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Feed inventory | Quarterly | April 2025 |
| SLA review | Quarterly | April 2025 |

---

*End of Document*
