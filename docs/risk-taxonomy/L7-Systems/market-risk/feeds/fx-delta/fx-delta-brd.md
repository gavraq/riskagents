# FX Delta Sensitivities - Business Requirements Document

**Meridian Global Bank - Market Risk Technology**

| Document Control | |
|-----------------|---|
| **Document ID** | FXD-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 13 January 2025 |
| **Owner** | Market Risk Technology |

---

## 1. Executive Summary

### 1.1 Purpose

This Business Requirements Document defines the functional and non-functional requirements for the FX Delta sensitivity feed from Murex to downstream market risk systems. The feed provides foreign exchange spot delta risk exposures for linear (non-option) FX products.

### 1.2 Business Context

FX Delta risk is a fundamental component of market risk for institutions with multi-currency exposures:

- **FX Trading Desks**: Position management and hedging decisions
- **Treasury**: Currency exposure management
- **ALM**: Structural FX risk measurement
- **Risk Management**: Aggregate FX exposure reporting and limits

### 1.3 Scope

| In Scope | Out of Scope |
|----------|--------------|
| FX spot delta sensitivities | FX Vega (option volatility) |
| Linear FX products | FX option Greeks (gamma, theta) |
| Structured bonds with FX exposure | Equity/Commodity delta |
| Trade-level granularity | IR sensitivities on FX products |
| Regional processing (LN, HK, NY, SP) | Intraday positions |

---

## 2. Business Requirements

### 2.1 Functional Requirements

#### BR-FXD-001: FX Delta Calculation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXD-001 |
| **Title** | FX Spot Delta Calculation |
| **Priority** | Critical |
| **Description** | The system shall calculate FX spot delta representing the PL variation for spot price movements |
| **Delta Type** | Spot Delta Hedge (dHedge@spot/dS) |
| **Acceptance Criteria** | Delta expressed in USD equivalent |

#### BR-FXD-002: Currency Pair Representation

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXD-002 |
| **Title** | FX Quotation Mode |
| **Priority** | Critical |
| **Description** | The feed shall express FX delta against standardized currency pairs using market convention |
| **Format** | CCY1-CCY2 (e.g., EUR-USD, GBP-USD) |
| **Reference** | TBL_FX_CNT_REP for standard quotation modes |

#### BR-FXD-003: Structured Bond Coverage

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXD-003 |
| **Title** | Structured Bond FX Delta |
| **Priority** | High |
| **Description** | The feed shall include FX delta from structured bonds with embedded FX exposure |
| **Product Types** | CLN Leveraged, Deposit Note, FX Linked Note, FX Passthrough, Passthrough |
| **Calculation** | Use Past and Future Flows if non-zero, else use FX delta from risk engine |

#### BR-FXD-004: Non-Structured Product Coverage

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXD-004 |
| **Title** | Linear FX Product Coverage |
| **Priority** | Critical |
| **Description** | The feed shall include all linear FX products |
| **Product Types** | FX Spots, Forwards, NDFs, Cross-Currency Swaps, FX Swaps |
| **Exclusions** | FX Options (covered by FX Vega feed) |

#### BR-FXD-005: Trade Status Handling

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXD-005 |
| **Title** | Live and Dead Deal Processing |
| **Priority** | High |
| **Description** | The feed shall handle both live and dead/purged deals appropriately |
| **Live Deals** | Full trade-level detail with individual trade numbers |
| **Dead Deals** | Aggregated by portfolio/currency pair with Trade Number = 0 |
| **Business Rationale** | Dead deal aggregation reduces file size while preserving total exposure |

#### BR-FXD-006: Regional Processing

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXD-006 |
| **Title** | Multi-Region Support |
| **Priority** | High |
| **Description** | The feed shall be produced separately for each trading region |
| **Regions** | London (LN), Hong Kong (HK), New York (NY), Sao Paulo (SP) |

#### BR-FXD-007: Entity Exclusion

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXD-007 |
| **Title** | SBSA Entity Exclusion |
| **Priority** | Medium |
| **Description** | Trades booked under SBSA legal entity shall be excluded from the feed |
| **Implementation** | Filter at extraction level |

### 2.2 Non-Functional Requirements

#### BR-FXD-NFR-001: Timeliness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXD-NFR-001 |
| **Title** | Data Delivery SLA |
| **Priority** | Critical |
| **Description** | Feed must be delivered by 05:30 GMT (T+1) for London region |
| **Measurement** | 95% of deliveries within SLA over rolling 30-day period |

#### BR-FXD-NFR-002: Completeness

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXD-NFR-002 |
| **Title** | Data Completeness |
| **Priority** | Critical |
| **Description** | All live FX positions must have delta values |
| **Tolerance** | <0.1% missing delta records for live trades |

#### BR-FXD-NFR-003: Accuracy

| Requirement | Description |
|-------------|-------------|
| **ID** | BR-FXD-NFR-003 |
| **Title** | Calculation Accuracy |
| **Priority** | Critical |
| **Description** | Delta values must match front office system within tolerance |
| **Tolerance** | ±0.01% for Delta values in USD |

---

## 3. Data Requirements

### 3.1 Input Data

| Source | Data Element | Description |
|--------|--------------|-------------|
| Murex Trade Repository | Trade attributes | Trade number, portfolio, status, legal entity |
| Murex Valuation | FX delta values | Spot and discounted delta per currency pair |
| Market Data | FX spot rates | For USD equivalent conversion |
| Reference Data | TBL_FX_CNT_REP | FX contract definitions and quotation modes |

### 3.2 Output Data

| Field | Type | Length | Description |
|-------|------|--------|-------------|
| TRADENUMBER | Numeric | 10 | Trade ID (0 for dead deals) |
| PORTFOLIO | VarChar | 16 | Trading book code |
| CURRENCY_PAIR | VarChar | 16 | FX quotation (e.g., EUR-USD) |
| FXDELTA | Numeric | 20 | FX delta in USD |
| FXDELTA_CURR | VarChar | 4 | Currency of delta (USD) |
| FXDELTA_ZAR | Numeric | 20 | FX delta in ZAR (deprecated) |
| FXDELTA_CURR2 | VarChar | 4 | ZAR (deprecated) |
| ZAR_PROCESSING | VarChar | 4 | JBSBSA flag (deprecated) |

### 3.3 Data Quality Rules

| Rule ID | Field | Rule | Action |
|---------|-------|------|--------|
| DQ-FXD-001 | TRADENUMBER | Must be numeric | Reject |
| DQ-FXD-002 | PORTFOLIO | Must not be null | Reject |
| DQ-FXD-003 | CURRENCY_PAIR | Must be valid CCY1-CCY2 format | Warning |
| DQ-FXD-004 | FXDELTA | Must be numeric | Reject |
| DQ-FXD-005 | Legal Entity | Must not be SBSA | Exclude |

---

## 4. Business Rules

### 4.1 FX Delta Source Selection (Structured Bonds)

| Rule ID | Condition | Delta Source |
|---------|-----------|--------------|
| BR-STB-001 | STB trade with non-zero Past_and_Future_Flows | Past_and_Future_Flows |
| BR-STB-002 | STB trade with zero Past_and_Future_Flows | FX_delta_STB (risk engine) |
| BR-STB-003 | Non-STB trade | FXDELTA from FXDELTAPOSRPT |

### 4.2 Currency Pair Construction (Structured Bonds)

| Rule ID | Product Type | Currency Pair Logic |
|---------|--------------|---------------------|
| BR-CCY-001 | FX Linked Note | FLOW_CURR - UNIT |
| BR-CCY-002 | Other STB (CURRENCY = FLOW_CURR) | CURRENCY - UNIT |
| BR-CCY-003 | Other STB (CURRENCY ≠ FLOW_CURR) | CURRENCY - FLOW_CURR |
| BR-CCY-004 | Non-STB | FXQUOT from simulation view |

### 4.3 Trade Status Rules

| Rule ID | Status | Treatment |
|---------|--------|-----------|
| BR-STS-001 | LIVE, MKT_OP | Full trade-level detail |
| BR-STS-002 | Other/NULL | Aggregated with Trade Number = 0 |

### 4.4 FX Delta Sign Convention

| Rule ID | Condition | Action |
|---------|-----------|--------|
| BR-SIGN-001 | MAX(FXDELTA) ≠ 0 | Use MAX(FXDELTA) |
| BR-SIGN-002 | MAX(FXDELTA) = 0 | Use MIN(FXDELTA) |

---

## 5. Processing Requirements

### 5.1 Processing Schedule

| Step | Time (GMT) | Description |
|------|------------|-------------|
| 1 | 18:00 | Market data close (London) |
| 2 | 21:00 | Valuation batch complete |
| 3 | 02:00 | STB feeder batch start |
| 4 | 02:30 | Non-STB feeder batch start |
| 5 | 03:30 | Feeder batches complete |
| 6 | 04:00 | Extraction start |
| 7 | 04:30 | File generation |
| 8 | 05:00 | File packaging |
| 9 | 05:30 | MFT delivery |

### 5.2 Dependencies

| Upstream | Dependency Type | Impact if Delayed |
|----------|-----------------|-------------------|
| Market Data | Hard | Feed cannot run |
| Valuation Batch | Hard | Feed cannot run |
| FX Spot Rates | Hard | USD conversion fails |
| TBL_FX_CNT_REP | Hard | Currency pair standardization fails |

---

## 6. Stakeholders

### 6.1 Business Stakeholders

| Role | Responsibility |
|------|----------------|
| Head of FX Trading | Business owner |
| FX Risk Manager | Daily user, requirements |
| Treasury | Currency exposure consumer |
| ALM | Structural FX risk |

### 6.2 Technical Stakeholders

| Role | Responsibility |
|------|----------------|
| Risk Technology Lead | Technical delivery |
| Murex Support Team | Source system support |
| Data Warehouse Team | Target system integration |

---

## 7. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| STB/Non-STB join mismatch | High | Low | Daily reconciliation checks |
| New product types | Medium | Medium | Regular product review |
| Currency pair mapping | Medium | Low | Reference data validation |
| Dead deal aggregation confusion | Low | Medium | Clear documentation |

---

## 8. Known Issues

### 8.1 Deprecated ZAR Fields

Multiple ZAR-related fields are JBSBSA legacy and should be decommissioned:
- FXDELTA_ZAR
- FXDELTA_CURR2
- ZAR_PROCESSING

### 8.2 Portfolio Filtering Inconsistency

Different regions use different portfolio node levels (L4 vs L5). Recommend standardization to L4.

### 8.3 London Multi-Batch STB Processing

LDN uses 3 separate STB feeder batches due to historical Murex constraints. Evaluate consolidation opportunity.

---

*Document Version: 1.0 | Last Updated: 2025-01-13*
