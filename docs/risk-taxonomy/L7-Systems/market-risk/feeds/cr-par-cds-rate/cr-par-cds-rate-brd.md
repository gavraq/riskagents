---
# Document Metadata
document_id: CR-PAR-BRD-001
document_name: CR Par CDS Rate Feed - Business Requirements Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Credit Risk Analytics
approving_committee: MLRC

# Parent Reference
parent_document: MR-L7-003  # Feeds Overview
feed_id: CR-PAR-001
---

# CR Par CDS Rate Feed - Business Requirements Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-PAR-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Credit Risk Analytics |
| **Approver** | MLRC |

---

## 1. Executive Summary

This document specifies the business requirements for the CR Par CDS Rate Feed (Credit Risk Par CDS Conventional Spread) from Murex to the downstream Market Risk and VESPA reporting systems. This feed is **one of 8 Credit Sensitivities feeds** that together provide comprehensive credit spread risk metrics.

Unlike other feeds in the CR suite which provide sensitivities, the CR Par CDS Rate feed provides **market data** - specifically the **conventional par CDS spread** at each tenor pillar for credit positions. This spread corresponds to the upfront amount for CDS contracts.

### 1.1 Credit Sensitivities Feed Suite

| Feed | File Name | Description |
|------|-----------|-------------|
| CR Delta Zero | MxMGB_MR_Credit_CS01_*.csv | CS01 based on zero/default spread curve |
| CR Delta Par | MxMGB_MR_Credit_CS01Par_*.csv | CS01 based on par spread curve |
| CR Basis Rate | MxMGB_MR_Credit_Basis_*.csv | Recovery rate sensitivity WITHOUT propagation |
| **CR Par CDS Rate** | MxMGB_MR_Credit_ParCDS_*.csv | Par CDS conventional spread (this document) |
| CR Instrument Spread | MxMGB_MR_Credit_Spread_*.csv | Zero/instrument spread |
| CR Corr01 | MxMGB_MR_Credit_Corr01_*.csv | Correlation sensitivity (Monte Carlo) |
| CR RR01 | MxMGB_MR_Credit_RR01_*.csv | Recovery rate sensitivity (with propagation) |
| CR RR02 | MxMGB_MR_Credit_RR02_*.csv | Recovery rate sensitivity (without propagation) |

### 1.2 Purpose

The CR Par CDS Rate feed provides the **conventional spread** (par CDS spread) for each credit position at each tenor pillar. This market data is essential for:

- Credit spread monitoring and analysis
- P&L attribution (spread level vs. spread sensitivity)
- Stress testing (applying spread shocks)
- Credit curve construction validation
- Regulatory reporting (credit spread levels)
- Jump-to-Default calculations (using spread as proxy for credit quality)

### 1.3 Par CDS Spread Definition

| Aspect | Description |
|--------|-------------|
| **Metric** | Par CDS Spread / Conventional Spread |
| **Source** | Credit curve market data (TBL_AC_CRDCURVES_REP) |
| **Unit** | Decimal (spread / 100) |
| **Example** | 0.0125 represents 125 basis points |
| **Bonds** | Set to 0 (bonds use z-spread, not CDS spread) |

---

## 2. Business Objectives

### 2.1 Primary Objectives

| # | Objective | Priority |
|---|-----------|----------|
| 1 | Provide par CDS spread levels for all credit positions | Critical |
| 2 | Enable credit spread monitoring by issuer/tenor | Critical |
| 3 | Support P&L attribution (spread level changes) | High |
| 4 | Enable stress scenario application | High |
| 5 | Support credit curve validation | Medium |

### 2.2 Use Cases

| Use Case | Description | User |
|----------|-------------|------|
| **UC-001** | Monitor credit spread levels by issuer | Credit Risk Analytics |
| **UC-002** | Attribute P&L to spread level changes | P&L Attribution |
| **UC-003** | Apply spread shocks in stress scenarios | Risk Engine (Plato) |
| **UC-004** | Validate credit curve calibration | Market Data Control |
| **UC-005** | Calculate implied default probability | Credit Risk |
| **UC-006** | Support regulatory credit spread reporting | Regulatory Reporting |

---

## 3. Data Requirements

### 3.1 Key Metric: PAR_CDS

| Property | Value |
|----------|-------|
| **Field Name** | PAR_CDS |
| **Description** | Conventional CDS spread divided by 100 |
| **Source** | M_CONVENTIO / 100 from TBL_AC_CRDCURVES_REP |
| **Unit** | Decimal (e.g., 0.0125 = 125 bps) |
| **Bonds** | Set to 0 (bonds do not use CDS spreads) |
| **CRDI** | From index curve data |

**Calculation**:
```
PAR_CDS = CASE WHEN GROUP = 'BOND'
               THEN 0
               ELSE M_CONVENTIO / 100
          END
```

### 3.2 Product Coverage

#### 3.2.1 Non-Index Products (Non-CRDI)

| Product Group | Product Types | PAR_CDS Handling |
|---------------|---------------|------------------|
| **CDS** | Single-name CDS | From credit curve |
| **BOND** | Corporate bonds, FRNs | Set to 0 |
| **CLN** | Credit-linked notes | From credit curve |

#### 3.2.2 Credit Index Products (CRDI)

| Index Family | Examples | PAR_CDS Handling |
|--------------|----------|------------------|
| **iTraxx** | iTraxx Europe, iTraxx Crossover | From index curve |
| **CDX** | CDX.NA.IG, CDX.NA.HY | From index curve |

### 3.3 Tenor Pillars

Par CDS spreads are reported at standard credit curve tenor pillars:

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
| Curve Name | Credit spread curve name | Risk factor mapping |
| CIF | Customer Information File ID | Issuer identification |
| GLOBUS ID | External issuer identifier | Cross-system reference |
| Country | Country of risk | Geographic concentration |
| ISIN | Reference obligation ISIN | Security identification |

#### 3.4.3 Market Data

| Field | Description | Purpose |
|-------|-------------|---------|
| PAR_CDS | Par CDS conventional spread / 100 | Spread level |
| Recovery Rate | Expected recovery in default | Reference data |
| Date | Tenor pillar date | Tenor classification |
| Currency | Trade currency | Currency identification |

#### 3.4.4 Trade Details

| Field | Description | Purpose |
|-------|-------------|---------|
| Maturity | Trade maturity date | Tenor classification |
| Underlying | Reference obligation | Credit reference |

**Note**: This feed has **19 fields** - simpler than CR Delta Zero/Par (23 fields) as it does not include NOTIONAL, MARKET, RESTRUCTURING, or USD conversion fields.

---

## 4. Data Quality Requirements

### 4.1 Completeness

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| All CDS positions must have PAR_CDS values | 100% | 0% |
| Bond positions must have PAR_CDS = 0 | 100% | 0% |
| Issuer field populated for non-CRDI trades | 100% | 0% |
| Recovery rate populated for non-CRDI trades | 100% | 0% |
| All hierarchy fields populated | 100% | 0% |

### 4.2 Accuracy

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| PAR_CDS values match credit curve market data | 100% | 0% |
| PAR_CDS values non-negative | 100% | 0% |
| PAR_CDS reasonable range (0-0.50 for most issuers) | 100% | Flag outliers |
| Recovery rates between 0% and 100% | 100% | 0% |

### 4.3 Reconciliation

| Reconciliation | Frequency | Tolerance |
|----------------|-----------|-----------|
| Position count: CR Par CDS vs. CR Delta Zero | Daily | 0% |
| PAR_CDS vs. Market Data Viewer MKTP_CRED_CURVES | Daily | 0.01% |
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
| Credit curve calibration complete | 18:00 | Missing PAR_CDS values |
| TBL_AC_CRDCURVES_REP populated | 18:30 | No curve data |
| Trade extraction complete | 19:00 | Missing positions |
| Valuation batch complete | 21:00 | Delayed processing |

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

| Region | Market Data Set | Curve Source |
|--------|-----------------|--------------|
| LN | LNCLOSE | TBL_AC_CRDCURVES_REP |
| HK | HKCLOSE | TBL_AC_CRDCURVES_REP |
| NY | NYCLOSE | TBL_AC_CRDCURVES_REP |
| SP | SPCLOSE | TBL_AC_CRDCURVES_REP |

---

## 8. Credit Index Handling (CRDI)

### 8.1 Differences from Single-Name Products

| Aspect | Single-Name (Non-CRDI) | Index (CRDI) |
|--------|------------------------|--------------|
| **Issuer** | Specific issuer name | PL Instrument (Index label) |
| **Curve Name** | Issuer credit curve | PL Instrument |
| **Recovery Rate** | Issuer-specific rate | Set to 0 |
| **PAR_CDS Source** | TBL_AC_CRDCURVES_REP via curve name | TBL_AC_CRDCURVES_REP via PL Instrument |
| **CIF/GLOBUS_ID** | Issuer identifiers | Set to 0/blank |
| **Country** | Issuer country | Blank (multi-country) |
| **Source Table** | TBL_VESPA_SENS_REP | TBL_VESPA_SENSCI_REP |

---

## 9. Credit Curve Data Source

### 9.1 TBL_AC_CRDCURVES_REP

| Property | Description |
|----------|-------------|
| **Table Name** | TBL_AC_CRDCURVES_REP |
| **Purpose** | Credit curve market data for non-bonds |
| **Key Field** | M_CONVENTIO (Conventional spread in bps) |
| **Join Key** | M_LABEL = CURVE_NAME, M_TENOR = DATE |
| **Market Data Viewer** | MKTP_CRED_CURVES |

### 9.2 Join Logic

```sql
-- Non-CRDI: Join on curve name and tenor
LEFT JOIN TBL_AC_CRDCURVES_REP CURVE
  ON CURVE.M_LABEL = VSP.M_CURVE_NA1
  AND CURVE.M_TENOR = VSP.M_DATE__ZER

-- CRDI: Join on PL Instrument (index label)
LEFT JOIN TBL_AC_CRDCURVES_REP CURVE
  ON CURVE.M_LABEL = VSP.M_PL_INSTRU
```

---

## 10. Exception Handling

### 10.1 Calculation Failures

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Credit curve missing | Use T-1 curve with flag | Market Data Control |
| Curve/tenor not found | Set PAR_CDS to null, flag | L2 Support |
| Position cannot be valued | Flag as ERROR, exclude | L2 Support |

### 10.2 Data Quality Issues

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Issuer unmapped | Use PL Instrument as fallback | Credit Data Team |
| Recovery rate missing | Use sector default | Credit Risk |
| Hierarchy unmapped | Map to UNMAPPED node | Bookman Team |
| Outlier PAR_CDS value (>5000 bps) | Flag for review, include | RAV Team |

---

## 11. Change Management

### 11.1 Change Triggers

| Trigger | Process |
|---------|---------|
| New credit product type | Update scope, add to extraction |
| New credit index | Add to CRDI extraction |
| Credit curve source change | Update joins, validate data |
| New credit curve provider | Update market data mapping |

### 11.2 Approval Requirements

| Change Type | Approval |
|-------------|----------|
| Scope change | Head of Credit Risk Analytics |
| Curve source change | Market Data Control |
| Feed structure change | Risk Technology + RAV |
| SLA change | Risk Technology + Downstream |

---

## 12. Regulatory Requirements

### 12.1 IMA Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| Credit spread data quality | CRR Art. 367 | Par CDS from market data |
| Issuer-level granularity | CRR Art. 367 | By issuer/curve |
| Consistent with pricing | CRR Art. 367 | Same curves as P&L |
| Daily calculation | CRR Art. 365 | Daily feed |

### 12.2 Use in Risk Calculations

| Calculation | Usage |
|-------------|-------|
| VaR | Spread level for shock application |
| Stress Testing | Base spread for scenario shocks |
| P&L Attribution | Spread level change contribution |
| Default Probability | Implied PD from spread |

---

## 13. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |
| [CR Par CDS Rate IT Config](./cr-par-cds-rate-config.md) | CR-PAR-CFG-001 | IT implementation |
| [CR Par CDS Rate IDD](./cr-par-cds-rate-idd.md) | CR-PAR-IDD-001 | Interface specification |
| [CR Delta Zero BRD](../cr-delta-zero/cr-delta-zero-brd.md) | CR-DZ-BRD-001 | Related CR01 feed |
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
