---
# Document Metadata
document_id: CR-RR01-BRD-001
document_name: CR RR01 Feed - Business Requirements Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Credit Risk Analytics
approving_committee: MLRC

# Parent Reference
parent_document: MR-L7-003  # Feeds Overview
feed_id: CR-RR01-001
---

# CR RR01 Feed - Business Requirements Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-RR01-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Credit Risk Analytics |
| **Approver** | MLRC |

---

## 1. Executive Summary

This document specifies the business requirements for the CR RR01 Feed (Credit Recovery Rate 01) from Murex to downstream Market Risk and VESPA reporting systems. This feed is **one of 8 Credit Sensitivities feeds** that together provide comprehensive credit spread risk metrics.

The CR RR01 feed provides **recovery rate sensitivity WITH propagation** - measuring the P&L impact of changes in the recovery rate assumption, where the change propagates through to affect credit spread calculations.

### 1.1 Credit Sensitivities Feed Suite

| Feed | File Name | Description |
|------|-----------|-------------|
| CR Delta Zero | MxMGB_MR_Credit_CS01_*.csv | CS01 based on zero/default spread curve |
| CR Delta Par | MxMGB_MR_Credit_CS01Par_*.csv | CS01 based on par spread curve |
| CR Basis Rate | MxMGB_MR_Credit_Basis_*.csv | Recovery rate sensitivity WITHOUT propagation |
| CR Par CDS Rate | MxMGB_MR_Credit_ParCDS_*.csv | Par CDS conventional spread |
| CR Instrument Spread | MxMGB_MR_Credit_Spread_*.csv | Zero/instrument spread |
| CR Corr01 | MxMGB_MR_Credit_Corr01_*.csv | Correlation sensitivity (Monte Carlo) |
| **CR RR01** | MxMGB_MR_Credit_RR01_*.csv | Recovery rate sensitivity WITH propagation (this document) |
| CR RR02 | MxMGB_MR_Credit_RR02_*.csv | Recovery rate sensitivity WITHOUT propagation |

### 1.2 Purpose

The CR RR01 feed provides **recovery rate sensitivity with propagation** for credit positions. This measure is essential for:

- Recovery rate risk monitoring and limits
- P&L attribution (recovery rate contribution)
- Stress testing (recovery rate shocks)
- VaR calculation (recovery as risk factor)
- Jump-to-Default calculations
- Regulatory capital (recovery rate assumptions)

### 1.3 RR01 vs RR02: Understanding Propagation

| Aspect | RR01 (With Propagation) | RR02 (Without Propagation) |
|--------|-------------------------|---------------------------|
| **Source Field** | M_RECOVERY_ | M_RECOVERY1 |
| **Spread Impact** | Recovery change affects spread calibration | Recovery change isolated |
| **Use Case** | Full recovery risk | Pure recovery sensitivity |
| **Magnitude** | Typically larger | Typically smaller |
| **CR Basis Rate** | N/A | Uses same M_RECOVERY1 |

**With Propagation**: When recovery rate changes, the credit spread is recalibrated to match market prices, causing a cascading P&L effect.

**Without Propagation**: Recovery rate changes in isolation, with credit spread held constant.

### 1.4 Recovery Rate Sensitivity Definition

| Property | Value |
|----------|-------|
| **Metric** | RR01 / Recovery Rate 01 |
| **Definition** | P&L sensitivity to 1% change in recovery rate (with spread recalibration) |
| **Source Field** | M_RECOVERY_ from VW_Vespa_Sensitivities |
| **Unit** | Local currency (trade currency) |
| **Example** | RR01 = 132.13 means 1% recovery increase = +132.13 MZN P&L impact |

---

## 2. Business Objectives

### 2.1 Primary Objectives

| # | Objective | Priority |
|---|-----------|----------|
| 1 | Capture full recovery rate risk including spread propagation | Critical |
| 2 | Enable recovery rate limit monitoring | Critical |
| 3 | Support P&L attribution for recovery changes | High |
| 4 | Enable recovery rate stress scenarios | High |
| 5 | Support Jump-to-Default calculations | High |

### 2.2 Use Cases

| Use Case | Description | User |
|----------|-------------|------|
| **UC-001** | Monitor recovery rate exposure by issuer/tenor | Credit Risk Analytics |
| **UC-002** | Attribute P&L to recovery rate changes | P&L Attribution |
| **UC-003** | Apply recovery shocks in stress scenarios | Risk Engine (Plato) |
| **UC-004** | Calculate Jump-to-Default exposure | Credit Risk |
| **UC-005** | Assess recovery assumption sensitivity | Model Validation |
| **UC-006** | Regulatory reporting (recovery assumptions) | Regulatory Reporting |

---

## 3. Data Requirements

### 3.1 Key Metric: RR01_SENSI

| Property | Value |
|----------|-------|
| **Field Name** | RR01_SENSI |
| **Description** | Recovery rate sensitivity with spread propagation |
| **Source** | M_RECOVERY_ from TBL_VESPA_SENS_REP / TBL_VESPA_SENSCI_REP |
| **Unit** | Local currency (trade currency) |
| **CRDI Handling** | Same source field from CRDI table |

**Interpretation**:
- **Positive RR01**: Higher recovery = higher P&L (protection seller benefits)
- **Negative RR01**: Higher recovery = lower P&L (protection buyer loses)
- **Magnitude**: Larger than RR02 due to spread recalibration effect

### 3.2 Product Coverage

#### 3.2.1 Non-Index Products (Non-CRDI)

| Product Group | Product Types | RR01 Applicability |
|---------------|---------------|-------------------|
| **CDS** | Single-name CDS | Full RR01 calculation |
| **BOND** | Corporate bonds, FRNs | RR01 for credit component |
| **CLN** | Credit-linked notes | RR01 per underlying |

#### 3.2.2 Credit Index Products (CRDI)

| Index Family | Examples | RR01 Handling |
|--------------|----------|---------------|
| **iTraxx** | iTraxx Europe, iTraxx Crossover | Index-level RR01 |
| **CDX** | CDX.NA.IG, CDX.NA.HY | Index-level RR01 |

### 3.3 Tenor Pillars

RR01 is reported at standard credit curve tenor pillars:

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
| RR01_SENSI | Recovery rate sensitivity (with propagation) | Core risk metric |
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

**Note**: This feed has **20 fields** - similar structure to CR Basis Rate.

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
| RR01 values match Murex calculation | 100% | 0.01% |
| RR01 sign consistent with position direction | 100% | Flag exceptions |
| Recovery rates between 0% and 100% | 100% | 0% |
| RR01 >= RR02 (propagation adds to sensitivity) | 95% | Flag exceptions |

### 4.3 Reconciliation

| Reconciliation | Frequency | Tolerance |
|----------------|-----------|-----------|
| Position count: CR RR01 vs. CR Delta Zero | Daily | 0% |
| RR01 vs. Murex P&L Attribution | Daily | 0.01% |
| RR01 vs. RR02 relationship | Daily | Flag where RR01 < RR02 |

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
| LN | LNCLOSE | MxMGB_MR_Credit_RR01_LN_YYYYMMDD.csv |
| HK | HKCLOSE | MxMGB_MR_Credit_RR01_HK_YYYYMMDD.csv |
| NY | NYCLOSE | MxMGB_MR_Credit_RR01_NY_YYYYMMDD.csv |
| SP | SPCLOSE | MxMGB_MR_Credit_RR01_SP_YYYYMMDD.csv |

---

## 8. Non-CRDI vs CRDI Handling

### 8.1 Structural Differences

| Aspect | Non-CRDI | CRDI |
|--------|----------|------|
| **Source Table** | TBL_VESPA_SENS_REP | TBL_VESPA_SENSCI_REP |
| **ISSUER** | Issuer name (or PL Instrument if null) | PL Instrument |
| **CURVE_NAME** | Credit curve name (M_CURVE_NA1) | PL Instrument |
| **DATE** | Tenor pillar (M_DATE__ZER) | Blank ('' ) |
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

## 9. Understanding Recovery Rate Risk

### 9.1 What is RR01?

**RR01** measures the P&L sensitivity of a credit position to changes in the recovery rate assumption, including the effect of spread recalibration.

```
RR01 = dP&L / dRecoveryRate (for 1% change, with spread propagation)
```

### 9.2 Propagation Effect

When recovery rate changes with propagation:
1. Recovery rate assumption changes by 1%
2. Credit spread is recalibrated to match market CDS prices
3. Position is revalued with new spread and recovery
4. Net P&L change = RR01

This captures the **total economic impact** of recovery assumption changes.

### 9.3 Position Direction and RR01 Sign

| Position | Recovery Up Impact | RR01 Sign |
|----------|-------------------|-----------|
| **CDS Protection Buyer** | Loss (LGD decreases) | Negative |
| **CDS Protection Seller** | Gain (payout decreases) | Positive |
| **Long Bond** | Gain (expected loss decreases) | Positive |
| **Short Bond** | Loss | Negative |

### 9.4 Relationship to Jump-to-Default

RR01 is closely related to Jump-to-Default (JTD) exposure:

```
JTD ≈ Notional × (1 - RecoveryRate) × Direction
dJTD/dRecovery = -Notional × Direction
```

RR01 captures this sensitivity plus spread propagation effects.

---

## 10. Exception Handling

### 10.1 Calculation Failures

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Recovery rate missing | Use sector default | Credit Risk |
| Credit curve missing | Use T-1 curve with flag | Market Data Control |
| RR01 calculation failed | Flag as ERROR, exclude | L2 Support |

### 10.2 Data Quality Issues

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Issuer unmapped | Use PL Instrument as fallback | Credit Data Team |
| Hierarchy unmapped | Map to UNMAPPED node | Bookman Team |
| RR01 < RR02 | Flag for review (unusual) | Risk Analytics |
| Outlier RR01 value | Flag for review, include | RAV Team |

---

## 11. Change Management

### 11.1 Change Triggers

| Trigger | Process |
|---------|---------|
| New credit product type | Update scope, add to extraction |
| New credit index | Add to CRDI extraction |
| Recovery model change | Update methodology documentation |
| New recovery data source | Update mappings |

### 11.2 Approval Requirements

| Change Type | Approval |
|-------------|----------|
| Scope change | Head of Credit Risk Analytics |
| Model change | Model Risk + MLRC |
| Feed structure change | Risk Technology + RAV |
| SLA change | Risk Technology + Downstream |

---

## 12. Regulatory Requirements

### 12.1 IMA Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| Recovery rate risk capture | CRR Art. 367 | RR01 metric |
| Tenor granularity | CRR Art. 367 | By tenor pillar |
| Issuer-level granularity | CRR Art. 367 | By issuer/curve |
| Daily calculation | CRR Art. 365 | Daily feed |

### 12.2 Use in Risk Calculations

| Calculation | Usage |
|-------------|-------|
| VaR | Recovery as risk factor |
| Stressed VaR | Recovery stress scenarios |
| IRC | Recovery for default/migration |
| Jump-to-Default | Base recovery for JTD |
| Stress Testing | Recovery rate shocks |

---

## 13. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |
| [CR RR01 IT Config](./cr-rr01-config.md) | CR-RR01-CFG-001 | IT implementation |
| [CR RR01 IDD](./cr-rr01-idd.md) | CR-RR01-IDD-001 | Interface specification |
| [CR RR02 BRD](../cr-rr02/cr-rr02-brd.md) | CR-RR02-BRD-001 | RR without propagation |
| [CR Basis Rate BRD](../cr-basis-rate/cr-basis-rate-brd.md) | CR-BR-BRD-001 | Related recovery feed |
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
