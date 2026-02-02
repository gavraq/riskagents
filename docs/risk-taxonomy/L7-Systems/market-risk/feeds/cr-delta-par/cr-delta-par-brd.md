---
# Document Metadata
document_id: CR-DP-BRD-001
document_name: CR Delta Par Feed - Business Requirements Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Credit Risk Analytics
approving_committee: MLRC

# Parent Reference
parent_document: MR-L7-003  # Feeds Overview
feed_id: CR-DP-001
---

# CR Delta Par Feed - Business Requirements Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-DP-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Credit Risk Analytics |
| **Approver** | MLRC |

---

## 1. Executive Summary

This document specifies the business requirements for the CR Delta Par Feed (Credit Risk CS01 Par Curve Sensitivities) from Murex to the downstream Market Risk and VESPA reporting systems. This feed is **one of 8 Credit Sensitivities feeds** that together provide comprehensive credit spread risk metrics.

The CR Delta Par feed provides position-level credit spread sensitivities based on the **par spread curve methodology** for:

- **Single-name credit instruments**: CDS, Bonds with credit risk, Credit-linked notes
- **Credit Insurance and Guarantee products**: CRD Insurance, CRD Guarantee
- **Credit Index instruments**: iTraxx, CDX, and other credit indices (CRDI)

### 1.1 Credit Sensitivities Feed Suite

| Feed | File Name | Description |
|------|-----------|-------------|
| CR Delta Zero | MxMGB_MR_Credit_CS01_*.csv | CS01 based on zero/default spread curve |
| **CR Delta Par** | MxMGB_MR_Credit_CS01Par_*.csv | CS01 based on par spread curve (this document) |
| CR Basis Rate | MxMGB_MR_Credit_Basis_*.csv | Recovery rate sensitivity WITHOUT propagation |
| CR Par CDS Rate | MxMGB_MR_Credit_ParCDS_*.csv | Par CDS spread rate |
| CR Instrument Spread | MxMGB_MR_Credit_Spread_*.csv | Zero/instrument spread |
| CR Corr01 | MxMGB_MR_Credit_Corr01_*.csv | Correlation sensitivity (Monte Carlo) |
| CR RR01 | MxMGB_MR_Credit_RR01_*.csv | Recovery rate sensitivity (with propagation) |
| CR RR02 | MxMGB_MR_Credit_RR02_*.csv | Recovery rate sensitivity (without propagation) |

### 1.2 Purpose

The CR Delta Par sensitivity measures the P&L impact of a 1 basis point parallel shift in the issuer's credit **par spread curve**. This metric complements the CR Delta Zero (default spread) sensitivity and is essential for:

- VaR calculation (credit spread component using par spreads)
- Credit risk aggregation by issuer/sector
- Par spread-based limit monitoring
- Regulatory capital calculation (IMA, FRTB-SA)
- P&L attribution (par credit spread moves)
- Hedging effectiveness analysis (CDS par quotes)

### 1.3 Par vs Zero Spread Curves

| Aspect | Par Spread Curve | Zero/Default Spread Curve |
|--------|------------------|---------------------------|
| **Definition** | Running spread that makes CDS value zero | Bootstrapped hazard rate curve |
| **Market Observable** | Directly quoted in CDS market | Derived from par spreads |
| **Primary Use** | Trading/hedging | Risk analytics |
| **CR01 Metric** | CR01 (Par) - this feed | CR01 (Zero) - CR Delta Zero feed |

---

## 2. Business Objectives

### 2.1 Primary Objectives

| # | Objective | Priority |
|---|-----------|----------|
| 1 | Provide accurate position-level par spread sensitivities for VaR | Critical |
| 2 | Enable aggregation by issuer, sector, and par credit curve | Critical |
| 3 | Support regulatory reporting (IMA credit spread risk, FRTB-SA) | Critical |
| 4 | Enable credit concentration limit monitoring | High |
| 5 | Support P&L attribution to par spread movements | High |
| 6 | Facilitate hedge effectiveness analysis using par CDS quotes | High |

### 2.2 Use Cases

| Use Case | Description | User |
|----------|-------------|------|
| **UC-001** | Calculate 1-day VaR par spread component | Risk Engine (Plato) |
| **UC-002** | Aggregate CS01 (Par) by issuer for concentration analysis | Credit Risk Analytics |
| **UC-003** | Monitor issuer-level credit limits | Risk Management |
| **UC-004** | Calculate Credit RWA for IMA | Capital Calculation |
| **UC-005** | Attribute P&L to par spread movements | P&L Attribution |
| **UC-006** | Analyze CDS hedge effectiveness | Trading/Hedging |
| **UC-007** | Generate regulatory reports (FRTB-SA CSR bucket) | Regulatory Reporting |

---

## 3. Data Requirements

### 3.1 Sensitivity Types

#### 3.1.1 CR01 Par (Credit Spread Sensitivity - Par Curve)

| Metric | Description | Unit |
|--------|-------------|------|
| **CR01 Par (Local Currency)** | P&L impact of 1bp parallel shift in par spread curve | Trade currency |
| **CR01 Par (USD)** | CR01 Par converted to USD at COB FX rate | USD |

**Calculation Method**:
- Bump the issuer's credit **par spread** curve by 1 basis point (parallel shift)
- Recalculate the position's mark-to-market value
- CR01 (Par) = New MTM - Original MTM

**Source Fields**:
- `M_CR01__PA2` = CR01 (Par) quotation in local currency
- `M_CR01__PA1` = CR01 (Par) quotation in USD

#### 3.1.2 Recovery Rate

| Metric | Description | Unit |
|--------|-------------|------|
| **Recovery Rate** | Expected recovery rate in default scenario | Percentage (0-100%) |

**Usage**: Provided for reference; set to 0 for CRDI products.

### 3.2 Product Coverage

#### 3.2.1 Non-Index Products (Non-CRDI, excluding Insurance/Guarantee)

| Product Group | Product Types | Description |
|---------------|---------------|-------------|
| **CDS** | Single-name CDS | Credit Default Swaps on single issuers |
| **BOND** | Corporate bonds, FRNs | Bonds with credit spread risk |
| **CLN** | Credit-linked notes | Structured credit products |

#### 3.2.2 Insurance and Guarantee Products

| Product Group | Typology | Description |
|---------------|----------|-------------|
| **CRD - INSURANCE** | Credit insurance | Credit protection products |
| **CRD - GUARANTEE** | Credit guarantees | Credit guarantee products |

**Note**: These products are extracted separately due to different join conditions in the extraction SQL.

#### 3.2.3 Credit Index Products (CRDI)

| Index Family | Examples | Description |
|--------------|----------|-------------|
| **iTraxx** | iTraxx Europe, iTraxx Crossover | European credit indices |
| **CDX** | CDX.NA.IG, CDX.NA.HY | North American credit indices |
| **Other** | ABX, CMBX | Structured credit indices |

### 3.3 Tenor Pillars

Credit sensitivities are reported at standard credit curve tenor pillars:

| Pillar | Description |
|--------|-------------|
| 6M | Six months |
| 1Y | One year |
| 2Y | Two years |
| 3Y | Three years |
| 5Y | Five years |
| 7Y | Seven years |
| 10Y | Ten years |
| 15Y | Fifteen years |
| 20Y | Twenty years |
| 30Y | Thirty years |

### 3.4 Required Data Elements

#### 3.4.1 Trade Identification

| Field | Description | Purpose |
|-------|-------------|---------|
| Trade Number | Murex trade identifier | Unique identification |
| Portfolio | Trading portfolio | Hierarchy aggregation |
| Family | Trade family (CRD, IRD, EQD) | Product classification |
| Group | Trade group (CDS, BOND, CRDI) | Product sub-classification |
| Type | Trade type | Detailed classification |
| Typology | Trade typology | Risk classification |
| Instrument | PL Instrument | Instrument identification |

#### 3.4.2 Credit Reference Data

| Field | Description | Purpose |
|-------|-------------|---------|
| Issuer | Issuer name/label | Credit concentration |
| Curve Name | Par credit spread curve name | Risk factor mapping |
| CIF | Customer Information File ID | Issuer identification |
| GLOBUS ID | External issuer identifier | Cross-system reference |
| Country | Country of risk | Geographic concentration |
| ISIN | Reference obligation ISIN | Security identification |

#### 3.4.3 Sensitivity Data

| Field | Description | Purpose |
|-------|-------------|---------|
| CR01 Par (Local) | Par credit sensitivity in trade currency | Local currency risk |
| CR01 Par (USD) | Par credit sensitivity in USD | Aggregation currency |
| Recovery Rate | Expected recovery in default | Reference data |
| Currency | Trade/sensitivity currency | FX conversion |

#### 3.4.4 Trade Details

| Field | Description | Purpose |
|-------|-------------|---------|
| Date | Tenor pillar date | Tenor classification |
| Maturity | Trade maturity date | Tenor classification |
| Notional | Trade notional amount | Exposure sizing |
| Market | Security market | Market classification |
| Restructuring | Restructuring clause (CDS) | Contract terms |
| Underlying | Reference obligation | Credit reference |

---

## 4. Data Quality Requirements

### 4.1 Completeness

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| All credit positions must have CR01 Par sensitivities | 100% | 0% |
| Issuer field populated for non-CRDI trades | 100% | 0% |
| Recovery rate populated for non-CRDI trades | 100% | 0% |
| All hierarchy fields populated | 100% | 0% |
| CR01 Par (USD) calculated for all positions | 100% | 0% |

### 4.2 Accuracy

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| CR01 Par sign consistent with trade direction | 100% | 0% |
| CR01 Par values within valid range | 100% | 0% |
| Recovery rates between 0% and 100% | 100% | 0% |
| FX conversion to USD correct | 100% | 0.01% |

### 4.3 Reconciliation

| Reconciliation | Frequency | Tolerance |
|----------------|-----------|-----------|
| Position count: CR Delta Par vs. CR Delta Zero | Daily | 0% |
| Total CR01 Par (USD): Feed vs. Risk matrices | Daily | 0.1% |
| Notional: Feed vs. Trade system | Daily | 0% |
| Issuer count: Feed vs. Credit limits system | Weekly | 0% |

---

## 5. Timeliness Requirements

### 5.1 Service Level Agreements

| Metric | Target | Escalation |
|--------|--------|------------|
| **Feed Delivery Time** | 05:30 GMT (T+1) | >06:00 escalate to L2 |
| **As-Of Date** | T (previous business day) | N/A |
| **Position Coverage** | 100% of credit positions | <99% escalate to L2 |

### 5.2 Dependencies

| Upstream Dependency | SLA | Impact |
|---------------------|-----|--------|
| Par credit curve calibration complete | 18:00 | Cannot calculate CR01 Par |
| Trade extraction complete | 19:00 | Missing positions |
| Valuation batch complete | 21:00 | Delayed sensitivities |
| Recovery rate updates | 17:00 | Stale recovery rates |

---

## 6. Scope Definition

### 6.1 In-Scope Positions

| Criteria | Value |
|----------|-------|
| **STP Status** | RELE (Released), VERI (Verified), STTL (Settled) |
| **Legal Entity** | MGB (Meridian Global Bank) |
| **Product Families** | CRD (Credit), IRD (with credit risk), EQD (with credit risk) |
| **Groups** | CDS, BOND, CRDI, and other credit-sensitive products |
| **Typologies** | All including CRD - INSURANCE, CRD - GUARANTEE |
| **Credit Delta Date** | Must be non-null (has credit risk) |
| **Issuer** | Must be populated (for non-CRDI) |

### 6.2 Out-of-Scope

| Exclusion | Reason |
|-----------|--------|
| STP Status PEND or SALES | Not live deals |
| No issuer (non-CRDI) | Cannot attribute credit risk |
| Null credit delta date | No credit sensitivity |
| Banking book positions | Separate IRRBB/CSRBB process |
| Matured/cancelled trades | No risk exposure |

---

## 7. Regional Coverage

### 7.1 Trading Regions

| Region | Code | Status | Primary Products |
|--------|------|--------|------------------|
| **London** | LN | Active | CDS, Bonds, Credit Indices |
| **Hong Kong** | HK | Active | Asia credit products |
| **New York** | NY | Active | US credit products |
| **Singapore** | SP | Limited | Regional credit |

### 7.2 Credit Curve Sources

| Region | Market Data Set | Curve Provider |
|--------|-----------------|----------------|
| LN | LNCLOSE | Bloomberg, Markit |
| HK | HKCLOSE | Bloomberg, Markit |
| NY | NYCLOSE | Bloomberg, Markit |
| SP | SPCLOSE | Bloomberg, Markit |

---

## 8. Data Extraction Structure

### 8.1 Three-Way UNION Structure

The CR Delta Par feed uses a more complex extraction structure than CR Delta Zero, combining three data sources:

```
UNION ALL Structure:
┌─────────────────────────────────────────────────────────────┐
│ (i) Non-CRDI (excluding Insurance/Guarantee)                │
│     Source: TBL_VESPA_SENS_REP                              │
│     Filter: M_GROUP <> 'CRDI'                               │
│             M_TYPOLOGY NOT IN ('CRD - GUARANTEE',           │
│                                'CRD - INSURANCE')           │
├─────────────────────────────────────────────────────────────┤
│ (ii) Insurance and Guarantee Products                       │
│     Source: TBL_VESPA_SENS_REP                              │
│     Filter: M_TYPOLOGY IN ('CRD - GUARANTEE',               │
│                            'CRD - INSURANCE')               │
├─────────────────────────────────────────────────────────────┤
│ (iii) Credit Index Products (CRDI)                          │
│     Source: TBL_VESPA_SENSCI_REP                            │
│     Filter: M_GROUP = 'CRDI'                                │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 Additional Reference Tables

The extraction joins with multiple reference tables:

| Table | Purpose |
|-------|---------|
| TBL_SE_ROOT_REP / SB_SE_HEAD_REP | Security definition |
| SB_CP_REP | Counterparty definition including UDF |
| SB_TP_REP / SB_TP_EXT_REP / SB_TP_BD_REP | Transaction details |
| SB_CRI_DEF_REP | Credit Index definition |
| TBL_CRD_RECOVERY_REP | Credit recovery rate details |

---

## 9. Credit Index Handling (CRDI)

### 9.1 Differences from Single-Name Products

| Aspect | Single-Name (Non-CRDI) | Index (CRDI) |
|--------|------------------------|--------------|
| **Issuer** | Specific issuer name | PL Instrument (Index label) |
| **Curve Name** | Par credit curve | PL Instrument |
| **Recovery Rate** | Issuer-specific rate | Set to 0 |
| **CIF/GLOBUS_ID** | Issuer identifiers | Set to 0/blank |
| **Country** | Issuer country | Blank (multi-country) |
| **ISIN** | Reference obligation ISIN | Blank |
| **Restructuring** | Contract term | Set to NONE |
| **Market** | Security market | Blank |
| **Source Table** | TBL_VESPA_SENS_REP | TBL_VESPA_SENSCI_REP |

---

## 10. Exception Handling

### 10.1 Calculation Failures

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Par credit curve missing | Use T-1 curve with flag | Market Data Control |
| Position cannot be valued | Flag as ERROR, exclude | L2 Support |
| CR01 Par calculation fails | Use T-1 sensitivity | L2 Support |
| FX rate missing | Use T-1 rate with flag | Market Data Control |

### 10.2 Data Quality Issues

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Issuer unmapped | Use PL Instrument as fallback | Credit Data Team |
| Recovery rate missing | Use sector default | Credit Risk |
| Hierarchy unmapped | Map to UNMAPPED node | Bookman Team |
| Outlier CR01 Par value | Flag for review, include | RAV Team |

---

## 11. Change Management

### 11.1 Change Triggers

| Trigger | Process |
|---------|---------|
| New credit product type | Update scope, add to extraction |
| New credit index | Add to CRDI extraction |
| Regulatory change | Update requirements, MLRC approval |
| New par curve provider | Update market data mapping |

### 11.2 Approval Requirements

| Change Type | Approval |
|-------------|----------|
| Scope change | Head of Credit Risk Analytics |
| New sensitivity type | MLRC |
| Calculation methodology | Model Validation |
| SLA change | Risk Technology + Downstream |

---

## 12. Regulatory Requirements

### 12.1 IMA Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| Capture credit spread risk | CRR Art. 367 | CR01 Par sensitivities included |
| Issuer-level granularity | CRR Art. 367 | By issuer aggregation |
| Consistent with pricing | CRR Art. 367 | Same models as P&L |
| Daily calculation | CRR Art. 365 | Daily feed |

### 12.2 FRTB-SA Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| CSR non-securitisation | MAR21.4 | Single-name CR01 Par |
| CSR securitisation | MAR21.4 | Securitized products CR01 Par |
| Credit index risk | MAR21.4 | CRDI CR01 Par |
| Bucket assignment | MAR21.53 | By issuer rating/sector |

---

## 13. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |
| [CR Delta Par IT Config](./cr-delta-par-config.md) | CR-DP-CFG-001 | IT implementation |
| [CR Delta Par IDD](./cr-delta-par-idd.md) | CR-DP-IDD-001 | Interface specification |
| [CR Delta Zero BRD](../cr-delta-zero/cr-delta-zero-brd.md) | CR-DZ-BRD-001 | Related Zero curve feed |
| [VaR/SVaR Methodology](../../../L6-Models/market-risk/var-svar-methodology.md) | MR-L6-001 | Risk methodology |

---

## 14. Document Control

### 14.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-02 | Initial version | MLRC |

### 14.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Scope review | Semi-annual | July 2025 |
| Regulatory alignment | As needed | On regulatory change |

---

*End of Document*
