---
# Process Metadata
process_id: FIN-L4-001
process_name: Hierarchy Management
version: 1.1
effective_date: 2025-01-15
next_review_date: 2026-01-15
owner: Head of Finance Operations
approving_committee: Finance Operating Committee

# Taxonomy Linkages
parent_process: None  # Finance-owned foundational process
l1_requirements:
  - REQ-L1-001  # CRR (Trading Book Boundary)
  - REQ-L1-003  # FRTB (Enhanced Boundary)
  - REQ-L1-022  # BCBS 239 (Data Governance)
l2_risk_types:
  - MR-L2-001   # Market Risk (consumer)
l3_governance:
  - MR-L3-001   # Market Risk Policy
  - FIN-L3-001  # Finance Policy
l7_systems:
  - SYS-FIN-001 # Finance Master Data
  - SYS-MR-011  # Hierarchy ODS
---

# Hierarchy Management Process

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Process ID** | FIN-L4-001 |
| **Version** | 1.0 |
| **Effective Date** | 15 January 2025 |
| **Owner** | Head of Finance Operations |
| **Approving Committee** | Finance Operating Committee |

---

## 1. Purpose

The Hierarchy Management process establishes and maintains the **book hierarchy structure** that is foundational for:

- **Balance sheet reporting** - Legal entity financial statements and consolidation
- **P&L attribution** - Revenue and cost allocation by desk, business, and division
- **Regulatory reporting** - Trading book boundary for market risk capital
- **Risk aggregation** - VaR calculation and limit monitoring
- **Cost centre management** - Budget allocation and expense attribution

This process is **owned by Finance** as the "keeper of the hierarchy" because the structure serves multiple enterprise purposes beyond risk management. Risk is a key **consumer** of the hierarchy and adds risk-specific attributes.

---

## 2. Scope

### 2.1 Hierarchy Levels

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           BOOK HIERARCHY STRUCTURE                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  Level 1: ENTERPRISE                                                                    │
│  └── Meridian Global Bank Group                                                         │
│                                                                                         │
│  Level 2: LEGAL ENTITY                                                                  │
│  ├── Meridian Bank UK (London)                                                          │
│  ├── Meridian Securities Asia (Hong Kong)                                               │
│  └── Meridian Capital Markets (New York)                                                │
│                                                                                         │
│  Level 3: DIVISION                                                                      │
│  ├── Global Markets                                                                     │
│  ├── Treasury                                                                           │
│  └── Principal Investments                                                              │
│                                                                                         │
│  Level 4: BUSINESS UNIT                                                                 │
│  ├── Rates Trading                                                                      │
│  ├── FX Trading                                                                         │
│  ├── Credit Trading                                                                     │
│  ├── Equities                                                                           │
│  └── Commodities                                                                        │
│                                                                                         │
│  Level 5: DESK                                                                          │
│  ├── EUR Rates London                                                                   │
│  ├── USD Rates NY                                                                       │
│  ├── G10 FX London                                                                      │
│  ├── Asia FX HK                                                                         │
│  └── ... (50+ desks)                                                                    │
│                                                                                         │
│  Level 6: BOOK (Lowest named level)                                                     │
│  └── Individual trading books (e.g., EUR-RATES-LON-01, G10FX-LON-MM-01)                 │
│                                                                                         │
│  Level 7: POSITION / TRADE (Transaction level)                                          │
│  └── Individual positions within books                                                  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Hierarchy Attributes

| Attribute | Owner | Description | Used By |
|-----------|-------|-------------|---------|
| **Book ID** | Finance | Unique identifier for each book | All |
| **Book Name** | Finance | Descriptive name | All |
| **Legal Entity** | Finance | Owning legal entity | Finance, Risk, Regulatory |
| **Division** | Finance | Business division | Finance, Management |
| **Business Unit** | Finance | Business unit within division | Finance, Management |
| **Desk** | Finance | Trading desk | Finance, Risk, Front Office |
| **Cost Centre** | Finance | Cost allocation code | Finance, HR |
| **Trading Book Flag** | Risk (with Finance) | Trading vs. Non-Trading classification | Risk, Regulatory |
| **VaR Limit Level** | Risk | Level at which VaR limits apply | Risk |
| **Reporting Tier** | Risk | Desk reporting classification | Risk |

### 2.3 Consumers of the Hierarchy

| Consumer | Use Case | Key Attributes Required |
|----------|----------|------------------------|
| **Finance** | P&L reporting, balance sheet, consolidation | All structure attributes, cost centres |
| **Market Risk** | VaR calculation, limit monitoring | Trading book flag, VaR limit level |
| **Regulatory Reporting** | Trading book capital, COREP | Trading book flag, legal entity |
| **Front Office** | Position booking, P&L attribution | Book ID, desk |
| **HR** | Headcount allocation | Cost centre |
| **Internal Audit** | Control testing | All |

---

## 3. Process Flow

### 3.1 Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     HIERARCHY MANAGEMENT PROCESS FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │                         1. HIERARCHY CHANGE REQUEST                                  │
    │                                                                                      │
    │  Triggers:                                                                           │
    │  • New trading desk setup (see Desk Mandate Management MR-L4-012)                    │
    │  • New book creation                                                                 │
    │  • Desk/book closure                                                                 │
    │  • Reorganisation (desk moves between business units)                                │
    │  • Legal entity restructuring                                                        │
    │                                                                                      │
    │  Requestor: Front Office, Business Management, or Finance                            │
    │                                                                                      │
    │  Note: New desk setup requires approved Desk Mandate (MR-L4-012) including           │
    │  designated dealers, risk limits, and MLRC approval before hierarchy setup.          │
    └───────────────────────────────────────────────────────────────────────────┬──────────┘
                                                                                │
                                                                                ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │                         2. FINANCE REVIEW AND SETUP                                  │
    │                                                                                      │
    │  Finance Operations:                                                                 │
    │  • Validate business rationale                                                       │
    │  • Assign book ID (following naming convention)                                      │
    │  • Map to legal entity, division, business unit, desk                                │
    │  • Assign cost centre                                                                │
    │  • Configure P&L attribution rules                                                   │
    │                                                                                      │
    │  Approval: Head of Finance Operations                                                │
    └───────────────────────────────────────────────────────────────────────────┬──────────┘
                                                                                │
                                                                                ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │                         3. RISK ATTRIBUTE ENRICHMENT                                 │
    │                                                                                      │
    │  Risk (RAV/RMA):                                                                     │
    │  • Determine trading book / non-trading book classification                          │
    │  • Assign VaR limit level                                                            │
    │  • Set reporting tier                                                                │
    │  • Validate risk factor mappings available                                           │
    │                                                                                      │
    │  Approval (Trading Book): MLRC                                                       │
    └───────────────────────────────────────────────────────────────────────────┬──────────┘
                                                                                │
                                                                                ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │                         4. SYSTEM UPDATE                                             │
    │                                                                                      │
    │  Data Operations:                                                                    │
    │  • Update Finance Master Data system                                                 │
    │  • Propagate to Hierarchy ODS                                                        │
    │  • Update downstream systems (Trading, Risk Engine, Reporting)                       │
    │  • Effective date management                                                         │
    │                                                                                      │
    │  Validation: Reconciliation between systems                                          │
    └───────────────────────────────────────────────────────────────────────────┬──────────┘
                                                                                │
                                                                                ▼
    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │                         5. GO-LIVE AND MONITORING                                    │
    │                                                                                      │
    │  • Book available for trading (if new)                                               │
    │  • First day validation of P&L attribution                                           │
    │  • VaR calculation validation (if trading book)                                      │
    │  • Ongoing monitoring for correct usage                                              │
    └──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Trading Book Boundary

### 4.1 Classification Criteria

For regulatory capital purposes, positions must be correctly classified as **Trading Book** or **Non-Trading Book (Banking Book)**:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     TRADING BOOK BOUNDARY CRITERIA                                       │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  TRADING BOOK (In scope for IMA VaR / Market Risk Capital)                               │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│                                                                                          │
│  Positions must meet ALL of the following criteria:                                      │
│                                                                                          │
│  ✓ TRADING INTENT                                                                        │
│    • Held for short-term resale                                                          │
│    • Held to benefit from actual or expected price movements                             │
│    • Held to lock in arbitrage profits                                                   │
│                                                                                          │
│  ✓ DAILY MARK-TO-MARKET                                                                  │
│    • Valued daily using observable market prices                                         │
│    • Or marked-to-model with regular validation                                          │
│                                                                                          │
│  ✓ ACTIVE MANAGEMENT                                                                     │
│    • Subject to position limits                                                          │
│    • Managed by traders with P&L mandates                                                │
│    • Regular trading activity expected                                                   │
│                                                                                          │
│  ✓ APPROPRIATE INFRASTRUCTURE                                                            │
│    • Risk limits in place                                                                │
│    • P&L attribution operational                                                         │
│    • Valuation controls established                                                      │
│                                                                                          │
│  ──────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                          │
│  TYPICAL TRADING BOOK POSITIONS:                                                         │
│  • Market-making inventory                                                               │
│  • Proprietary trading positions                                                         │
│  • Hedges of other trading book positions                                                │
│  • Client facilitation positions                                                         │
│  • Underwriting commitments (short-term)                                                 │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     NON-TRADING BOOK / BANKING BOOK                                      │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  Positions held for purposes OTHER than trading:                                         │
│                                                                                          │
│  ✗ Loans and advances (credit risk capital)                                              │
│  ✗ Investment securities held-to-collect (credit risk capital)                           │
│  ✗ Structural FX positions                                                               │
│  ✗ IRRBB hedges (Interest Rate Risk in Banking Book)                                     │
│  ✗ CVA hedges (separate regulatory treatment)                                            │
│  ✗ Equity investments in subsidiaries                                                    │
│  ✗ Pension fund assets                                                                   │
│                                                                                          │
│  Note: Banking book subject to Credit Risk and IRRBB capital frameworks                  │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Classification Governance

| Activity | Owner | Approver | Timing |
|----------|-------|----------|--------|
| Initial trading book classification | Finance + Risk | MLRC | New book setup |
| Classification change request | Business + Risk | MLRC | As needed (rare) |
| Annual boundary review | Risk (RAV) | RMA | Annual |
| Trading book boundary audit | Internal Audit | Audit Committee | Annual |

### 4.3 Internal Risk Transfers

When positions are transferred between trading book and banking book:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     INTERNAL RISK TRANSFER RULES                                         │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  BANKING BOOK → TRADING BOOK                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│  • Must meet all trading book criteria                                                   │
│  • MLRC pre-approval required                                                            │
│  • Documented business rationale                                                         │
│  • Effective date for capital treatment                                                  │
│                                                                                          │
│  TRADING BOOK → BANKING BOOK                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│  • Generally PROHIBITED (one-way boundary)                                               │
│  • Only permitted in exceptional circumstances:                                          │
│    - Genuine change in business strategy                                                 │
│    - Market conditions make trading impossible                                           │
│  • Requires CRO approval + regulatory notification                                       │
│  • Any P&L impact recognised at transfer                                                 │
│                                                                                          │
│  INTERNAL HEDGES (Trading Book ↔ Banking Book)                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│  • Hedges of banking book positions executed via trading book                            │
│  • Trading book leg: Subject to market risk capital                                      │
│  • Banking book leg: IRRBB treatment                                                     │
│  • Must be documented and approved                                                       │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Finance Responsibilities

### 5.1 Book Setup

| Task | Description | SLA |
|------|-------------|-----|
| **New book request review** | Validate business need and structure | 2 business days |
| **Book ID assignment** | Assign unique ID per naming convention | Same day |
| **Hierarchy mapping** | Map to entity, division, BU, desk | 1 business day |
| **Cost centre assignment** | Assign appropriate cost centre | 1 business day |
| **System configuration** | Update Finance Master Data | 1 business day |
| **Go-live** | Book available for trading | T+5 from request |

### 5.2 Book Naming Convention

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     BOOK NAMING CONVENTION                                               │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  FORMAT: [ASSET]-[PRODUCT]-[LOCATION]-[SEQUENCE]                                         │
│                                                                                          │
│  EXAMPLES:                                                                               │
│  • EUR-RATES-LON-01      EUR Rates, London, Book 01                                      │
│  • USD-RATES-NY-01       USD Rates, New York, Book 01                                    │
│  • G10FX-SPOT-LON-MM-01  G10 FX Spot, London, Market Making, Book 01                     │
│  • EMFX-FWD-HK-01        EM FX Forwards, Hong Kong, Book 01                              │
│  • CREDIT-CDS-LON-IG-01  Credit CDS, London, Investment Grade, Book 01                   │
│                                                                                          │
│  ASSET CODES:         PRODUCT CODES:       LOCATION CODES:                               │
│  EUR, USD, GBP...     RATES, SPOT, FWD     LON, NY, HK, SG                               │
│  G10FX, EMFX          CDS, BOND, OPT       TKY, SYD                                      │
│  CREDIT, EQ           STRUCT, EXOT                                                       │
│  CMDTY                                                                                   │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Cost Centre Management

Each book is associated with a cost centre for:
- Expense allocation
- Budget tracking
- Headcount attribution
- Profitability analysis

| Cost Centre Level | Example | Typical Granularity |
|-------------------|---------|---------------------|
| Division | GM-001 | Global Markets |
| Business Unit | GM-RATES-001 | Rates Trading |
| Desk | GM-RATES-EUR-001 | EUR Rates London |

---

## 6. Risk Responsibilities

### 6.1 Trading Book Classification

Risk (RAV/RMA) is responsible for:

| Task | Description | Timing |
|------|-------------|--------|
| **Classification determination** | Assess trading book criteria | New book setup |
| **MLRC submission** | Prepare paper for trading book designation | Before go-live |
| **Ongoing monitoring** | Review books for continued trading intent | Monthly |
| **Boundary review** | Annual comprehensive review | Annual |

### 6.2 Risk Attribute Assignment

| Attribute | Description | Owner |
|-----------|-------------|-------|
| **Trading Book Flag** | Y/N designation for IMA VaR scope | RMA (MLRC approval) |
| **VaR Limit Level** | Hierarchy level for limit application | Market Risk |
| **Reporting Tier** | Classification for reporting granularity | RAV |
| **Risk Factor Group** | Primary risk factor for analytics | RMA |

### 6.3 Trading Book Monitoring

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     TRADING BOOK BOUNDARY MONITORING                                     │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  MONTHLY CHECKS (RAV):                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│  • Trading activity review (books with low/no turnover flagged)                          │
│  • Age analysis of positions (positions held > 90 days reviewed)                         │
│  • P&L volatility check (low volatility may indicate non-trading intent)                 │
│                                                                                          │
│  QUARTERLY CHECKS (RMA):                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│  • Business strategy alignment (confirm trading intent still valid)                      │
│  • New product review (ensure appropriate classification)                                │
│  • Regulatory change impact assessment                                                   │
│                                                                                          │
│  ANNUAL REVIEW (Internal Audit):                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│  • Full trading book boundary audit                                                      │
│  • Sample testing of classification decisions                                            │
│  • Control effectiveness assessment                                                      │
│  • Regulatory compliance confirmation                                                    │
│                                                                                          │
│  TRIGGERS FOR IMMEDIATE REVIEW:                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────   │
│  • Book inactive for > 30 days                                                           │
│  • Significant strategy change announced                                                 │
│  • Regulatory query on classification                                                    │
│  • Internal Audit finding                                                                │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Data Flow

### 7.1 System Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                     HIERARCHY DATA FLOW                                                  │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │   FINANCE MASTER DATA (Golden Source)                                               │ │
│  │   SYS-FIN-001                                                                       │ │
│  │                                                                                     │ │
│  │   Maintains:                                                                        │ │
│  │   • Book definitions and IDs                                                        │ │
│  │   • Legal entity structure                                                          │ │
│  │   • Division / Business Unit / Desk hierarchy                                       │ │
│  │   • Cost centre mappings                                                            │ │
│  │   • Effective dates and history                                                     │ │
│  └───────────────────────────────────────────────┬─────────────────────────────────────┘ │
│                                                  │                                       │
│                                                  │ Daily Extract                         │
│                                                  ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │   HIERARCHY ODS (Operational Data Store)                                            │ │
│  │   SYS-MR-011                                                                        │ │
│  │                                                                                     │ │
│  │   Combines:                                                                         │ │
│  │   • Finance hierarchy structure                                                     │ │
│  │   • Risk attributes (trading book flag, VaR limit level)                            │ │
│  │   • Position → Book mappings (from Trading Systems)                                 │ │
│  │   • As-of date versioning                                                           │ │
│  └───────────────────────────────────────────────┬─────────────────────────────────────┘ │
│                                                  │                                       │
│                          ┌───────────────────────┼───────────────────────┐               │
│                          │                       │                       │               │
│                          ▼                       ▼                       ▼               │
│  ┌─────────────────────────────┐ ┌─────────────────────────────┐ ┌─────────────────────┐ │
│  │   RISK ENGINE               │ │   FINANCE REPORTING         │ │   REGULATORY        │ │
│  │   SYS-MR-003                │ │   SYS-FIN-002               │ │   REPORTING         │ │
│  │                             │ │                             │ │   SYS-REG-001       │ │
│  │   Uses:                     │ │   Uses:                     │ │                     │ │
│  │   • Trading book scope      │ │   • P&L aggregation         │ │   Uses:             │ │
│  │   • Aggregation path        │ │   • Balance sheet           │ │   • Trading book    │ │
│  │   • VaR limit levels        │ │   • Cost allocation         │ │     boundary        │ │
│  └─────────────────────────────┘ └─────────────────────────────┘ └─────────────────────┘ │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Data Quality Controls

| Control | Description | Frequency | Owner |
|---------|-------------|-----------|-------|
| **Reconciliation** | Finance Master ↔ Hierarchy ODS | Daily | Data Ops |
| **Orphan check** | Positions without valid book mapping | Daily | Data Ops |
| **Completeness** | All books have required attributes | Daily | Data Ops |
| **Consistency** | Trading book flag aligned across systems | Daily | RAV |

---

## 8. Controls

| Control ID | Control | Type | Owner |
|------------|---------|------|-------|
| HM-C01 | All new books require documented business rationale | Preventive | Finance |
| HM-C02 | Book IDs follow naming convention | Preventive | Finance |
| HM-C03 | Trading book designation requires MLRC approval | Preventive | Risk |
| HM-C04 | Hierarchy changes require Head of Finance Ops approval | Preventive | Finance |
| HM-C05 | Daily reconciliation Finance Master ↔ Hierarchy ODS | Detective | Data Ops |
| HM-C06 | Monthly trading book boundary monitoring | Detective | RAV |
| HM-C07 | Annual trading book boundary audit | Detective | Internal Audit |
| HM-C08 | Position transfers TB ↔ BB require MLRC pre-approval | Preventive | Risk |
| HM-C09 | Book closure requires sign-off that no open positions | Preventive | Finance |
| HM-C10 | Cost centre changes require Finance approval | Preventive | Finance |

---

## 9. Service Levels

| Metric | Target | Threshold | Escalation |
|--------|--------|-----------|------------|
| New book setup (standard) | 5 business days | 7 business days | Head of Finance Ops |
| New book setup (urgent) | 2 business days | 3 business days | Head of Finance Ops |
| Hierarchy ODS refresh | Daily by 06:00 GMT | 07:00 GMT | Data Ops Manager |
| Reconciliation completion | Daily by 08:00 GMT | 09:00 GMT | Data Ops Manager |
| Trading book classification | Before book go-live | - | RMA |

---

## 10. Exception Handling

### 10.1 Hierarchy Discrepancies

| Issue | Resolution | Escalation |
|-------|------------|------------|
| **Position without valid book** | Assign to suspense book; investigate | Data Ops → Finance |
| **Book without cost centre** | Assign default cost centre; flag | Finance Ops |
| **Trading book flag mismatch** | Investigate; align to MLRC decision | RAV → RMA |
| **Duplicate book IDs** | Block; investigate source system | Data Ops → IT |

### 10.2 Urgent Changes

For urgent hierarchy changes (e.g., regulatory deadline, new business opportunity):

| Scenario | Approval | SLA |
|----------|----------|-----|
| Emergency book setup | Head of Finance Ops + verbal MLRC | Same day |
| Critical hierarchy fix | Data Ops Manager | 4 hours |
| Regulatory-driven change | CFO | As required |

---

## 11. Regulatory Requirements

| Regulation | Requirement | How Addressed |
|------------|-------------|---------------|
| **CRR Article 104** | Trading book definition and boundary | Trading book classification process |
| **CRR Article 104a-c** | Internal risk transfers; reclassification | Transfer approval process |
| **FRTB** | Enhanced boundary; presumptive list | Annual boundary review |
| **PRA SS13/13** | Trading book policy and procedures | This process document |
| **Basel BCBS 239** | Data governance; accuracy | Daily reconciliation controls |
| **IFRS 9** | Classification for accounting | Alignment with Finance classification |

---

## 12. Related Documents

| Document | Relationship |
|----------|--------------|
| [Market Risk Process Orchestration](./market-risk-process-orchestration.md) | Consumer of hierarchy for VaR |
| [Risk Engine Calculation](./risk-engine-calculation.md) | Consumer of hierarchy for aggregation |
| [Desk Mandate Management](./desk-mandate-management.md) | Defines desk mandates and designated dealers (CRR 104b) |
| [VaR Limit Framework](../L3-Governance/policies/var-limit-framework.md) | Defines limit levels in hierarchy |
| [Market Risk Policy](../L3-Governance/policies/market-risk-policy.md) | Governance framework |
| Finance Policy | Finance hierarchy governance |

---

## 13. Document Control

### 13.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-15 | Initial version | Finance Operating Committee |
| 1.1 | 2025-01-16 | Added cross-reference to Desk Mandate Management (MR-L4-012) | Finance Operating Committee |

---

*End of Document*
