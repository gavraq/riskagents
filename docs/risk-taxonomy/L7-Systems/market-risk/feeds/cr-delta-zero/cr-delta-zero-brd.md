---
# Document Metadata
document_id: CR-DZ-BRD-001
document_name: CR Delta Zero Feed - Business Requirements Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Credit Risk Analytics
approving_committee: MLRC

# Parent Reference
parent_document: MR-L7-003  # Feeds Overview
feed_id: CR-DZ-001
---

# CR Delta Zero Feed - Business Requirements Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-DZ-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Credit Risk Analytics |
| **Approver** | MLRC |

---

## 1. Executive Summary

This document specifies the business requirements for the CR Delta Zero Feed (Credit Risk CS01 Zero Curve Sensitivities) from Murex to the downstream Market Risk and VESPA reporting systems. This feed is **one of 8 Credit Sensitivities feeds** that together provide comprehensive credit spread risk metrics.

The CR Delta Zero feed provides position-level credit spread sensitivities based on the **zero curve methodology** (default spreads) for:

- **Single-name credit instruments**: CDS, Bonds with credit risk, Credit-linked notes
- **Credit Index instruments**: iTraxx, CDX, and other credit indices (CRDI)

### 1.1 Credit Sensitivities Feed Suite

| Feed | File Name | Description |
|------|-----------|-------------|
| **CR Delta Zero** | MxMGB_MR_Credit_CS01_*.csv | CS01 based on zero/default spread curve (this document) |
| CR Delta Par | MxMGB_MR_Credit_CS01Par_*.csv | CS01 based on par spread curve |
| CR Basis Rate | MxMGB_MR_Credit_Basis_*.csv | Credit basis rate sensitivities |
| CR Par CDS Rate | MxMGB_MR_Credit_ParCDS_*.csv | Par CDS spread rate |
| CR Instrument Spread | MxMGB_MR_Credit_Spread_*.csv | Zero/instrument spread |
| CR Corr01 | MxMGB_MR_Credit_Corr01_*.csv | Correlation sensitivity (Monte Carlo) |
| CR RR01 | MxMGB_MR_Credit_RR01_*.csv | Recovery rate sensitivity (with propagation) |
| CR RR02 | MxMGB_MR_Credit_RR02_*.csv | Recovery rate sensitivity (without propagation) |

### 1.2 Purpose

The CR Delta Zero sensitivity measures the P&L impact of a 1 basis point parallel shift in the issuer's credit **zero/default spread curve**. This metric is essential for:

- VaR calculation (credit spread component)
- Credit risk aggregation by issuer/sector
- Limit monitoring (issuer concentration limits)
- Jump-to-Default (JTD) risk estimation
- Regulatory capital calculation (IMA, FRTB-SA)
- P&L attribution (credit spread moves)

---

## 2. Business Objectives

### 2.1 Primary Objectives

| # | Objective | Priority |
|---|-----------|----------|
| 1 | Provide accurate position-level credit spread sensitivities for VaR | Critical |
| 2 | Enable aggregation by issuer, sector, and credit curve | Critical |
| 3 | Support regulatory reporting (IMA credit spread risk, FRTB-SA) | Critical |
| 4 | Enable credit concentration limit monitoring | High |
| 5 | Support P&L attribution to credit spread movements | High |
| 6 | Provide recovery rate information for JTD calculations | High |

### 2.2 Use Cases

| Use Case | Description | User |
|----------|-------------|------|
| **UC-001** | Calculate 1-day VaR credit spread component | Risk Engine (Plato) |
| **UC-002** | Aggregate CS01 by issuer for concentration analysis | Credit Risk Analytics |
| **UC-003** | Monitor issuer-level credit limits | Risk Management |
| **UC-004** | Calculate Credit RWA for IMA | Capital Calculation |
| **UC-005** | Attribute P&L to credit spread movements | P&L Attribution |
| **UC-006** | Estimate Jump-to-Default exposure using recovery rates | Credit Risk |
| **UC-007** | Generate regulatory reports (FRTB-SA CSR bucket) | Regulatory Reporting |

---

## 3. Data Requirements

### 3.1 Sensitivity Types

#### 3.1.1 CR01 / CS01 (Credit Spread Sensitivity)

| Metric | Description | Unit |
|--------|-------------|------|
| **CR01 (Local Currency)** | P&L impact of 1bp parallel shift in credit spread curve | Trade currency |
| **CR01 (USD)** | CR01 converted to USD at COB FX rate | USD |

**Calculation Method**:
- Bump the issuer's credit spread curve by 1 basis point (parallel shift)
- Recalculate the position's mark-to-market value
- CR01 = New MTM - Original MTM

#### 3.1.2 Recovery Rate

| Metric | Description | Unit |
|--------|-------------|------|
| **Recovery Rate** | Expected recovery rate in default scenario | Percentage (0-100%) |

**Usage**: Used with CR01 to estimate Jump-to-Default (JTD) exposure:
```
JTD = Notional × (1 - Recovery Rate) × Direction
```

### 3.2 Product Coverage

#### 3.2.1 Non-Index Products (Non-CRDI)

| Product Group | Product Types | Description |
|---------------|---------------|-------------|
| **CDS** | Single-name CDS | Credit Default Swaps on single issuers |
| **BOND** | Corporate bonds, FRNs | Bonds with credit spread risk |
| **CLN** | Credit-linked notes | Structured credit products |

#### 3.2.2 Credit Index Products (CRDI)

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

#### 3.4.2 Credit Reference Data

| Field | Description | Purpose |
|-------|-------------|---------|
| Issuer | Issuer name/label | Credit concentration |
| Curve Name | Credit spread curve name | Risk factor mapping |
| CIF | Customer Information File ID | Issuer identification |
| GLOBUS ID | External issuer identifier | Cross-system reference |
| Country | Country of risk | Geographic concentration |
| ISIN | Reference obligation ISIN | Security identification |

#### 3.4.3 Sensitivity Data

| Field | Description | Purpose |
|-------|-------------|---------|
| CR01 (Local) | Credit sensitivity in trade currency | Local currency risk |
| CR01 (USD) | Credit sensitivity in USD | Aggregation currency |
| Recovery Rate | Expected recovery in default | JTD calculation |
| Currency | Trade/sensitivity currency | FX conversion |

#### 3.4.4 Trade Details

| Field | Description | Purpose |
|-------|-------------|---------|
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
| All credit positions must have CR01 sensitivities | 100% | 0% |
| Issuer field populated for non-CRDI trades | 100% | 0% |
| Recovery rate populated for CDS trades | 100% | 0% |
| All hierarchy fields populated | 100% | 0% |
| CR01 (USD) calculated for all positions | 100% | 0% |

### 4.2 Accuracy

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| CR01 sign consistent with trade direction | 100% | 0% |
| CR01 values within valid range | 100% | 0% |
| Recovery rates between 0% and 100% | 100% | 0% |
| FX conversion to USD correct | 100% | 0.01% |

### 4.3 Reconciliation

| Reconciliation | Frequency | Tolerance |
|----------------|-----------|-----------|
| Position count: CR Delta feed vs. Trade feed | Daily | 0% |
| Total CR01 (USD): Feed vs. Risk matrices | Daily | 0.1% |
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
| Credit curve calibration complete | 18:00 | Cannot calculate CR01 |
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

### 6.3 Product Breakdown

| Family | Group | Products |
|--------|-------|----------|
| **CRD** | CDS | Single-name CDS, CDS on sovereigns |
| **CRD** | CRDI | iTraxx, CDX indices and tranches |
| **IRD** | BOND | Corporate bonds, FRNs with credit risk |
| **IRD** | CALL/PUT | Callable bonds with credit risk |

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

## 8. Credit Index Handling (CRDI)

### 8.1 Differences from Single-Name Products

| Aspect | Single-Name (Non-CRDI) | Index (CRDI) |
|--------|------------------------|--------------|
| **Issuer** | Specific issuer name | Index label (e.g., CDX.NA.IG) |
| **Curve Name** | Issuer credit curve | Index label |
| **Recovery Rate** | Issuer-specific rate | Set to 0 (index-level) |
| **CIF/GLOBUS_ID** | Issuer identifiers | Set to 0/blank |
| **Country** | Issuer country | Blank (multi-country) |
| **ISIN** | Reference obligation ISIN | Blank |
| **Source Table** | TBL_VESPA_SENS_REP | TBL_VESPA_SENSCI_REP |

### 8.2 Index Decomposition

For regulatory purposes (FRTB-SA), credit indices may need to be decomposed into their constituent single-name exposures. This is handled by a separate decomposition process, not this feed.

---

## 9. Exception Handling

### 9.1 Calculation Failures

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Credit curve missing | Use T-1 curve with flag | Market Data Control |
| Position cannot be valued | Flag as ERROR, exclude | L2 Support |
| CR01 calculation fails | Use T-1 sensitivity | L2 Support |
| FX rate missing | Use T-1 rate with flag | Market Data Control |

### 9.2 Data Quality Issues

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Issuer unmapped | Flag for review | Credit Data Team |
| Recovery rate missing | Use sector default | Credit Risk |
| Hierarchy unmapped | Map to UNMAPPED node | Bookman Team |
| Outlier CR01 value | Flag for review, include | RAV Team |

---

## 10. Change Management

### 10.1 Change Triggers

| Trigger | Process |
|---------|---------|
| New credit product type | Update scope, add to extraction |
| New credit index | Add to CRDI extraction |
| Regulatory change | Update requirements, MLRC approval |
| New credit curve provider | Update market data mapping |

### 10.2 Approval Requirements

| Change Type | Approval |
|-------------|----------|
| Scope change | Head of Credit Risk Analytics |
| New sensitivity type | MLRC |
| Calculation methodology | Model Validation |
| SLA change | Risk Technology + Downstream |

---

## 11. Regulatory Requirements

### 11.1 IMA Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| Capture credit spread risk | CRR Art. 367 | CR01 sensitivities included |
| Issuer-level granularity | CRR Art. 367 | By issuer aggregation |
| Consistent with pricing | CRR Art. 367 | Same models as P&L |
| Daily calculation | CRR Art. 365 | Daily feed |

### 11.2 FRTB-SA Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| CSR non-securitisation | MAR21.4 | Single-name CR01 |
| CSR securitisation | MAR21.4 | Securitized products CR01 |
| Credit index risk | MAR21.4 | CRDI CR01 |
| Bucket assignment | MAR21.53 | By issuer rating/sector |

---

## 12. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |
| [CR Delta Zero IT Config](./cr-delta-zero-config.md) | CR-DZ-CFG-001 | IT implementation |
| [CR Delta Zero IDD](./cr-delta-zero-idd.md) | CR-DZ-IDD-001 | Interface specification |
| [Sensitivities BRD](../sensitivities/sensitivities-brd.md) | SENS-BRD-001 | General sensitivities |
| [VaR/SVaR Methodology](../../../L6-Models/market-risk/var-svar-methodology.md) | MR-L6-001 | Risk methodology |

---

## 13. Document Control

### 13.1 Version History

| Version | Date | Change | Approved By |
|---------|------|--------|-------------|
| 1.0 | 2025-01-02 | Initial version | MLRC |

### 13.2 Review Schedule

| Review Type | Frequency | Next Due |
|-------------|-----------|----------|
| Full review | Annual | January 2026 |
| Scope review | Semi-annual | July 2025 |
| Regulatory alignment | As needed | On regulatory change |

---

*End of Document*
