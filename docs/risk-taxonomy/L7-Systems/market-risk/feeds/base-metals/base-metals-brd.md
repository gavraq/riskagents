---
# Document Metadata
document_id: BM-BRD-001
document_name: Base Metals Sensitivities Feed - Business Requirements Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Commodities Risk Analytics
approving_committee: MLRC

# Parent Reference
parent_document: MR-L7-003  # Feeds Overview
feed_id: BM-001
---

# Base Metals Sensitivities Feed - Business Requirements Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | BM-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Commodities Risk Analytics |
| **Approver** | MLRC |

---

## 1. Executive Summary

This document specifies the business requirements for the Base Metals Sensitivities Feed from Murex to the downstream Market Risk process. The feed provides position-level sensitivity metrics (Greeks) for base metals commodities traded on the London Metal Exchange (LME). These sensitivities are used for:

- VaR calculation (delta-gamma-vega approximation)
- Risk aggregation and reporting
- Limit monitoring
- Hedge effectiveness analysis
- P&L attribution

### 1.1 Covered Commodities

| Metal | Symbol | LME Code | Primary Exchange |
|-------|--------|----------|------------------|
| Copper | CU | CA | LME |
| Aluminium | AL | AH | LME |
| Zinc | ZN | ZS | LME |
| Nickel | NI | NI | LME |
| Lead | PB | PB | LME |
| Tin | SN | SN | LME |

---

## 2. Business Objectives

### 2.1 Primary Objectives

| # | Objective | Priority |
|---|-----------|----------|
| 1 | Provide accurate position-level sensitivities for base metals VaR calculation | Critical |
| 2 | Enable risk aggregation across metal types and portfolios | Critical |
| 3 | Support regulatory reporting (IMA, FRTB-SA) | Critical |
| 4 | Enable intraday commodity risk monitoring | High |
| 5 | Support P&L attribution and back-testing | High |

### 2.2 Use Cases

| Use Case | Description | User |
|----------|-------------|------|
| **UC-001** | Calculate 1-day VaR using sensitivity-based approach for base metals | Risk Engine |
| **UC-002** | Aggregate Delta by metal type and tenor bucket | Commodities Risk Analytics |
| **UC-003** | Monitor Delta and Vega limits by trading desk | Risk Management |
| **UC-004** | Calculate Risk-Weighted Assets for IMA commodities | Capital Calculation |
| **UC-005** | Attribute P&L to base metal price and volatility factors | P&L Attribution |
| **UC-006** | Calculate Weighted Vega for time-adjusted volatility risk | Options Risk |

---

## 3. Data Requirements

### 3.1 Sensitivity Types Required

The following sensitivities must be calculated and included in the feed:

#### 3.1.1 Position Quantity Metrics

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **Quantity (Lots)** | Number of lots purchased/sold | Lots | By position, metal |
| **Quantity (MT)** | Number of Lots × Lot size | Metric Tonnes | By position, metal |
| **Quantity (USD)** | Quantity in MT × Price in USD | USD | By position, metal |

**Lot Sizes by Metal**:

| Metal | Lot Size (MT) |
|-------|---------------|
| Copper (CU) | 25 |
| Aluminium (AL) | 25 |
| Zinc (ZN) | 25 |
| Nickel (NI) | 6 |
| Lead (PB) | 25 |
| Tin (SN) | 5 |

#### 3.1.2 Delta Sensitivities

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **Adapted Forward Delta (MT)** | P&L impact of $1/MT move in metal price, including smile impact | MT | By metal, tenor bucket |
| **Adapted Forward Delta (USD)** | Adapted Forward Delta (MT) × Metal Price | USD | By metal, tenor bucket |
| **Discounted Adapted Forward Delta (MT)** | Adapted Forward Delta discounted to COB valuation date | MT | By metal, tenor bucket |
| **Discounted Adapted Forward Delta (USD)** | Discounted Delta (MT) × Metal Price | USD | By metal, tenor bucket |

**Note**: "Adapted" Delta incorporates volatility smile impact, unlike standard ("Unadapted") Delta which assumes flat volatility.

#### 3.1.3 Gamma Sensitivities

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **Discounted Adapted Forward Gamma (MT)** | Change in Delta for $1/MT shift in metal price | MT | By metal, tenor bucket |
| **Discounted Adapted Forward Gamma (USD)** | Discounted Gamma (MT) × Metal Price² | USD | By metal, tenor bucket |

#### 3.1.4 Volatility Sensitivities

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **Vega** | Change in option value from 1% relative increase in implied volatility | USD | By metal, tenor, strike pillar |
| **Weighted Vega** | Vega weighted by square root of time-to-maturity (30-day reference) | USD | By metal, tenor, strike pillar |
| **Volga** | Change in Vega from 1% volatility change (second-order vol sensitivity) | USD | By metal |
| **Vanna** | Change in Discounted Forward Delta from 1% volatility change | USD | By metal |

**Weighted Vega Calculation**:
```
IF (Vega <> 0.0) THEN
  Weighted_Vega := sqrt(30.0 / Days_to_Maturity) * (1.0/100.0) * Vega * 100.0
```

This formula applies time-decay weighting relative to 1 month (30 days), so:
- Options maturing in 30 days have Weighted Vega = Vega
- Options maturing in 120 days have Weighted Vega = 0.5 × Vega
- Options maturing in 7.5 days have Weighted Vega = 2 × Vega

#### 3.1.5 Time Decay

| Sensitivity | Description | Unit | Granularity |
|-------------|-------------|------|-------------|
| **Theta** | P&L impact of 1-day time decay | USD | By position |

### 3.2 Pillaring Structure

#### 3.2.1 Tenor Pillars (LME Standard)

Sensitivities are bucketed to the following LME-aligned tenor pillars:

| Pillar | Description | Days to Maturity |
|--------|-------------|------------------|
| Cash | Spot settlement | 0-2 |
| 1M | One month | ~22 business days |
| 3M | Three months | ~66 business days |
| 6M | Six months | ~132 business days |
| 1Y | One year | ~264 business days |
| 18M | Eighteen months | ~396 business days |
| 2Y | Two years | ~528 business days |
| 3Y | Three years | ~792 business days |
| 5Y | Five years | ~1320 business days |
| 7Y | Seven years | ~1848 business days |
| 10Y | Ten years | ~2640 business days |

**Pillaring Methodology**:
- Sensitivities are allocated to adjacent pillars using linear interpolation
- Allocation is weighted by proximity to each pillar date
- Example: A sensitivity at 4.5M maturity allocates 50% to 3M pillar and 50% to 6M pillar

#### 3.2.2 Volatility Surface Pillars (Delta-Based)

For volatility sensitivities (Vega, Weighted Vega, Volga, Vanna), strike is expressed in delta terms:

| Delta Pillar | Description |
|--------------|-------------|
| 10 | 10-delta (deep out-of-the-money) |
| 25 | 25-delta (out-of-the-money) |
| 50 | 50-delta (at-the-money) |
| 75 | 75-delta (in-the-money) |
| 90 | 90-delta (deep in-the-money) |

### 3.3 Required Fields

Each sensitivity record must include:

| Field Category | Fields | Purpose |
|----------------|--------|---------|
| **Position ID** | Trade ID, Position ID | Unique identification |
| **Hierarchy** | Book, Desk, Division, Entity | Aggregation |
| **Product** | Product type, Option type | Classification |
| **Underlying** | Metal code, Metal name | Risk attribution |
| **Tenor** | Pillar date, Days to maturity | Tenor granularity |
| **Strike** | Delta pillar (for vol sensitivities) | Moneyness |
| **Sensitivity** | Sensitivity type, Value (USD/MT) | Risk metric |
| **Metadata** | Calculation date, As-of date, Market data set | Audit trail |

### 3.4 Calculation Specifications

#### 3.4.1 Bump Sizes

| Risk Factor | Bump Size | Direction |
|-------------|-----------|-----------|
| Metal Price (Delta) | $1/MT | Up |
| Metal Price (Gamma) | $1/MT | Up |
| Implied Volatility | 1% relative | Up |
| Time (Theta) | 1 day | Forward |

#### 3.4.2 Calculation Method

- **Method**: Full revaluation with analytical sensitivities where available
- **Model**: Murex standard pricing models for commodity options
- **Market Data**: LNCLOSE (London COB market data set)
- **Currency**: All sensitivities reported in USD (base currency)
- **Discounting**: Discounted to COB valuation date using risk-free rate

### 3.5 Aggregation Requirements

Sensitivities must be aggregated at the following levels:

| Level | Description | Use Case |
|-------|-------------|----------|
| **Position** | Individual trade/position | Granular analysis |
| **Metal** | By commodity type (CU, AL, etc.) | Metal-level risk |
| **Portfolio** | Lowest aggregation node | Desk reporting |
| **Desk** | Trading desk | Limit monitoring |
| **Division** | Business division | Management reporting |
| **Entity** | Legal entity | Regulatory reporting |
| **Total** | Bank-wide base metals | Executive reporting |

---

## 4. Data Quality Requirements

### 4.1 Completeness

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| All in-scope positions must have sensitivities | 100% | 0% |
| All required sensitivity types calculated | 100% | 0% |
| All hierarchy fields populated | 100% | 0% |
| All reference data resolved | 100% | 0% |
| Metal code mapping complete | 100% | 0% |

### 4.2 Accuracy

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| Sensitivity values within valid range | 100% | 0% |
| Delta-Gamma consistency | 100% | 0.1% |
| Vega-Volga-Vanna consistency | 100% | 0.1% |
| Sign consistency with position direction | 100% | 0% |
| Weighted Vega formula applied correctly | 100% | 0% |

### 4.3 Reconciliation

| Reconciliation | Frequency | Tolerance |
|----------------|-----------|-----------|
| Position count: Base Metals Sensitivity feed vs. Trade feed | Daily | 0% |
| Delta total: Sensitivity feed vs. Risk matrices | Daily | 0.1% |
| VaR contribution: Sensitivity-based vs. Full reval | Weekly | 5% |
| Quantity (Lots) vs. Trade system | Daily | 0% |

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
| LME market data snapshot | 18:30 | Cannot calculate |
| Valuation batch complete | 21:00 | Cannot calculate |
| Volatility surface calibration | 20:00 | Vega metrics delayed |

---

## 6. Scope Definition

### 6.1 In-Scope Portfolios

| Criteria | Value |
|----------|-------|
| **Book Type** | Trading Book only |
| **Entity Set** | TRADING (not BANKING) |
| **Product Status** | Live (not matured, not cancelled) |
| **Position Value** | Non-zero MTM or sensitivity |
| **Commodity Type** | Base Metals (LME-traded) |

### 6.2 Out-of-Scope

| Exclusion | Reason |
|-----------|--------|
| Banking Book positions | Separate process |
| Matured trades | No risk exposure |
| Cancelled trades | No risk exposure |
| Placeholder trades | Not real exposure |
| Precious Metals (Gold, Silver, Platinum) | Separate Precious Metals feed |
| Energy commodities | Separate Energy feed |
| Agricultural commodities | Separate Agri feed |

### 6.3 Product Coverage

| Product Type | Description |
|--------------|-------------|
| **LME Futures** | Standard LME metal futures |
| **LME Options** | Options on LME futures |
| **Metal Swaps** | OTC metal price swaps |
| **Asian Options** | Average price options |
| **Barrier Options** | Knock-in/knock-out options |
| **Forwards** | OTC metal forwards |

---

## 7. Regional Coverage

### 7.1 Trading Regions

| Region | Portfolio Node | Status | Market Data Set |
|--------|----------------|--------|-----------------|
| **London (LN)** | BMLN | Active (LIVE trades) | LNCLOSE |
| Hong Kong (HK) | PMHK | Dormant | HKCLOSE |
| New York (NY) | PMNY | Dormant | NYCLOSE |
| Singapore (SP) | LMSP | Dormant | SPCLOSE |

**Note**: Currently, all Base Metals trading is conducted out of London. Other regions maintain portfolio structures for potential future expansion.

### 7.2 Market Data Sets

| Market Data Set | Description | Usage |
|-----------------|-------------|-------|
| **LNCLOSE** | London COB prices | Primary (all regions currently) |
| HKCLOSE | Hong Kong COB prices | Future use |
| NYCLOSE | New York COB prices | Future use |
| SPCLOSE | Singapore COB prices | Future use |

---

## 8. Exception Handling

### 8.1 Calculation Failures

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Position cannot be valued | Flag as ERROR, exclude from feed | L2 Support |
| Sensitivity calculation fails | Use T-1 sensitivity with flag | L2 Support |
| Market data missing | Use T-1 prices with flag | Market Data Control |
| Volatility surface incomplete | Use proxy surface with flag | Commodities Risk |

### 8.2 Data Quality Issues

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Hierarchy unmapped | Map to UNMAPPED node | Bookman Team |
| Metal code unrecognized | Flag for review | Data Management |
| Outlier sensitivity | Flag for review, include | RAV Team |
| Lot size mismatch | Reconcile with trade system | Operations |

---

## 9. Change Management

### 9.1 Change Triggers

| Trigger | Process |
|---------|---------|
| New metal type added | Update scope, add sensitivity mappings |
| New option type | Update calculation methodology |
| Regulatory change | Update requirements, obtain MLRC approval |
| LME contract specification change | Update lot sizes, pillar dates |
| New trading region activation | Configure regional extraction |

### 9.2 Approval Requirements

| Change Type | Approval |
|-------------|----------|
| Scope change | Head of Commodities Risk Analytics |
| New sensitivity type | MLRC |
| Calculation methodology | Model Validation |
| SLA change | Risk Technology + Downstream |

---

## 10. Regulatory Requirements

### 10.1 IMA Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| Full capture of commodity risks | CRR Art. 367 | All sensitivity types included |
| Consistent with pricing models | CRR Art. 367 | Same models as P&L |
| Daily calculation | CRR Art. 365 | Daily feed |
| Separate commodity risk factors | CRR Art. 365 | By metal type and tenor |

### 10.2 FRTB-SA Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| Commodity delta risk | MAR21.8 | Adapted Forward Delta |
| Commodity vega risk | MAR21.9 | Vega by tenor and strike |
| Commodity curvature risk | MAR21.5 | Gamma sensitivities |
| Commodity bucket mapping | MAR21.82 | LME pillar structure |

---

## 11. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |
| [Base Metals IT Config](./base-metals-config.md) | BM-CFG-001 | IT implementation |
| [Base Metals IDD](./base-metals-idd.md) | BM-IDD-001 | Interface specification |
| [Sensitivities BRD](../sensitivities/sensitivities-brd.md) | SENS-BRD-001 | General sensitivities |
| [VaR/SVaR Methodology](../../../L6-Models/market-risk/var-svar-methodology.md) | MR-L6-001 | Risk methodology |

---

## 12. Document Control

### 12.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-02 | Initial version | MLRC |

### 12.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Scope review | Semi-annual | July 2025 |
| Regulatory alignment | As needed | On regulatory change |

---

*End of Document*
