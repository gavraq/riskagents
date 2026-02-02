# Risk Taxonomy Framework - Implementation Plan

**Project**: Risk Agents Platform - Knowledge Foundation
**Version**: 2.0
**Date**: 2025-12-11
**Status**: DRAFT
**Changes**: v2.0 - Added ICBCS real data sources, Apache Iceberg architecture, policy framework guidance, composable skills concept

---

## Executive Summary

This document outlines the comprehensive plan for building the Risk Taxonomy Framework - a hierarchical knowledge structure that serves as the foundational layer for the Risk Agents platform. The taxonomy provides:

1. **For Humans**: A knowledge management platform enabling rapid onboarding, cross-training, and regulatory/audit communication
2. **For AI Agents**: Context-aware retrieval allowing efficient token usage and precise information sourcing
3. **For Skills**: A completeness map showing which capabilities exist and where gaps remain across the 9 risk domains

The framework follows a "pyramid" structure with high-level strategic information at the apex flowing down to detailed operational data at the base, with full lineage/audit trail throughout.

---

## Table of Contents

1. [Vision & Objectives](#1-vision--objectives)
2. [Taxonomy Pyramid Architecture](#2-taxonomy-pyramid-architecture)
3. [Reference Bank Design](#3-reference-bank-design)
4. [Data Lakehouse Architecture](#4-data-lakehouse-architecture) **(NEW)**
5. [Implementation Phases](#5-implementation-phases)
6. [Skills Mapping Framework](#6-skills-mapping-framework)
7. [Technical Architecture](#7-technical-architecture)
8. [Policy Framework Guidelines](#8-policy-framework-guidelines) **(NEW)**
9. [Deliverables & Artefacts](#9-deliverables--artefacts)
10. [Success Metrics](#10-success-metrics)

---

## 1. Vision & Objectives

### 1.1 Vision Statement

Create a **living, linked knowledge ecosystem** that transforms risk management expertise into an accessible, structured, and queryable resource that powers both human understanding and AI agent responses.

### 1.2 Primary Objectives

| Objective | Human Benefit | AI/Agent Benefit |
|-----------|---------------|------------------|
| **Structure** | Clear navigation through risk domains | Efficient context retrieval without loading all documents |
| **Completeness** | Demonstrate comprehensive coverage to regulators/auditors | Map skills to taxonomy nodes - identify gaps |
| **Linkage** | Audit trail from requirements → controls → data | Query expansion - find related content automatically |
| **Currency** | Self-documenting through API-first infrastructure | Auto-update documentation when schemas change |
| **Consistency** | Standard nomenclature across risk domains | Reliable entity recognition in queries |

### 1.3 Design Principles

1. **Federated Ownership**: Central framework, distributed maintenance by domain experts
2. **API-First Infrastructure**: Systems publish schemas; documentation auto-updates
3. **Progressive Disclosure**: Top-level summaries expand to detail on demand
4. **Audit Trail**: Every node links to parent requirements and child implementations
5. **Skills Integration**: Each taxonomy node maps to applicable Risk Agent skills

---

## 2. Taxonomy Pyramid Architecture

### 2.1 The Seven-Layer Pyramid

```
                    ┌─────────────────────┐
                    │   L1: REQUIREMENTS  │  ← Regulatory & Business Drivers
                    │   (Why we do this)  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   L2: RISK TYPES    │  ← Risk Classification & Definitions
                    │   (What risks)      │
                    └──────────┬──────────┘
                               │
              ┌────────────────▼────────────────┐
              │       L3: GOVERNANCE            │  ← Policies, Committees, Mandates
              │       (Who decides)             │
              └────────────────┬────────────────┘
                               │
         ┌─────────────────────▼─────────────────────┐
         │           L4: PROCESSES                   │  ← Business Processes & Procedures
         │           (How we operate)                │
         └─────────────────────┬─────────────────────┘
                               │
    ┌──────────────────────────▼──────────────────────────┐
    │              L5: CONTROLS & METRICS                 │  ← KRIs, Limits, RCSA Controls
    │              (How we measure & control)             │
    └──────────────────────────┬──────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                  L6: MODELS & METHODOLOGIES                 │  ← Calculations, Algorithms
│                  (How we calculate)                         │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                 L7: DATA, SYSTEMS & FEEDS                       │  ← Infrastructure Layer
│                 (What data, where stored, how flows)            │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Layer Definitions

| Layer | Name | Description | Key Artefacts | Example Content |
|-------|------|-------------|---------------|-----------------|
| **L1** | Requirements | Regulatory mandates and business requirements driving risk management | Regulatory inventory, Strategic objectives | CRR Art. 325, PRA SS1/23, BCBS239 |
| **L2** | Risk Types | Classification of risks into types, sub-types, definitions | Risk Taxonomy document, Materiality matrix | Credit Risk → Counterparty → Pre-settlement |
| **L3** | Governance | Committees, policies, mandates, terms of reference | Policy inventory, Committee TORs, RACI | ALCO, RMC, Credit Committee, Market Risk Policy |
| **L4** | Processes | Business processes, procedures, workflows | Process catalogue, Procedure documents, BPMN | Daily VaR production, Credit approval workflow |
| **L5** | Controls & Metrics | Key controls, KRIs, limits, RCSA | Control inventory, KRI definitions, Limit framework | VaR limits, Credit concentration limits, DQ checks |
| **L6** | Models | Risk models, methodologies, validation | Model registry, Methodology docs, Validation reports | VaR model, PD/LGD models, ECL models |
| **L7** | Data/Systems | Data domains, systems, feeds, architecture | Data dictionary, System inventory, Feed IDDs, Architecture | Market Risk System, Credit Risk System e.g. Adaptiv, market data feeds, trade feeds |

### 2.3 Cross-Cutting Dimensions

In addition to the vertical layers, three dimensions cut across the entire taxonomy:

| Dimension | Description | Purpose |
|-----------|-------------|---------|
| **Products** | Approved Product List, Trade Execution Framework | Links risk activities to specific product types |
| **Reports** | Report inventory with dependencies | Output layer - what MI is produced from each process |
| **Change** | Change artefacts (BRD, FRD, Test packs) | Tracks evolution of taxonomy components |

---

## 3. Reference Bank Design

### 3.1 "Best Practice Bank" Concept

Rather than using real bank data with confidentiality concerns, we'll create a **fictional but realistic reference bank** that demonstrates best practices:

| Attribute | Reference Bank Value | Rationale |
|-----------|---------------------|-----------|
| **Name** | Meridian Global Bank | Fictional name, no trademark issues |
| **Type** | Universal bank with trading operations | Covers both banking and trading book risks |
| **Size** | Mid-tier GSIB ($50-100bn assets) | Large enough for complexity, small enough to document |
| **Geography** | UK-headquartered, global operations | PRA-regulated, international scope |
| **Business Lines** | Markets, Transaction Banking, Asset Management | Representative product mix |
| **Regulator** | PRA/FCA (UK), with Fed/OCC considerations | Familiar regulatory framework |

### 3.2 Reference Implementation Scope

For Phase 1, we'll build out **two complete vertical slices** through the taxonomy:

#### Vertical Slice 1: Market Risk - Comprehensive ✅ COMPLETE
Complete end-to-end from regulatory requirement to daily data

```
L1: CRR Art. 325 (IMA approval) + BCBS239 (data aggregation) + CRR 104b (desk mandates)
    ↓
L2: Market Risk → Trading Book Risk → VaR, SVaR, IRC, Stress
    ↓
L3: Market Risk Policy → MLRC Committee → VaR Limit Framework
    ↓
L4: Market Risk Process Orchestration (14 sub-processes)
    ├── Trade Capture Controls
    ├── EOD Market Data Snapshot
    ├── Regional EOD Management
    ├── Time Series Management (6 sub-docs)
    ├── Risk Engine Calculation (VaR/SVaR)
    ├── VaR Reporting & Sign-off
    ├── Backtesting
    ├── Regulatory Reporting
    ├── IRC Calculation
    ├── Stress Testing (Pillar/PoW)
    ├── Desk Mandate Management
    └── Hierarchy Management
    ↓
L5: VaR Limits, Stress Limits, Sensitivity Limits, Concentration Limits, Stop-Loss, Backtesting
    ↓
L6: Historical Simulation VaR/SVaR methodology (RNIV, proxy governance, data floors)
    ↓
L7: Risk Engine, ODSs (Trade, Market Data, Valuations, Risk, P&L, Hierarchy)
```

**Status**: 30 documents complete across L3-L7. See Section 5.1 for full inventory.

#### Vertical Slice 2: Credit Risk - Counterparty Limit Management
Complete end-to-end from regulatory requirement to daily data

```
L1: CRR Part 3 (Credit Risk) + Large Exposures Regime
    ↓
L2: Credit Risk → Counterparty Risk → Pre-settlement Risk
    ↓
L3: Credit Risk Policy → Credit Committee → Limit Delegation
    ↓
L4: Credit Limit Approval Process, Daily Exposure Monitoring
    ↓
L5: Counterparty limits, Concentration limits, Excess management
    ↓
L6: PFE model, PD/LGD models, Wrong Way Risk model
    ↓
L7: Trade feeds, Counterparty master, Credit Risk system, Collateral data
```

### 3.3 Data Sources - ICBCS Reference Data

Rather than creating synthetic data from scratch, we leverage **real anonymized data from ICBCS Bank** to provide authentic examples of risk data structures, feed formats, and metrics calculations.

#### Available ICBCS Data Sources

| Data Category | Location | Contents |
|---------------|----------|----------|
| **Feed Documentation** | `/data/ICBCS Bank/Feeds/Feed Documentation/` | 27 PDFs covering sensitivities (IR, FX, Credit, Commodities), VaR methodology, stress testing documentation |
| **Metrics Definitions** | `/data/ICBCS Bank/metrics/` | Product attribute spreadsheets, metrics documentation, CDM mappings |
| **Murex Trade Data** | `/data/ICBCS Bank/Systems/Market Risk/Murex/Feeds/` | Actual sensitivity data (MxGTS files), trade attributes, static reference data |
| **FMDM Risk Data** | `/data/ICBCS Bank/Systems/Market Risk/FMDM/Feeds/` | VaR curve data, energy surfaces, stress test parameters |

#### Key ICBCS Data Files

**Feed Documentation** (27 PDFs):
- Interest Rate Sensitivities documentation
- FX Sensitivities documentation
- Credit Sensitivities documentation
- Commodity Sensitivities documentation
- VaR methodology and calculation guides
- Stress testing frameworks

**Murex Feeds**:
- `MxGTS_*.zip` - Trade sensitivity extracts
- `PacMan/` - Hierarchy data
- `static_mr.csv` - Market risk static data

**FMDM Feeds**:
- VaR curve data files
- Energy surface parameters
- Stress test scenario data

#### Data Usage Approach

| Data Type | ICBCS Source | Meridian Reference Use |
|-----------|--------------|------------------------|
| **Market Data Structures** | FMDM VaR curves, energy surfaces | Template for curve/surface definitions |
| **Trade Data Schemas** | Murex MxGTS exports | FpML-to-Parquet field mappings |
| **Sensitivity Formats** | IR/FX/Credit/Commodity PDFs | Reference for sensitivity calculations |
| **Risk Metrics** | Metrics documentation | KRI/KPI definitions |
| **Feed Specifications** | Feed Documentation PDFs | IDD templates for L7 |

---

## 4. Data Lakehouse Architecture

### 4.1 Architecture Overview

The reference implementation uses an **Apache Iceberg Data Lakehouse** architecture, adapted from the Nordea Trading & Risk reference architecture. This replaces the traditional Trading Data Warehouse approach with a modern lakehouse pattern.

#### Key Architecture Principles

1. **Parquet for Storage**: All data stored as Parquet files (not XML, even for FpML trades)
2. **Iceberg for Management**: Apache Iceberg table format for ACID transactions, time travel, schema evolution
3. **Query Engine Flexibility**: On-the-fly joins via Trino, DuckDB, or Spark
4. **ODS Pattern Retained**: Operational Data Stores concept from Nordea retained, but stored as Iceberg tables

### 4.2 Apache Iceberg Overview

Apache Iceberg is an open table format for large analytic datasets that brings database-like capabilities to data lakes:

#### Core Concepts

| Concept | Description |
|---------|-------------|
| **Table Format** | Defines how to organize data files, metadata, and enable ACID transactions |
| **Parquet Files** | Actual data stored in columnar Parquet format (efficient storage/retrieval) |
| **Metadata Layer** | Three-tier hierarchy: Metadata JSON → Manifest Lists → Manifest Files |
| **Catalog** | Single source of truth for table locations (REST Catalog, Hive, AWS Glue) |
| **Snapshots** | Immutable point-in-time views enabling time travel queries |

#### Key Features for Risk Management

| Feature | Benefit for Risk |
|---------|------------------|
| **Time Travel** | Reconstruct any historical position/valuation state for audit |
| **Schema Evolution** | Add new risk factors without breaking existing queries |
| **Partition Evolution** | Change partitioning strategy without rewriting data |
| **ACID Transactions** | Reliable concurrent writes from multiple risk processes |
| **Hidden Partitioning** | Partition by business date/trade date without exposing to queries |
| **Column-Level Statistics** | Fast filtering for specific instruments, desks, dates |

### 4.3 Adapted Nordea Architecture

The Nordea Trading & Risk architecture provides a component-based reference with ODSs feeding a Trading Data Warehouse. We adapt this to an Iceberg lakehouse:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DATA LAKEHOUSE (Apache Iceberg)                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │                    OPERATIONAL DATA STORES (as Iceberg Tables)           │  │
│   ├──────────────────────────────────────────────────────────────────────────┤  │
│   │                                                                          │  │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│   │  │ Counterparty │  │  Agreement   │  │   Product    │  │    Book      │  │  │
│   │  │     ODS      │  │     ODS      │  │     ODS      │  │     ODS      │  │  │
│   │  │  (Parquet)   │  │  (Parquet)   │  │  (Parquet)   │  │  (Parquet)   │  │  │
│   │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│   │                                                                          │  │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│   │  │ Instrument   │  │   TradeHub   │  │ Market Data  │  │  Valuations  │  │  │
│   │  │     ODS      │  │     ODS      │  │     ODS      │  │     ODS      │  │  │
│   │  │  (Parquet)   │  │  (Parquet)   │  │  (Parquet)   │  │  (Parquet)   │  │  │
│   │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│   │                                                                          │  │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                    │  │
│   │  │     Risk     │  │  Accounting  │  │     P&L      │                    │  │
│   │  │     ODS      │  │   Cash ODS   │  │     ODS      │                    │  │
│   │  │  (Parquet)   │  │  (Parquet)   │  │  (Parquet)   │                    │  │
│   │  └──────────────┘  └──────────────┘  └──────────────┘                    │  │
│   │                                                                          │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │                         QUERY ENGINE LAYER                               │  │
│   │                                                                          │  │
│   │     ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                │  │
│   │     │    Trino    │    │   DuckDB    │    │    Spark    │                │  │
│   │     │  (Federated │    │  (Local/    │    │  (Large-    │                │  │
│   │     │   Queries)  │    │   Dev)      │    │   Scale)    │                │  │
│   │     └─────────────┘    └─────────────┘    └─────────────┘                │  │
│   │                                                                          │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                        ┌───────────────┴───────────────┐
                        │      ICEBERG CATALOG          │
                        │   (REST Catalog / Nessie)     │
                        │  - Table locations            │
                        │  - Schema versions            │
                        │  - Snapshot history           │
                        └───────────────────────────────┘
```

### 4.4 ODS Definitions (Adapted from Nordea)

| ODS | Domain | Key Entities | Source Systems |
|-----|--------|--------------|----------------|
| **Counterparty ODS** | Client/Party | Legal entities, ratings, limits | CRM, Credit system |
| **Agreement ODS** | Legal | ISDA, CSA, netting agreements | Legal system |
| **Product ODS** | Reference | Product definitions, lifecycles | Product catalog |
| **Book ODS** | Hierarchy | Book/desk/entity structure | GL, Trading systems |
| **Instrument ODS** | Security | Instrument definitions, static | Security master |
| **TradeHub ODS** | Transactions | All trades (FpML fields extracted) | Trading systems (Murex) |
| **Market Data ODS** | Prices | Curves, surfaces, fixings | Market data vendors |
| **Valuations ODS** | MTM | NPV, Greeks, sensitivities | Valuation engine |
| **Risk ODS** | Metrics | VaR, PFE, stress results | Risk engines |
| **Accounting ODS** | Cash | Cash flows, settlements | GL, Treasury |
| **P&L ODS** | Performance | P&L explain, attribution | P&L engine |

### 4.5 FpML-to-Parquet Transformation

Instead of storing FpML XML files directly (difficult to query), we extract key fields to Parquet:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FpML → Parquet Transformation                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Source: Murex Trade Export (FpML/XML)                                 │
│                                                                         │
│   ┌────────────────────────────────────────────────────────────────┐    │
│   │  <trade>                                                       │    │
│   │    <tradeHeader>                                               │    │
│   │      <partyTradeIdentifier>                                    │    │
│   │        <tradeId>TRD-001234</tradeId>                           │    │
│   │      </partyTradeIdentifier>                                   │    │
│   │    </tradeHeader>                                              │    │
│   │    <swap>                                                      │    │
│   │      <productType>InterestRateSwap</productType>               │    │
│   │      <swapStream>...</swapStream>                              │    │
│   │    </swap>                                                     │    │
│   │  </trade>                                                      │    │
│   └────────────────────────────────────────────────────────────────┘    │
│                           │                                             │
│                           ▼                                             │
│                    Extract & Flatten                                    │
│                           │                                             │
│                           ▼                                             │
│   ┌────────────────────────────────────────────────────────────────┐    │
│   │  TradeHub ODS (Parquet Schema)                                 │    │
│   │                                                                │    │
│   │  trade_id        │ product_type      │ trade_date   │ maturity │    │
│   │  ───────────────────────────────────────────────────────────── │    │
│   │  TRD-001234      │ InterestRateSwap  │ 2024-01-15   │ 2029-01  │    │
│   │                                                                │    │
│   │  notional  │ ccy  │ pay_freq  │ rec_freq  │ book_id  │ cpty_id │    │
│   │  ───────────────────────────────────────────────────────────── │    │
│   │  10000000  │ USD  │ 3M        │ 6M        │ BK-001   │ CP-042  │    │
│   └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.6 Query Engine Selection

| Engine | Use Case | Advantages |
|--------|----------|------------|
| **DuckDB** | Local development, small queries | Zero-config, embedded, very fast |
| **Trino** | Federated queries across ODSs | Distributed, connects to multiple sources |
| **Spark** | Large-scale batch processing | Handles massive datasets, ML integration |

**Recommended Approach**: Use DuckDB for development and small-scale demos, Trino for production-like federated queries.

### 4.7 Time Travel for Audit

Apache Iceberg's snapshot capability enables regulatory-required historical reconstruction:

```sql
-- Query current state
SELECT * FROM risk_ods.var_results WHERE business_date = '2024-12-10';

-- Query state as of yesterday (time travel)
SELECT * FROM risk_ods.var_results FOR TIMESTAMP AS OF '2024-12-10 17:00:00';

-- Query by snapshot ID (for audit)
SELECT * FROM risk_ods.var_results FOR VERSION AS OF 1234567890;

-- View snapshot history
SELECT * FROM risk_ods.var_results.snapshots;
```

---

## 5. Implementation Phases

### Phase 1: Foundation (Weeks 1-4) ✅ COMPLETE
**Objective**: Establish taxonomy structure and first vertical slice

#### Week 1-2: Taxonomy Structure ✅
- [x] Create taxonomy schema (YAML/JSON structure) ✅
- [x] Build L1-L2 content (Requirements, Risk Types) for all 9 risk domains ✅
- [x] Design node linking mechanism (parent-child, cross-references) ✅
- [x] Create documentation templates for each layer ✅

#### Week 3-4: First Vertical Slice (Market Risk) ✅
- [x] L3: Market Risk Policy, MLRC TOR, VaR Limit Framework ✅
- [x] L4: Market Risk Process Orchestration (comprehensive - see Section 5.1) ✅
- [x] L5: VaR limits, Stress limits, Sensitivity limits, Concentration limits, Stop-loss, Backtesting controls ✅
- [x] L6: VaR/SVaR methodology (enhanced with RNIV, proxy governance, data floors) ✅
- [x] L7: System architecture diagram (Risk Engine, ODSs, integrations) ✅

### 5.0 Enterprise Governance - Committee Structure & Risk Appetite ✅ NEW

Enterprise-level governance documents that apply across all risk domains.

#### Enterprise Committees (4 documents) ✅

| Document | ID | Status | Description |
|----------|-----|--------|-------------|
| [Board Terms of Reference](./L3-Governance/committees/enterprise/board-terms-of-reference.md) | GOV-L3-001 | ✅ v1.0 | Board mandate, composition, reserved matters |
| [BRMC Terms of Reference](./L3-Governance/committees/enterprise/brmc-terms-of-reference.md) | GOV-L3-002 | ✅ v1.0 | Board Risk Management Committee - risk oversight |
| [ExCo Terms of Reference](./L3-Governance/committees/enterprise/exco-terms-of-reference.md) | GOV-L3-003 | ✅ v1.0 | Executive Committee - day-to-day management |
| [RMC Terms of Reference](./L3-Governance/committees/enterprise/rmc-terms-of-reference.md) | GOV-L3-004 | ✅ v1.0 | Risk Management Committee - cross-domain risk oversight |

#### Risk Appetite Documents (2 documents) ✅

| Document | ID | Status | Description |
|----------|-----|--------|-------------|
| [Risk Appetite Statement](./L3-Governance/risk-appetite-statement.md) | GOV-L3-010 | ✅ v1.0 | Level 1/2/3 risk appetite metrics with Green/Amber/Red thresholds |
| [Risk Appetite Framework](./L3-Governance/risk-appetite-framework.md) | GOV-L3-011 | ✅ v1.0 | Methodology, cascading, measurement, monitoring, governance |

**Committee Hierarchy:**
```
┌─────────────────────────────────────────────────────────────────┐
│                        BOARD (GOV-L3-001)                        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│      BRMC       │  │  Audit Committee│  │  Remuneration   │
│  (GOV-L3-002)   │  │   (Future)      │  │   (Future)      │
└────────┬────────┘  └─────────────────┘  └─────────────────┘
         │
         │              ┌─────────────────┐
         │              │      ExCo       │
         │              │  (GOV-L3-003)   │
         │              └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
            ┌────────▼────────┐
            │      RMC        │
            │  (GOV-L3-004)   │
            └────────┬────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
┌───────┐      ┌───────┐      ┌───────┐
│ MLRC  │      │ CRMC  │      │ ORMC  │
│MR-L3-2│      │(Future)│      │(Future)│
└───────┘      └───────┘      └───────┘
```

---

### 5.1 Market Risk Vertical Slice - Completion Status (December 2025)

**NOTE**: The Market Risk vertical slice has been expanded significantly beyond the original "VaR Production" scope to cover comprehensive Market Risk processes.

#### L3 - Governance (6 documents) ✅

| Document | ID | Status | Description |
|----------|-----|--------|-------------|
| [Market Risk Policy](./L3-Governance/policies/market-risk-policy.md) | MR-L3-001 | ✅ v1.5 | Umbrella framework policy with taxonomy linkages |
| [MLRC Terms of Reference](./L3-Governance/committees/mlrc-terms-of-reference.md) | MR-L3-002 | ✅ Complete | Committee governance |
| [VaR Limit Framework](./L3-Governance/policies/var-limit-framework.md) | MR-L3-003 | ✅ Complete | Limit structure and delegation |
| [VaR Policy](./L3-Governance/policies/var-policy.md) | MR-L3-004 | ✅ v1.0 | VaR/SVaR governance, time series, proxying, RNIV, backtesting |
| [Stress Testing Policy](./L3-Governance/policies/stress-testing-policy.md) | MR-L3-005 | ✅ v1.0 | Pillar stresses, PoW, scenario design, stress limits |
| [Trading Book Boundary Policy](./L3-Governance/policies/trading-book-boundary-policy.md) | MR-L3-006 | ✅ v1.0 | TB vs BB boundary, reclassification, trading intent, FRTB |

#### L4 - Processes (21 documents) ✅

| Document | ID | Status | Description |
|----------|-----|--------|-------------|
| **[Market Risk Process Orchestration](./L4-Processes/processes/market-risk-process-orchestration.md)** | MR-L4-001 | ✅ v3.2 | **Master orchestration** for all Market Risk processes (14 sub-processes) |
| [Trade Capture Controls](./L4-Processes/processes/trade-capture-controls.md) | MR-L4-002 | ✅ Complete | Trade completeness and reconciliation |
| [EOD Market Data Snapshot](./L4-Processes/processes/eod-market-data-snapshot.md) | MR-L4-003 | ✅ Complete | Official EOD prices, curves, volatilities |
| [Regional EOD Management](./L4-Processes/processes/regional-eod-management.md) | MR-L4-004 | ✅ Complete | Asia/London/NY timing |
| **Time Series Management Suite** | MR-L4-005 | ✅ Complete | 6 sub-documents: |
| → [Time Series Overview](./L4-Processes/processes/time-series-management/time-series-overview.md) | MR-L4-005a | ✅ v1.1 | Master document with proxy lineage |
| → [Instrument Setup](./L4-Processes/processes/time-series-management/instrument-setup.md) | MR-L4-005b | ✅ Complete | Instrument to risk factor mapping |
| → [Risk Factor Setup](./L4-Processes/processes/time-series-management/risk-factor-setup.md) | MR-L4-005c | ✅ Complete | Risk factor creation |
| → [Price Collection](./L4-Processes/processes/time-series-management/price-collection.md) | MR-L4-005d | ✅ Complete | Market data sourcing |
| → [Cleaning & Validation](./L4-Processes/processes/time-series-management/cleaning-validation.md) | MR-L4-005e | ✅ Complete | DQ checks, outlier detection |
| → [Curve Stripping](./L4-Processes/processes/time-series-management/curve-stripping.md) | MR-L4-005f | ✅ Complete | Curve construction |
| → [Proxying Process](./L4-Processes/processes/time-series-management/proxying-process.md) | MR-L4-005g | ✅ v1.1 | Proxy Level Waterfall (1-4) |
| [Risk Engine Calculation](./L4-Processes/processes/risk-engine-calculation.md) | MR-L4-006 | ✅ v1.7 | VaR/SVaR 3-step chain + **Three Parallel Streams** architecture |
| [Market Risk Reporting & Sign-off](./L4-Processes/processes/market-risk-reporting-signoff.md) | MR-L4-007 | ✅ v2.0 | **All three streams**: Sensitivities, VaR/SVaR, Stress reporting |
| [Backtesting](./L4-Processes/processes/backtesting.md) | MR-L4-008 | ✅ Complete | Model validation, Basel traffic light |
| [Regulatory Reporting](./L4-Processes/processes/regulatory-reporting.md) | MR-L4-009 | ✅ Complete | PRA notifications, COREP |
| [IRC Calculation](./L4-Processes/processes/irc-calculation.md) | MR-L4-010 | ✅ v1.0 | Incremental Risk Charge (Monte Carlo) |
| [Stress Testing](./L4-Processes/processes/stress-testing.md) | MR-L4-011 | ✅ v1.2 | Pillar/PoW, FO consultation, Golden Source, **Risk Engine orchestration** |
| [Desk Mandate Management](./L4-Processes/processes/desk-mandate-management.md) | MR-L4-012 | ✅ v1.0 | CRR 104b, designated dealers |
| [Market Risk Limits Management](./L4-Processes/processes/market-risk-limits-management.md) | MR-L4-013 | ✅ v1.1 | **Full limit lifecycle**: setup, monitoring, breach management, annual review |
| [Aged Inventory Monitoring](./L4-Processes/processes/aged-inventory-monitoring.md) | MR-L4-014 | ✅ v1.0 | Quarterly inventory review, ICAAP illiquidity input |
| [Hierarchy Management](./L4-Processes/processes/hierarchy-management.md) | FIN-L4-001 | ✅ v1.1 | Book/desk/entity structure (Finance-owned) |

#### L5 - Controls (7 documents) ✅

| Document | ID | Status | Description |
|----------|-----|--------|-------------|
| [VaR Limits Controls](./L5-Controls/market-risk/var-limits-controls.md) | MR-L5-001 | ✅ v1.1 | Desk/entity VaR/SVaR limits |
| [Stress Limits Controls](./L5-Controls/market-risk/stress-limits-controls.md) | MR-L5-002 | ✅ v1.1 | Stress scenario limits |
| [Sensitivity Limits Controls](./L5-Controls/market-risk/sensitivity-limits-controls.md) | MR-L5-003 | ✅ Complete | DV01, CS01, Vega limits |
| [Backtesting Controls](./L5-Controls/market-risk/backtesting-controls.md) | MR-L5-004 | ✅ Complete | Exception thresholds, traffic light |
| [Concentration Limits Controls](./L5-Controls/market-risk/concentration-limits-controls.md) | MR-L5-005 | ✅ v1.2 | Single name, curve, sector limits; **Aged Inventory controls** |
| [Stop-Loss Controls](./L5-Controls/market-risk/stop-loss-controls.md) | MR-L5-006 | ✅ Complete | P&L trigger limits |
| [ECAP Controls](./L5-Controls/market-risk/ecap-controls.md) | MR-L5-007 | ✅ v1.0 | **Economic Capital** (99.9%, ICAAP contribution) |

#### L6 - Models (2 documents) ✅

| Document | ID | Status | Description |
|----------|-----|--------|-------------|
| [VaR/SVaR Methodology](./L6-Models/market-risk/var-svar-methodology.md) | MR-L6-001 | ✅ v1.1 | HS VaR, SVaR, RNIV, proxy governance, data floors |
| [ECAP Methodology](./L6-Models/market-risk/ecap-methodology.md) | MR-L6-002 | ✅ v1.0 | Economic Capital (99.9%, liquidity-adjusted, ICAAP) |

#### L7 - Systems (1 document) ✅

| Document | ID | Status | Description |
|----------|-----|--------|-------------|
| [System Architecture](./L7-Systems/market-risk/system-architecture.md) | MR-L7-001 | ✅ v1.2 | Risk Engine (incl. ECAP), ODSs, integrations |

#### Summary Statistics - Market Risk Vertical

| Layer | Documents | Status |
|-------|-----------|--------|
| L3 - Governance | 6 | ✅ 100% Complete |
| L4 - Processes | 20 | ✅ 100% Complete |
| L5 - Controls | 7 | ✅ 100% Complete |
| L6 - Models | 2 | ✅ 100% Complete |
| L7 - Systems | 1 | ✅ 100% Complete |
| **TOTAL** | **36** | **✅ 100% Complete** |

#### Overall Summary (Including Enterprise Governance)

| Category | Documents | Status |
|----------|-----------|--------|
| Enterprise Governance (Committees) | 4 | ✅ 100% Complete |
| Enterprise Governance (Risk Appetite) | 2 | ✅ 100% Complete |
| Market Risk Vertical (L3-L7) | 36 | ✅ 100% Complete |
| **GRAND TOTAL** | **42** | **✅ 100% Complete** |

---

### Phase 2: Expansion (Weeks 5-8)
**Objective**: Second vertical slice and horizontal expansion

#### Week 5-6: Second Vertical Slice (Credit Risk)
- [ ] Complete Credit Risk vertical from L3-L7
- [ ] Cross-link to Market Risk where they intersect (CVA, Wrong Way Risk)

#### Week 7-8: Horizontal Expansion at Upper Layers
- [ ] Complete L3 (Governance) across all risk domains
- [ ] Build out L4 (Processes) catalogue with priorities
- [ ] Map existing skills to taxonomy nodes
- [ ] Document cross-functional processes:
  - [ ] NPSTA-L4-001: New Products and Significant Transactions Approval (cross-functional)
  - [ ] Document Market Risk, Credit Risk, Model Risk, Operations, Compliance inputs
- [ ] Document ICAAP Framework:
  - [ ] ICAAP-L3-001: ICAAP Policy and Governance
  - [ ] ICAAP-L4-001: ICAAP Process (annual cycle, quarterly updates)
  - [ ] Link domain-specific ECAP contributions (Market Risk, Credit Risk, Operational Risk)
  - [ ] Document Pillar 2A capital requirements and SREP interaction
  - [ ] Include stressed capital projections and capital planning integration

#### Enterprise Policy Backlog (Future)

The following enterprise-level policies span multiple risk domains and should be developed as horizontal expansion progresses:

| Policy | Scope | Priority | Dependencies | Description |
|--------|-------|----------|--------------|-------------|
| **Model Risk Policy** | Enterprise | HIGH | SS1/23 implementation | Enterprise model governance framework covering all risk domains (Market, Credit, Operational); Model tier classification; Development, validation, monitoring standards; Model inventory governance |
| **Economic Capital (ECAP) Policy** | Enterprise | MEDIUM | Domain ECAP methodologies complete | Enterprise ECAP framework beyond Market Risk; Aggregation methodology; Diversification benefit governance; ICAAP integration and Pillar 2 capital |
| **Environmental Risk Policy** | Enterprise | MEDIUM | Climate/ESG regulatory clarity | Physical and transition risk framework; TCFD alignment; Climate stress testing; ESG integration across risk domains |

**Rationale for Enterprise Scope**:
- **Model Risk Policy**: SS1/23 requires consistent model governance across all risk types. Market-specific model governance (VaR, pricing models) should be subsidiary to enterprise policy.
- **ECAP Policy**: Economic Capital spans Credit, Market, Operational risk with diversification benefits requiring enterprise-level governance. Market Risk ECAP methodology (MR-L6-002) provides the template.
- **Environmental Risk Policy**: Climate risk manifests across credit (transition risk in loan portfolios), market (carbon pricing), and operational (physical risk) domains.

### Phase 3: Data Lakehouse Implementation (Weeks 9-12)
**Objective**: Build Iceberg lakehouse with ICBCS reference data

#### Week 9-10: Lakehouse Infrastructure
- [ ] Set up Apache Iceberg catalog (local development with DuckDB)
- [ ] Define Parquet schemas for each ODS based on ICBCS data structures
- [ ] Create FpML-to-Parquet transformation scripts
- [ ] Load sample ICBCS data into TradeHub ODS

#### Week 11-12: ODS Population & Queries
- [ ] Populate Market Data ODS from ICBCS FMDM feeds
- [ ] Populate Risk ODS from ICBCS sensitivity data
- [ ] Build sample federated queries joining across ODSs
- [ ] Document data lineage from source to ODS

### Phase 4: Skills Integration (Weeks 13-16)
**Objective**: Connect taxonomy to Risk Agents skills

#### Week 13-14: Skills Mapping
- [x] Complete skills-to-taxonomy mapping matrix ✅
- [x] Identify skill gaps per taxonomy node ✅
- [ ] Prioritize new skill development

#### Week 15-16: AI Context Integration
- [ ] Build taxonomy index for agent context
- [ ] Implement taxonomy-aware RAG retrieval
- [ ] Test query routing using taxonomy structure

---

## 6. Skills Mapping Framework

### 6.1 Current Skills Inventory (12 skills)

| Skill | Primary Risk Domain | Taxonomy Layers Covered |
|-------|--------------------|-----------------------|
| **meeting-minutes** | Cross-cutting | L3 (Governance meetings) |
| **project-planner** | Cross-cutting | L4 (Change processes) |
| **status-reporter** | Cross-cutting | L5 (Project controls) |
| **stakeholder-analysis** | Cross-cutting | L3 (Governance) |
| **itc-template-filler** | Cross-Cutting | L3-L4 (IT governance) |
| **icc-business-case-filler** | Cross-Cutting | L3-L4-L5 (Change governance) |
| **process-documenter** | Cross-cutting | L4 (All processes) |
| **pillar-stress-generator** | Market Risk | L5-L6 (Stress scenarios, models) |
| **stress-scenario-suggester** | Market Risk | L2-L5 (Risk identification, scenarios) |
| **climate-scorecard-filler** | Sustainability Risk | L2-L5 (ESG assessment) |
| **regulatory-risk-researcher** | Regulatory Risk | L1 (Regulatory monitoring) |
| **regulatory-change-assessor** | Regulatory Risk | L1, L3-L7 (Impact assessment) |

### 6.2 Composable Skills Architecture

**Key Principle**: Skills at the lowest level are specific "tasks" that are **composable**. Each bank may structure these tasks differently to build their own processes according to how they operate.

#### Reference Process vs. Bank-Specific Process

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          COMPOSABLE SKILLS CONCEPT                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌────────────────────────────────────────────────────────────────────────┐    │
│   │                        REFERENCE PROCESS                               │    │
│   │                    (Best Practice Template)                            │    │
│   │                                                                        │    │
│   │   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐             │    │
│   │   │ Skill A │ →  │ Skill B │ →  │ Skill C │ →  │ Skill D │             │    │
│   │   └─────────┘    └─────────┘    └─────────┘    └─────────┘             │    │
│   │                                                                        │    │
│   └────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│   ┌────────────────────────────────────────────────────────────────────────┐    │
│   │                        BANK A PROCESS                                  │    │
│   │                    (Different Composition)                             │    │
│   │                                                                        │    │
│   │   ┌─────────┐    ┌─────────┐    ┌─────────┐                            │    │
│   │   │ Skill A │ →  │ Skill C │ →  │ Skill D │    (Skip B, same outcome)  │    │
│   │   └─────────┘    └─────────┘    └─────────┘                            │    │
│   │                                                                        │    │
│   └────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│   ┌────────────────────────────────────────────────────────────────────────┐    │
│   │                        BANK B PROCESS                                  │    │
│   │                    (Additional Steps)                                  │    │
│   │                                                                        │    │
│   │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │    │
│   │   │ Skill A │→ │ Skill B │→ │ Skill E │→ │ Skill C │→ │ Skill D │      │    │
│   │   └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │    │
│   │                                                                        │    │
│   └────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Example: Daily VaR Production Process

| Step | Reference Process | Bank A (Simplified) | Bank B (Enhanced) |
|------|-------------------|---------------------|-------------------|
| 1 | Extract trades | Extract trades | Extract trades |
| 2 | Validate data quality | Skip (automated) | Validate data quality |
| 3 | Calculate sensitivities | Calculate sensitivities | Calculate sensitivities |
| 4 | Run VaR engine | Run VaR engine | Run preliminary VaR |
| 5 | Check limits | Check limits | Manual review |
| 6 | Generate report | Generate report | Run final VaR |
| 7 | - | - | Check limits |
| 8 | - | - | Generate report |

#### Skill Design Principles

1. **Single Responsibility**: Each skill does ONE thing well
2. **Loose Coupling**: Skills don't depend on specific other skills
3. **Standard Interfaces**: Common input/output formats between skills
4. **Configurable**: Skills accept parameters to adjust behavior
5. **Composable**: Skills can be chained in different orders

### 6.3 Planned Skills by Risk Domain

Based on the Risk Agents website vision of "100+ modular capabilities across 9 risk domains":

| Risk Domain | Current Skills | Planned Skills (Examples) |
|-------------|----------------|---------------------------|
| **Market Risk** | 2 (pillar-stress, stress-suggester) | VaR analyzer, Limit monitor, Backtesting reviewer, FRTB calculator |
| **Credit Risk** | 1 (climate-scorecard) | Credit memo generator, Rating calculator, Concentration analyzer, IFRS9 ECL |
| **Operational Risk** | 2 (itc, icc templates) | RCSA facilitator, Incident reporter, KRI dashboard, Loss event analyzer |
| **Liquidity Risk** | 0 | LCR/NSFR calculator, Cash flow forecaster, Funding plan generator |
| **Model Risk** | 0 | Validation assistant, Back-test analyzer, Model inventory manager |
| **Climate/ESG Risk** | 1 (climate-scorecard) | TCFD reporter, Transition risk analyzer, Physical risk assessor |
| **Regulatory Risk** | 0 | Regulatory change tracker, Compliance checker, Capital calculator |
| **Strategic Risk** | 0 | M&A risk assessor, Competitor analyzer, Strategic scenario planner |
| **Change Management** | 4 (meetings, project, status, stakeholder) | RAID log manager, Benefits tracker, Test coordinator |

### 5.3 Skills-to-Taxonomy Mapping Matrix

Each skill will be mapped to specific taxonomy nodes:

```
Skill: pillar-stress-generator
├── L2: Market Risk → Stress Testing
├── L3: MLRC Committee, Market Risk Policy (Stress Testing section)
├── L4: Annual Stress Scenario Review Process
├── L5: Stress scenario library, Scenario controls, Validation requirements
├── L6: Stress scenario parameterization methodology
└── L7: Risk factor library (473 curves, 271 FX pairs, etc.)
```

This mapping enables:
1. **Context Loading**: When skill invoked, load relevant taxonomy nodes
2. **Gap Analysis**: Identify taxonomy nodes with no supporting skills
3. **Coverage Reporting**: Show skills coverage across risk domains

---

## 7. Technical Architecture

### 7.1 Taxonomy Data Structure

```yaml
# Example taxonomy node structure
node:
  id: "MR-L4-001"
  layer: 4
  name: "Daily VaR Production"
  domain: "Market Risk"
  parent: "MR-L3-002"  # Links to Market Risk Policy
  children:
    - "MR-L5-001"  # VaR Limits
    - "MR-L5-002"  # Backtesting Controls
  cross_refs:
    - "CR-L4-005"  # Credit exposure feed (input to CVA)
  skills:
    - "pillar-stress-generator"
    - "process-documenter"
  artefacts:
    - type: "process_map"
      path: "/docs/processes/daily-var-production.bpmn"
    - type: "procedure"
      path: "/docs/procedures/var-production-runbook.md"
  metadata:
    owner: "Market Risk Analytics"
    review_date: "2025-06-01"
    status: "active"
```

### 7.2 Directory Structure

```
/Users/gavinslater/projects/riskagent/
├── docs/
│   └── risk-taxonomy/
│       ├── 00-Risk-Taxonomy-Implementation-Plan.md  (this document)
│       ├── 01-Taxonomy-Schema.md                     (structure definition)
│       ├── L1-Requirements/
│       │   ├── regulatory-inventory.md
│       │   └── business-requirements.md
│       ├── L2-Risk-Types/
│       │   ├── risk-taxonomy.md                      (master document)
│       │   ├── market-risk.md
│       │   ├── credit-risk.md
│       │   └── ... (other risk domains)
│       ├── L3-Governance/
│       │   ├── policy-inventory.md
│       │   ├── committee-inventory.md
│       │   └── policies/
│       │       ├── market-risk-policy.md
│       │       └── credit-risk-policy.md
│       ├── L4-Processes/
│       │   ├── process-catalogue.md
│       │   └── processes/
│       │       ├── daily-var-production/
│       │       │   ├── process.md
│       │       │   └── process.bpmn
│       │       └── credit-limit-approval/
│       ├── L5-Controls/
│       │   ├── control-inventory.md
│       │   ├── kri-inventory.md
│       │   └── limit-frameworks/
│       ├── L6-Models/
│       │   ├── model-registry.md
│       │   └── methodologies/
│       │       ├── var-methodology.md
│       │       └── pfe-methodology.md
│       ├── L7-Data-Systems/
│       │   ├── system-inventory.md
│       │   ├── data-dictionary.md
│       │   ├── feed-inventory.md
│       │   └── architecture/
│       └── cross-cutting/
│           ├── products/
│           ├── reports/
│           └── change/
├── data/
│   └── reference-bank/
│       ├── market-data/
│       ├── positions/
│       ├── counterparties/
│       └── reports/
└── src/
    └── taxonomy/
        ├── schema.py                 (taxonomy node definitions)
        ├── loader.py                 (load taxonomy for agent context)
        └── navigator.py              (traverse taxonomy relationships)
```

### 7.3 Self-Documenting Infrastructure

Key principle: **Systems publish schemas; documentation auto-updates**

```
┌─────────────────┐     Schema Change    ┌──────────────────┐
│   Data System   │ ──────────────────→  │  Schema Registry │
│   (eg. Risk ODS)│                      │  (API endpoint)  │
└─────────────────┘                      └────────┬─────────┘
                                                  │
                                         Schema Published
                                                  │
                                                  ▼
                                        ┌─────────────────────┐
                                        │ Documentation Agent │
                                        │ (monitors registry) │
                                        └─────────┬───────────┘
                                                  │
                                         Updates Taxonomy
                                                  │
                                                  ▼
                                        ┌─────────────────────┐
                                        │   L7 Data Dictionary│
                                        │   (auto-updated)    │
                                        └─────────────────────┘
```

---

## 8. Policy Framework Guidelines

### 8.1 Policy-Framework Alignment Principle

**Key Requirement**: When policies are written, they must clearly demonstrate how they connect to and support the overall taxonomy framework.

#### Upward Linkage (Policy → Requirements)

Every policy should reference:
- **L1 Requirements**: Which regulatory requirements or business drivers mandate this policy
- **L2 Risk Types**: Which specific risk types the policy addresses
- **L3 Governance**: Which committee(s) approve and own the policy

#### Downward Linkage (Policy → Implementation)

Every policy should reference or describe:
- **L4 Processes**: Which operational processes implement the policy requirements
- **L5 Controls/Metrics**: Which controls, limits, and KRIs enforce the policy
- **L6 Models**: Which models/methodologies are used (if applicable)
- **L7 Data/Systems**: Which systems and data support policy implementation

### 8.2 Policy Document Template Structure

```markdown
# [Policy Name]

## 1. Policy Overview
- Purpose and scope
- **Regulatory Drivers** (L1 linkage)
- **Risk Types Addressed** (L2 linkage)

## 2. Governance
- **Approval Authority** (L3 committee)
- Policy owner and review cycle
- Escalation procedures

## 3. Policy Statements
- Core requirements
- Materiality thresholds
- Exception handling

## 4. Implementation Framework
- **Key Processes** (L4 linkage with references)
- Roles and responsibilities
- Timeline requirements

## 5. Controls and Metrics
- **Limits and Thresholds** (L5 linkage)
- **Key Risk Indicators** (L5 linkage)
- Monitoring frequency
- Breach procedures

## 6. Supporting Infrastructure
- **Models/Methodologies** (L6 linkage, if applicable)
- **Systems and Data** (L7 linkage)
- Reporting requirements

## 7. Related Documents
- Cross-references to other policies
- Related procedures and guidelines
```

### 8.3 Example: Market Risk Policy Linkages

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    MARKET RISK POLICY - TAXONOMY LINKAGES                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │ UPWARD LINKAGE (Why this policy exists)                                  │  │
│   ├──────────────────────────────────────────────────────────────────────────┤  │
│   │                                                                          │  │
│   │  L1: CRR Art. 325-377 (IMA requirements)                                 │  │
│   │      PRA SS13/13 (Market risk management)                                │  │
│   │      BCBS d352 (FRTB)                                                    │  │
│   │                                                                          │  │
│   │  L2: MR-L2-001 (General Market Risk)                                     │  │
│   │      MR-L2-002 (Interest Rate Risk)                                      │  │
│   │      MR-L2-003 (FX Risk)                                                 │  │
│   │      ... etc.                                                            │  │
│   │                                                                          │  │
│   │  L3: MLRC (Market & Liquidity Risk Committee)                            │  │
│   │      RMC (Risk Management Committee - escalation)                        │  │
│   │                                                                          │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │          MARKET RISK POLICY (L3: MR-L3-001)                              │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│   ┌──────────────────────────────────────────────────────────────────────────┐  │
│   │ DOWNWARD LINKAGE (How this policy is implemented)                        │  │
│   ├──────────────────────────────────────────────────────────────────────────┤  │
│   │                                                                          │  │
│   │  L4: Daily VaR Production Process (MR-L4-001)                            │  │
│   │      Backtesting Process (MR-L4-002)                                     │  │
│   │      Stress Testing Process (MR-L4-003)                                  │  │
│   │      New Product Approval (MR-L4-004)                                    │  │
│   │                                                                          │  │
│   │  L5: VaR Limits (desk/entity) (MR-L5-001)                                │  │
│   │      Stress Limits (MR-L5-002)                                           │  │
│   │      Greeks Limits (MR-L5-003)                                           │  │
│   │      Backtesting Exception Limits (MR-L5-004)                            │  │
│   │                                                                          │  │
│   │  L6: Historical Simulation VaR Model (MR-L6-001)                         │  │
│   │      Stress VaR Model (MR-L6-002)                                        │  │
│   │      IRC Model (MR-L6-003)                                               │  │
│   │                                                                          │  │
│   │  L7: Market Risk System (Murex/FMDM)                                     │  │
│   │      Market Data ODS, TradeHub ODS, Risk ODS                             │  │
│   │      Daily VaR Report, MLRC Pack                                         │  │
│   │                                                                          │  │
│   └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 8.4 Benefits of Framework-Aligned Policies

| Benefit | Description |
|---------|-------------|
| **Audit Trail** | Clear traceability from regulation to implementation |
| **Gap Analysis** | Easy identification of missing controls or processes |
| **Change Impact** | Understand implications when policies change |
| **Onboarding** | New staff can navigate from policy to operational detail |
| **Regulatory Response** | Quickly demonstrate control framework to regulators |

---

## 9. Deliverables & Artefacts

### Phase 1 Deliverables

| Deliverable | Description | Format |
|-------------|-------------|--------|
| **Taxonomy Schema** | YAML schema defining node structure | `.yaml` |
| **Risk Type Definitions** | Complete L2 for all 9 risk domains | `.md` |
| **Market Risk Vertical** | L3-L7 complete for VaR production | `.md`, `.bpmn` |
| **Skills Mapping Matrix** | Current skills mapped to taxonomy | `.md` |

### Phase 2 Deliverables

| Deliverable | Description | Format |
|-------------|-------------|--------|
| **Credit Risk Vertical** | L3-L7 complete for limit management | `.md`, `.bpmn` |
| **Governance Inventory** | All committees, policies across domains | `.md` |
| **Process Catalogue** | Prioritized list of all risk processes | `.md` |

### Phase 3 Deliverables

| Deliverable | Description | Format |
|-------------|-------------|--------|
| **Iceberg Catalog Setup** | Local development catalog with DuckDB | Config files |
| **ODS Parquet Schemas** | Schema definitions for each ODS | `.parquet`, `.py` |
| **FpML Transformation Scripts** | XML to Parquet converters | `.py` |
| **Sample ODS Data** | ICBCS reference data loaded | `.parquet` |
| **Federated Query Examples** | Cross-ODS join examples | `.sql`, `.py` |
| **Data Lineage Documentation** | Source to ODS traceability | `.md` |

### Phase 4 Deliverables

| Deliverable | Description | Format |
|-------------|-------------|--------|
| **Skills Gap Analysis** | Taxonomy nodes without skills | `.md` |
| **Taxonomy Index** | Optimized for agent context loading | `.json` |
| **Query Routing Tests** | Test cases for taxonomy-aware retrieval | `.py` |

---

## 10. Success Metrics

### 10.1 Completeness Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Risk domain coverage | 100% of 9 domains at L2 | Count of populated L2 nodes |
| Vertical slice depth | 2 complete slices L1-L7 | Manual review of linkage |
| Skills mapping | 100% of current skills mapped | Matrix completion rate |

### 10.2 Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Linkage integrity | 0 orphan nodes | Automated validation script |
| Artefact freshness | 100% dated within 6 months | Review date < today - 180 days |
| Cross-reference accuracy | 0 broken links | Link validation script |

### 10.3 Usability Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Agent context accuracy | 80% relevant context loaded | Test query results |
| Human navigation time | <3 clicks to target | User testing |
| Onboarding effectiveness | 50% faster with taxonomy | Comparative timing |

---

## Appendix A: Reference Materials Used

### ICBCS Bank Materials
- Risk_Taxonomy.md - Risk type definitions and classifications
- Risk_Taxonomy_Framework_Master.md - Framework structure and artefact inventory
- Taxonomy_Framework_Artefacts.md - Detailed artefact specifications
- Risk_Knowledge_Management_Platform_Plan_Revised.md - Implementation approach

### Risk Agents Platform
- Skills Guide (docs/06-skills-guide.md) - Current skills documentation
- Risk Agents website (https://risk-agents.com/) - Platform vision

---

## Appendix B: Next Steps

### Immediate Actions (This Week)

1. **Create taxonomy directory structure** in `/docs/risk-taxonomy/`
2. **Build L2 Risk Types** using ICBCS Risk_Taxonomy.md as template but generalizing
3. **Design taxonomy schema** in YAML for node definitions
4. **Start Market Risk vertical slice** with VaR production process

### Decision Points Required

1. **Reference Bank Naming**: Confirm "Meridian Global Bank" or alternative
2. **Synthetic Data Scope**: Confirm 500 trades, 100 counterparties sufficient
3. **Phase Prioritization**: Confirm Market Risk first, Credit Risk second
4. **Skills Development Priority**: Which new skills to build first based on gaps

---

*Document Control*
- **Created**: 2025-12-11
- **Author**: Risk Agents Team
- **Classification**: Internal
- **Next Review**: 2025-12-25 (Phase 1 checkpoint)
