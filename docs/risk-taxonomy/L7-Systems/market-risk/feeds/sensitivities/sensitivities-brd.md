---
# Document Metadata
document_id: SENS-BRD-001
document_name: Sensitivities Feed - Business Requirements Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Market Risk Analytics
approving_committee: MLRC

# Parent Reference
parent_document: MR-L7-003  # Feeds Overview
feed_id: SENS-001
---

# Sensitivities Feed - Business Requirements Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | SENS-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Market Risk Analytics |
| **Approver** | MLRC |

---

## 1. Executive Summary

This document specifies the business requirements for the Sensitivities Feed from Murex to the downstream Market Risk process. The feed provides position-level sensitivity metrics (Greeks) that are used for:

- VaR calculation (delta-gamma approximation)
- Risk aggregation and reporting
- Limit monitoring
- Hedge effectiveness analysis
- P&L attribution

---

## 2. Business Objectives

### 2.1 Primary Objectives

| # | Objective | Priority |
|---|-----------|----------|
| 1 | Provide accurate position-level sensitivities for VaR calculation | Critical |
| 2 | Enable risk aggregation to portfolio hierarchy | Critical |
| 3 | Support regulatory reporting (IMA, FRTB) | Critical |
| 4 | Enable intraday risk monitoring | High |
| 5 | Support P&L attribution and back-testing | High |

### 2.2 Use Cases

| Use Case | Description | User |
|----------|-------------|------|
| **UC-001** | Calculate 1-day VaR using sensitivity-based approach | Risk Engine |
| **UC-002** | Aggregate DV01 by currency and tenor bucket | Market Risk Analytics |
| **UC-003** | Monitor DV01 limits by trading desk | Risk Management |
| **UC-004** | Calculate Risk-Weighted Assets for IMA | Capital Calculation |
| **UC-005** | Attribute P&L to risk factors | P&L Attribution |

---

## 3. Data Requirements

### 3.1 Sensitivity Types Required

The following sensitivities must be calculated and included in the feed:

#### 3.1.1 Interest Rate Sensitivities

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **DV01** | P&L impact of 1bp parallel shift in yield curve | USD | By currency, tenor bucket |
| **KRD** | Key Rate Duration (sensitivity to specific tenor) | USD | By currency, tenor point |
| **Convexity** | Second-order interest rate sensitivity | USD | By currency |
| **Twist Risk** | Sensitivity to yield curve steepening | USD | By currency |

**Tenor Buckets for Interest Rate Risk**:
- 0-3M, 3-6M, 6M-1Y, 1-2Y, 2-3Y, 3-5Y, 5-7Y, 7-10Y, 10-15Y, 15-20Y, 20-30Y, 30Y+

#### 3.1.2 Credit Sensitivities

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **CS01** | P&L impact of 1bp parallel shift in credit spread | USD | By issuer, tenor bucket |
| **JTD** | Jump-to-Default exposure | USD | By issuer |
| **Recovery** | Sensitivity to recovery rate | USD | By issuer |

**Tenor Buckets for Credit Risk**:
- 0-1Y, 1-3Y, 3-5Y, 5-10Y, 10Y+

#### 3.1.3 FX Sensitivities

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **FX Delta** | P&L impact of 1% move in FX rate | USD | By currency pair |
| **FX Gamma** | Second-order FX sensitivity | USD | By currency pair |
| **FX Vega** | Sensitivity to FX implied vol | USD | By currency pair, tenor |

#### 3.1.4 Equity Sensitivities

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **EQ Delta** | P&L impact of 1% move in equity price | USD | By underlying |
| **EQ Gamma** | Second-order equity sensitivity | USD | By underlying |
| **EQ Vega** | Sensitivity to equity implied vol | USD | By underlying, tenor |

#### 3.1.5 Commodity Sensitivities

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **CM Delta** | P&L impact of 1% move in commodity price | USD | By commodity, tenor |
| **CM Vega** | Sensitivity to commodity implied vol | USD | By commodity, tenor |

#### 3.1.6 Volatility Sensitivities

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **Vega** | P&L impact of 1% move in implied vol | USD | By underlying, tenor, strike |
| **Volga** | Second-order vol sensitivity | USD | By underlying |
| **Vanna** | Cross sensitivity (delta to vol) | USD | By underlying |

#### 3.1.7 Time Decay

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **Theta** | P&L impact of 1-day time decay | USD | By position |

### 3.2 Required Fields

Each sensitivity record must include:

| Field Category | Fields | Purpose |
|----------------|--------|---------|
| **Position ID** | Trade ID, Position ID | Unique identification |
| **Hierarchy** | Book, Desk, Division, Entity | Aggregation |
| **Product** | Product type, Asset class | Classification |
| **Risk Factor** | Currency, Issuer, Underlying | Risk attribution |
| **Tenor** | Tenor bucket, Maturity date | Tenor granularity |
| **Sensitivity** | Sensitivity type, Value (USD) | Risk metric |
| **Metadata** | Calculation date, As-of date | Audit trail |

### 3.3 Calculation Specifications

#### 3.3.1 Bump Sizes

| Risk Factor | Bump Size | Direction |
|-------------|-----------|-----------|
| Interest Rate | 1 basis point | Up |
| Credit Spread | 1 basis point | Up |
| FX Rate | 1% | Up |
| Equity Price | 1% | Up |
| Commodity Price | 1% | Up |
| Implied Volatility | 1% absolute | Up |

#### 3.3.2 Calculation Method

- **Method**: Full revaluation with analytical sensitivities where available
- **Model**: Murex standard pricing models per asset class
- **Market Data**: VaR market data set (e.g., LNVARVAL, NYVARVAL)
- **Currency**: All sensitivities reported in USD (base currency)

### 3.4 Aggregation Requirements

Sensitivities must be aggregated at the following levels:

| Level | Description | Use Case |
|-------|-------------|----------|
| **Position** | Individual trade/position | Granular analysis |
| **Portfolio** | Lowest aggregation node | Desk reporting |
| **Desk** | Trading desk | Limit monitoring |
| **Division** | Business division | Management reporting |
| **Entity** | Legal entity | Regulatory reporting |
| **Total** | Bank-wide | Executive reporting |

---

## 4. Data Quality Requirements

### 4.1 Completeness

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| All in-scope positions must have sensitivities | 100% | 0% |
| All required sensitivity types calculated | 100% | 0% |
| All hierarchy fields populated | 100% | 0% |
| All reference data resolved | 100% | 0% |

### 4.2 Accuracy

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| Sensitivity values within valid range | 100% | 0% |
| Cross-sensitivity consistency | 100% | 0.1% |
| Sign consistency with position direction | 100% | 0% |

### 4.3 Reconciliation

| Reconciliation | Frequency | Tolerance |
|----------------|-----------|-----------|
| Position count: Sensitivity feed vs. Trade feed | Daily | 0% |
| DV01 total: Sensitivity feed vs. Risk matrices | Daily | 0.1% |
| VaR contribution: Sensitivity-based vs. Full reval | Weekly | 5% |

---

## 5. Timeliness Requirements

### 5.1 Service Level Agreements

| Metric | Target | Escalation |
|--------|--------|------------|
| **Feed Delivery Time** | 05:30 GMT (T+1) | >06:00 escalate to L2 |
| **As-Of Date** | T (previous business day) | N/A |
| **Position Coverage** | 100% of EOD positions | <99% escalate to L2 |

### 5.2 Dependencies

| Upstream Dependency | SLA | Impact |
|---------------------|-----|--------|
| Trade extraction complete | 19:00 | Cannot calculate |
| Market data snapshot | 18:30 | Cannot calculate |
| Valuation batch complete | 21:00 | Cannot calculate |

---

## 6. Scope Definition

### 6.1 In-Scope Portfolios

| Criteria | Value |
|----------|-------|
| **Book Type** | Trading Book only |
| **Entity Set** | TRADING (not BANKING) |
| **Product Status** | Live (not matured, not cancelled) |
| **Position Value** | Non-zero MTM or sensitivity |

### 6.2 Out-of-Scope

| Exclusion | Reason |
|-----------|--------|
| Banking Book positions | Separate IRRBB process |
| Matured trades | No risk exposure |
| Cancelled trades | No risk exposure |
| Placeholder trades | Not real exposure |

### 6.3 Product Coverage

| Asset Class | Product Types |
|-------------|---------------|
| **Interest Rates** | Swaps, FRAs, Caps/Floors, Swaptions, Bond options |
| **Credit** | CDS, Index CDS, Tranches, CLNs |
| **FX** | Spots, Forwards, Options, Exotics |
| **Equities** | Stocks, Options, Variance swaps, Dividends |
| **Commodities** | Futures, Options, Swaps |

---

## 7. Exception Handling

### 7.1 Calculation Failures

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Position cannot be valued | Flag as ERROR, exclude from feed | L2 Support |
| Sensitivity calculation fails | Use T-1 sensitivity with flag | L2 Support |
| Market data missing | Use proxy/T-1 with flag | Market Data Control |

### 7.2 Data Quality Issues

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Hierarchy unmapped | Map to UNMAPPED node | RAV Team |
| Reference data missing | Flag as INCOMPLETE | Data Management |
| Outlier sensitivity | Flag for review, include | RAV Team |

---

## 8. Change Management

### 8.1 Change Triggers

| Trigger | Process |
|---------|---------|
| New product type | Update scope, add sensitivity types |
| New risk factor | Add to sensitivity calculation |
| Regulatory change | Update requirements, obtain MLRC approval |
| Downstream consumer change | Impact assessment, coordinate timing |

### 8.2 Approval Requirements

| Change Type | Approval |
|-------------|----------|
| Scope change | Head of Market Risk Analytics |
| New sensitivity type | MLRC |
| Calculation methodology | Model Validation |
| SLA change | Risk Technology + Downstream |

---

## 9. Regulatory Requirements

### 9.1 IMA Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| Full capture of material risks | CRR Art. 367 | All sensitivity types included |
| Consistent with pricing models | CRR Art. 367 | Same models as P&L |
| Daily calculation | CRR Art. 365 | Daily feed |

### 9.2 FRTB Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| Standardised sensitivities | MAR21 | Separate FRTB feed |
| Risk factor granularity | MAR21 | Meets bucket requirements |
| Currency conversion | MAR21 | USD base currency |

---

## 10. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |
| [Sensitivities IT Config](./sensitivities-config.md) | SENS-CFG-001 | IT implementation |
| [Sensitivities IDD](./sensitivities-idd.md) | SENS-IDD-001 | Interface specification |
| [VaR/SVaR Methodology](../../../L6-Models/market-risk/var-svar-methodology.md) | MR-L6-001 | Risk methodology |

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-02 | Initial version | MLRC |

### 11.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Scope review | Semi-annual | July 2025 |
| Regulatory alignment | As needed | On regulatory change |

---

*End of Document*
