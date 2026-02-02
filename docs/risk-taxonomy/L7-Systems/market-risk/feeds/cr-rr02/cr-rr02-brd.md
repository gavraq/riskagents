---
# Document Metadata
document_id: CR-RR02-BRD-001
document_name: CR RR02 Feed - Business Requirements Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Credit Risk Analytics
approving_committee: MLRC

# Parent Reference
parent_document: MR-L7-003  # Feeds Overview
feed_id: CR-RR02-001
---

# CR RR02 Feed - Business Requirements Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-RR02-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Credit Risk Analytics |
| **Approver** | MLRC |

---

## 1. Executive Summary

This document specifies the business requirements for the CR RR02 Feed (Credit Recovery Rate 02) from Murex to downstream Market Risk and VESPA reporting systems. This feed is **one of 8 Credit Sensitivities feeds** that together provide comprehensive credit spread risk metrics.

The CR RR02 feed provides **recovery rate sensitivity WITHOUT propagation** - measuring the P&L impact of changes in the recovery rate assumption in isolation, without recalibrating credit spreads.

### 1.1 Credit Sensitivities Feed Suite

| Feed | File Name | Description |
|------|-----------|-------------|
| CR Delta Zero | MxMGB_MR_Credit_CS01_*.csv | CS01 based on zero/default spread curve |
| CR Delta Par | MxMGB_MR_Credit_CS01Par_*.csv | CS01 based on par spread curve |
| CR Basis Rate | MxMGB_MR_Credit_Basis_*.csv | Recovery rate sensitivity WITHOUT propagation |
| CR Par CDS Rate | MxMGB_MR_Credit_ParCDS_*.csv | Par CDS conventional spread |
| CR Instrument Spread | MxMGB_MR_Credit_Spread_*.csv | Zero/instrument spread |
| CR Corr01 | MxMGB_MR_Credit_Corr01_*.csv | Correlation sensitivity (Monte Carlo) |
| CR RR01 | MxMGB_MR_Credit_RR01_*.csv | Recovery rate sensitivity WITH propagation |
| **CR RR02** | MxMGB_MR_Credit_RR02_*.csv | Recovery rate sensitivity WITHOUT propagation (this document) |

### 1.2 Purpose

The CR RR02 feed provides **pure recovery rate sensitivity** for credit positions, isolating the recovery assumption impact from spread effects. This measure is essential for:

- Pure recovery rate risk monitoring
- Understanding isolated recovery assumption impact
- Comparison with RR01 to understand propagation effect
- Model validation and back-testing
- Regulatory reporting (recovery risk decomposition)
- P&L attribution granularity

### 1.3 RR02 vs RR01: Understanding the Difference

| Aspect | RR02 (Without Propagation) | RR01 (With Propagation) |
|--------|---------------------------|-------------------------|
| **Source Field** | M_RECOVERY1 | M_RECOVERY_ |
| **Spread Impact** | No spread recalibration | Spread recalibrates |
| **Use Case** | Pure recovery sensitivity | Full recovery risk |
| **Magnitude** | Typically smaller | Typically larger |
| **Same As** | CR Basis Rate | - |

**Without Propagation**: Recovery rate changes in isolation, with credit spread held constant. This captures the **direct** impact of recovery assumption changes.

**With Propagation**: When recovery rate changes, the credit spread is recalibrated to match market CDS prices, causing a cascading P&L effect.

### 1.4 Recovery Rate Sensitivity Definition

| Property | Value |
|----------|-------|
| **Metric** | RR02 / Recovery Rate 02 |
| **Definition** | P&L sensitivity to 1% change in recovery rate (spread held constant) |
| **Source Field** | M_RECOVERY1 from VW_Vespa_Sensitivities |
| **Unit** | Local currency (trade currency) |
| **Example** | RR02 = 220.87 means 1% recovery increase = +220.87 MZN P&L impact |

### 1.5 Relationship: RR01, RR02, and CR Basis Rate

| Feed | Source Field | Description | Relationship |
|------|--------------|-------------|--------------|
| **CR RR01** | M_RECOVERY_ | With propagation | RR01 ≈ RR02 + Spread Effect |
| **CR RR02** | M_RECOVERY1 | Without propagation | Pure recovery |
| **CR Basis Rate** | M_RECOVERY1 | Without propagation | Same as RR02 |

**Note**: CR Basis Rate and CR RR02 use the same source field (M_RECOVERY1) but may have different naming/formatting in output.

---

## 2. Business Objectives

### 2.1 Primary Objectives

| # | Objective | Priority |
|---|-----------|----------|
| 1 | Capture pure recovery rate risk without spread effects | Critical |
| 2 | Enable recovery assumption sensitivity analysis | Critical |
| 3 | Support model validation (RR01 vs RR02 comparison) | High |
| 4 | Enable P&L attribution decomposition | High |
| 5 | Support regulatory recovery risk reporting | High |

### 2.2 Use Cases

| Use Case | Description | User |
|----------|-------------|------|
| **UC-001** | Isolate pure recovery rate risk | Credit Risk Analytics |
| **UC-002** | Compare RR01 vs RR02 to understand spread propagation | Model Validation |
| **UC-003** | P&L attribution: recovery vs. spread | P&L Attribution |
| **UC-004** | Validate recovery assumption sensitivity | Risk Analytics |
| **UC-005** | Regulatory reporting (recovery decomposition) | Regulatory Reporting |
| **UC-006** | Back-testing recovery risk models | Model Risk |

---

## 3. Data Requirements

### 3.1 Key Metric: RR02_SENSI

| Property | Value |
|----------|-------|
| **Field Name** | RR02_SENSI |
| **Description** | Recovery rate sensitivity WITHOUT spread propagation |
| **Source** | M_RECOVERY1 from TBL_VESPA_SENS_REP / TBL_VESPA_SENSCI_REP |
| **Unit** | Local currency (trade currency) |
| **Change Reference** | CM-6396 (changed from M_VALUE to M_RECOVERY1) |

**Interpretation**:
- **Positive RR02**: Higher recovery = higher P&L (direct effect only)
- **Negative RR02**: Higher recovery = lower P&L (direct effect only)
- **RR02 <= RR01**: Typically, as propagation adds to total sensitivity

### 3.2 Product Coverage

#### 3.2.1 Non-Index Products (Non-CRDI)

| Product Group | Product Types | RR02 Applicability |
|---------------|---------------|-------------------|
| **CDS** | Single-name CDS | Full RR02 calculation |
| **BOND** | Corporate bonds, FRNs | RR02 for credit component |
| **CLN** | Credit-linked notes | RR02 per underlying |

#### 3.2.2 Credit Index Products (CRDI)

| Index Family | Examples | RR02 Handling |
|--------------|----------|---------------|
| **iTraxx** | iTraxx Europe, iTraxx Crossover | Index-level RR02 |
| **CDX** | CDX.NA.IG, CDX.NA.HY | Index-level RR02 |

### 3.3 Tenor Pillars

RR02 is reported at standard credit curve tenor pillars:

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

**Note**: For CRDI, the DATE field is blank (index-level aggregation).

### 3.4 Required Data Elements

#### 3.4.1 Trade Identification

| Field | Description | Purpose |
|-------|-------------|---------|
| TRADE_NUM | Murex trade identifier | Unique identification |
| PORTFOLIO | Trading portfolio | Bookman hierarchy aggregation |
| FAMILY | Trade family (CRD, IRD, EQD) | Product classification |
| GROUP | Trade group (CDS, BOND, CRDI) | Product sub-classification |
| TYPE | Trade type | Detailed classification |
| TYPOLOGY | Trade typology | Risk classification |
| INSTRUMENT | PL Instrument | Instrument identification |

#### 3.4.2 Credit Reference Data

| Field | Description | Purpose |
|-------|-------------|---------|
| ISSUER | Issuer name/label | Credit concentration |
| CURVE_NAME | Credit spread curve name | Risk factor mapping |
| CIF | Customer Information File ID | Issuer identification |
| GLOBUS_ID | External issuer identifier | Cross-system reference |
| COUNTRY | Country of risk | Geographic concentration |

#### 3.4.3 Risk Metrics

| Field | Description | Purpose |
|-------|-------------|---------|
| RR02_SENSI | Recovery rate sensitivity (without propagation) | Core risk metric |
| RECOVERY_RATE | Current recovery rate assumption | Reference data |
| DATE | Tenor pillar date | Tenor classification |
| CURRENCY | Trade/sensitivity currency | Currency identification |

#### 3.4.4 Trade Details

| Field | Description | Purpose |
|-------|-------------|---------|
| MATURITY | Trade maturity date | Tenor classification |
| ISIN | Reference obligation ISIN | Security identification |
| UNDERLYING | Reference obligation label | CDS reference |
| RESTRUCT | Restructuring terms | CDS terms classification |

**Note**: This feed has **20 fields** - identical structure to CR RR01.

---

## 4. Data Quality Requirements

### 4.1 Completeness

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| All credit positions with recovery sensitivity included | 100% | 0% |
| ISSUER field populated for non-CRDI trades | 100% | 0% |
| RECOVERY_RATE populated for non-CRDI trades | 100% | 0% |
| DATE (tenor) populated for non-CRDI trades | 100% | 0% |
| All hierarchy fields populated | 100% | 0% |

### 4.2 Accuracy

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| RR02 values match Murex calculation | 100% | 0.01% |
| RR02 sign consistent with position direction | 100% | Flag exceptions |
| Recovery rates between 0% and 100% | 100% | 0% |
| RR02 <= RR01 (propagation adds sensitivity) | 95% | Flag exceptions |

### 4.3 Reconciliation

| Reconciliation | Frequency | Tolerance |
|----------------|-----------|-----------|
| Position count: CR RR02 vs. CR RR01 | Daily | 0% |
| RR02 vs. CR Basis Rate (same source) | Daily | 0.01% |
| RR02 vs. RR01 relationship | Daily | Flag where RR02 > RR01 |

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
| Credit curve calibration complete | 18:00 | Missing curves |
| Recovery rate data populated | 18:00 | Missing recovery rates |
| TBL_VESPA_SENS_REP populated | 21:00 | No sensitivity data |
| TBL_VESPA_SENSCI_REP populated | 21:00 | No CRDI data |
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

### 7.2 Regional Processing

| Region | Market Data Set | Output File Pattern |
|--------|-----------------|---------------------|
| LN | LNCLOSE | MxMGB_MR_Credit_RR02_LN_YYYYMMDD.csv |
| HK | HKCLOSE | MxMGB_MR_Credit_RR02_HK_YYYYMMDD.csv |
| NY | NYCLOSE | MxMGB_MR_Credit_RR02_NY_YYYYMMDD.csv |
| SP | SPCLOSE | MxMGB_MR_Credit_RR02_SP_YYYYMMDD.csv |

---

## 8. Non-CRDI vs CRDI Handling

### 8.1 Structural Differences

| Aspect | Non-CRDI | CRDI |
|--------|----------|------|
| **Source Table** | TBL_VESPA_SENS_REP | TBL_VESPA_SENSCI_REP |
| **ISSUER** | Issuer name (or PL Instrument if null) | PL Instrument |
| **CURVE_NAME** | Credit curve name (M_CURVE_NA1) | PL Instrument |
| **DATE** | Tenor pillar (M_DATE__ZER) | Blank ('') |
| **RECOVERY_RATE** | Issuer recovery rate (M_RATE) | 0 |
| **CIF** | Issuer CIF | 0 |
| **GLOBUS_ID** | Issuer GLOBUS ID | Blank |
| **COUNTRY** | Issuer country | Blank |
| **ISIN** | Reference obligation ISIN | Blank |
| **UNDERLYING** | Reference obligation label | Blank |
| **RESTRUCT** | Restructuring terms (Yes/NONE) | NONE |

### 8.2 Filter Differences

| Filter | Non-CRDI | CRDI |
|--------|----------|------|
| **Group Filter** | M_GROUP <> 'CRDI' | M_GROUP = 'CRDI' |
| **Issuer Filter** | M_ISSUER IS NOT NULL | N/A |
| **Date Filter** | M_DATE__ZER IS NOT NULL | N/A |

---

## 9. Understanding RR02: Pure Recovery Sensitivity

### 9.1 What is RR02?

**RR02** measures the P&L sensitivity of a credit position to changes in the recovery rate assumption, **holding credit spread constant**.

```
RR02 = dP&L / dRecoveryRate (for 1% change, spread fixed)
```

### 9.2 Why "Without Propagation"?

In reality, recovery rate and credit spread are linked through the credit pricing model:
- CDS pricing depends on both spread and recovery
- Market CDS prices imply a spread-recovery combination
- If recovery changes, spread must adjust to match market prices

**RR02 ignores this linkage** and shows the direct mathematical impact of recovery changes.

### 9.3 Comparing RR01 and RR02

For the same trade at 1Y tenor (from sample data):

| Metric | RR01 | RR02 | Difference |
|--------|------|------|------------|
| Value | 132.13 | 220.87 | 88.74 |
| Interpretation | Full impact | Direct impact | Spread effect |

**Note**: In some cases RR02 > RR01, depending on the spread sensitivity direction.

### 9.4 Use Case: Decomposition

| Component | Calculation | Purpose |
|-----------|-------------|---------|
| **Total Recovery Risk** | RR01 | Full P&L impact |
| **Direct Recovery Risk** | RR02 | Pure assumption impact |
| **Spread Propagation** | RR01 - RR02 | Indirect effect |

---

## 10. Exception Handling

### 10.1 Calculation Failures

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Recovery rate missing | Use sector default | Credit Risk |
| Credit curve missing | Use T-1 curve with flag | Market Data Control |
| RR02 calculation failed | Flag as ERROR, exclude | L2 Support |

### 10.2 Data Quality Issues

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Issuer unmapped | Use PL Instrument as fallback | Credit Data Team |
| Hierarchy unmapped | Map to UNMAPPED node | Bookman Team |
| RR02 > RR01 significantly | Flag for review (unusual direction) | Risk Analytics |
| Outlier RR02 value | Flag for review, include | RAV Team |

---

## 11. Change Management

### 11.1 Change Triggers

| Trigger | Process |
|---------|---------|
| New credit product type | Update scope, add to extraction |
| New credit index | Add to CRDI extraction |
| Recovery model change | Update methodology documentation |
| Source field change | Update extraction SQL (ref: CM-6396) |

### 11.2 Historical Change Reference

| Change ID | Date | Description |
|-----------|------|-------------|
| CM-6396 | Historical | Changed RR02_SENSI source from M_VALUE to M_RECOVERY1 |

### 11.3 Approval Requirements

| Change Type | Approval |
|-------------|----------|
| Scope change | Head of Credit Risk Analytics |
| Source field change | Risk Technology + RAV |
| Feed structure change | Risk Technology + RAV |
| SLA change | Risk Technology + Downstream |

---

## 12. Regulatory Requirements

### 12.1 IMA Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| Recovery rate risk decomposition | CRR Art. 367 | RR02 metric |
| Tenor granularity | CRR Art. 367 | By tenor pillar |
| Issuer-level granularity | CRR Art. 367 | By issuer/curve |
| Daily calculation | CRR Art. 365 | Daily feed |

### 12.2 Use in Risk Calculations

| Calculation | Usage |
|-------------|-------|
| VaR | Pure recovery risk factor |
| Model Validation | RR01 vs RR02 comparison |
| P&L Attribution | Recovery decomposition |
| Back-testing | Isolated recovery sensitivity |

---

## 13. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |
| [CR RR02 IT Config](./cr-rr02-config.md) | CR-RR02-CFG-001 | IT implementation |
| [CR RR02 IDD](./cr-rr02-idd.md) | CR-RR02-IDD-001 | Interface specification |
| [CR RR01 BRD](../cr-rr01/cr-rr01-brd.md) | CR-RR01-BRD-001 | RR with propagation |
| [CR Basis Rate BRD](../cr-basis-rate/cr-basis-rate-brd.md) | CR-BR-BRD-001 | Same source field |
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
