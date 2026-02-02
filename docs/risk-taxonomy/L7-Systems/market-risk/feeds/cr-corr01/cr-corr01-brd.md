---
# Document Metadata
document_id: CR-CORR-BRD-001
document_name: CR Corr01 Feed - Business Requirements Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Credit Risk Analytics
approving_committee: MLRC

# Parent Reference
parent_document: MR-L7-003  # Feeds Overview
feed_id: CR-CORR-001
---

# CR Corr01 Feed - Business Requirements Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-CORR-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Credit Risk Analytics |
| **Approver** | MLRC |

---

## 1. Executive Summary

This document specifies the business requirements for the CR Corr01 Feed (Credit Correlation 01) from Murex to downstream Market Risk and VESPA reporting systems. This feed is **one of 8 Credit Sensitivities feeds** that together provide comprehensive credit spread risk metrics.

The CR Corr01 feed provides **correlation sensitivity** - the P&L impact of changes in the average correlation parameter used in Monte Carlo pricing of correlation-dependent credit products (CDOs, CLNs, basket CDS, first-to-default swaps, etc.).

### 1.1 Credit Sensitivities Feed Suite

| Feed | File Name | Description |
|------|-----------|-------------|
| CR Delta Zero | MxMGB_MR_Credit_CS01_*.csv | CS01 based on zero/default spread curve |
| CR Delta Par | MxMGB_MR_Credit_CS01Par_*.csv | CS01 based on par spread curve |
| CR Basis Rate | MxMGB_MR_Credit_Basis_*.csv | Recovery rate sensitivity WITHOUT propagation |
| CR Par CDS Rate | MxMGB_MR_Credit_ParCDS_*.csv | Par CDS conventional spread |
| CR Instrument Spread | MxMGB_MR_Credit_Spread_*.csv | Zero/instrument spread |
| **CR Corr01** | MxMGB_MR_Credit_Corr01_*.csv | Correlation sensitivity (this document) |
| CR RR01 | MxMGB_MR_Credit_RR01_*.csv | Recovery rate sensitivity (with propagation) |
| CR RR02 | MxMGB_MR_Credit_RR02_*.csv | Recovery rate sensitivity (without propagation) |

### 1.2 Purpose

The CR Corr01 feed provides **correlation sensitivity** for credit products priced using Monte Carlo simulation. This measure is essential for:

- Correlation risk monitoring and limits
- P&L attribution (correlation contribution)
- Stress testing (correlation shocks)
- VaR calculation (correlation as risk factor)
- Structured credit product risk management
- Regulatory capital (correlation-based charges)

### 1.3 Correlation Sensitivity Definition

| Aspect | Description |
|--------|-------------|
| **Metric** | Corr01 / Correlation 01 |
| **Definition** | P&L sensitivity to 1bp change in average correlation |
| **Source Field** | M_CORR01 from VW_Vespa_Sensitivities |
| **Unit** | Local currency (trade currency) |
| **Products** | Monte Carlo priced products only |
| **Example** | Corr01 = -2014 means 1bp correlation increase = -2,014 USD P&L impact |

### 1.4 Key Differentiators from Other CR Feeds

| Aspect | CR Corr01 | Other CR Feeds |
|--------|-----------|----------------|
| **Scope** | Non-CRDI only | Non-CRDI + CRDI |
| **Metric Type** | Correlation sensitivity | Spread/recovery sensitivity |
| **Pricing Method** | Monte Carlo only | All methods |
| **Credit References** | Two curves/issuers | Single curve/issuer |
| **Output Fields** | 13 fields | 19-23 fields |
| **Products** | Correlation products | All credit products |

---

## 2. Business Objectives

### 2.1 Primary Objectives

| # | Objective | Priority |
|---|-----------|----------|
| 1 | Capture correlation risk for structured credit products | Critical |
| 2 | Enable correlation limit monitoring | Critical |
| 3 | Support P&L attribution for correlation changes | High |
| 4 | Enable correlation stress scenarios | High |
| 5 | Support regulatory capital for correlation risk | High |

### 2.2 Use Cases

| Use Case | Description | User |
|----------|-------------|------|
| **UC-001** | Monitor correlation exposure by product/portfolio | Credit Risk Analytics |
| **UC-002** | Attribute P&L to correlation changes | P&L Attribution |
| **UC-003** | Apply correlation shocks in stress scenarios | Risk Engine (Plato) |
| **UC-004** | Calculate correlation VaR contribution | Market Risk |
| **UC-005** | Support correlation limit framework | Credit Limits |
| **UC-006** | Regulatory reporting (correlation charges) | Regulatory Reporting |

---

## 3. Data Requirements

### 3.1 Key Metric: CREDIT_CORR01

| Property | Value |
|----------|-------|
| **Field Name** | CREDIT_CORR01 |
| **Description** | Sensitivity to average correlation parameter |
| **Source** | M_CORR01 from TBL_VESPA_SENS_REP |
| **Unit** | Local currency (trade currency) |
| **Applicability** | Monte Carlo priced products only |
| **Filter** | Only positions where M_CORR01 <> 0 |

**Interpretation**:
- **Positive Corr01**: Long correlation - benefits from correlation increase
- **Negative Corr01**: Short correlation - suffers from correlation increase
- **Zero Corr01**: No correlation sensitivity (non-MC priced or uncorrelated)

### 3.2 Product Coverage

#### 3.2.1 In-Scope Products (Monte Carlo Priced)

| Product Group | Product Types | Correlation Exposure |
|---------------|---------------|----------------------|
| **CDO/CLO** | Synthetic CDOs, CLOs, CDO-squared | Tranche attachment/detachment |
| **CLN** | Credit-linked notes | Multi-name embedded |
| **Basket CDS** | First-to-default, nth-to-default | Default correlation |
| **Index Tranches** | iTraxx/CDX tranches | Correlation between names |

#### 3.2.2 Out-of-Scope Products

| Product Group | Reason |
|---------------|--------|
| **Single-name CDS** | No correlation (single reference) |
| **Bonds** | No correlation |
| **Index (plain)** | No MC pricing (correlation implicit) |
| **IR/FX Products** | No credit correlation |

### 3.3 Dual Credit Reference Structure

Unlike other CR feeds with single issuer/curve, Corr01 captures **two credit references** for correlation products:

| Field | Description | Purpose |
|-------|-------------|---------|
| **CREDIT_CURVE1** | First underlying credit curve | Primary reference entity |
| **CREDIT_CURVE2** | Second underlying credit curve | Secondary reference entity |
| **CREDIT_ISSUER1** | First issuer name | Issuer identification |
| **CREDIT_ISSUER2** | Second issuer name | Issuer identification |

**Note**: For products with more than 2 references (e.g., 125-name CDX), only the first two (alphabetically) are captured. Full decomposition is available via constituent-level feeds.

### 3.4 Required Data Elements

#### 3.4.1 Trade Identification

| Field | Description | Purpose |
|-------|-------------|---------|
| TRADE_NUM | Murex trade identifier | Unique identification |
| PORTFOLIO | Trading portfolio | Hierarchy aggregation |
| INSTRUMENT | PL Instrument | Instrument identification |
| TRN_FAMILY | Trade family (CRD, IRD) | Product classification |
| TRN_GROUP | Trade group (BOND, CDS) | Product sub-classification |
| TRN_TYPE | Trade type | Detailed classification |

#### 3.4.2 Security Reference

| Field | Description | Purpose |
|-------|-------------|---------|
| SECURITY_CODE | ISIN of reference obligation | Security identification |
| CURRENCY | Trade/sensitivity currency | Currency identification |

#### 3.4.3 Credit Reference Data

| Field | Description | Purpose |
|-------|-------------|---------|
| CREDIT_CURVE1 | First credit curve name | Risk factor mapping |
| CREDIT_CURVE2 | Second credit curve name | Risk factor mapping |
| CREDIT_ISSUER1 | First issuer label | Concentration analysis |
| CREDIT_ISSUER2 | Second issuer label | Concentration analysis |

#### 3.4.4 Risk Metric

| Field | Description | Purpose |
|-------|-------------|---------|
| CREDIT_CORR01 | Correlation sensitivity | Core risk metric |

**Note**: This feed has only **13 fields** - the simplest in the CR suite, as it focuses solely on correlation sensitivity without tenor breakdown or USD conversion.

---

## 4. Data Quality Requirements

### 4.1 Completeness

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| All MC-priced positions with Corr01 included | 100% | 0% |
| CREDIT_CURVE1 populated | 100% | 0% |
| CREDIT_ISSUER1 populated | 100% | 0% |
| Trade identification fields populated | 100% | 0% |

### 4.2 Accuracy

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| Corr01 values match Murex calculation | 100% | 0.01% |
| Corr01 sign consistent with position direction | 100% | Flag exceptions |
| Credit curve names valid | 100% | 0% |
| Issuer names match market data | 100% | 0% |

### 4.3 Reconciliation

| Reconciliation | Frequency | Tolerance |
|----------------|-----------|-----------|
| Corr01 vs. Murex MC valuation report | Daily | 0.01% |
| Position count vs. MC-priced universe | Daily | Review variance |
| Credit curves vs. TBL_AC_CRDCURVES_REP | Daily | 0% |

---

## 5. Timeliness Requirements

### 5.1 Service Level Agreements

| Metric | Target | Escalation |
|--------|--------|------------|
| **Feed Delivery Time** | 05:30 GMT (T+1) | >06:00 escalate to L2 |
| **As-Of Date** | T (previous business day) | N/A |
| **Position Coverage** | 100% of MC-priced credit | <99% escalate to L2 |

### 5.2 Dependencies

| Upstream Dependency | SLA | Impact |
|---------------------|-----|--------|
| Monte Carlo valuation batch complete | 20:00 | No Corr01 values |
| Credit curve calibration complete | 18:00 | Missing curve/issuer data |
| TBL_VESPA_SENS_REP populated | 21:00 | No sensitivity data |
| TBL_AC_CRDCURVES_REP populated | 18:30 | Missing issuer mappings |

**Note**: Monte Carlo valuation is typically longer-running than analytical pricing, so this feed depends on later upstream completion.

---

## 6. Scope Definition

### 6.1 In-Scope Positions

| Criteria | Value |
|----------|-------|
| **STP Status** | RELE (Released), VERI (Verified), STTL (Settled) |
| **Legal Entity** | MGB (Meridian Global Bank) |
| **Pricing Method** | Monte Carlo simulation |
| **M_CORR01** | Non-zero (has correlation sensitivity) |
| **Product Type** | Correlation-dependent credit products |

### 6.2 Out-of-Scope

| Exclusion | Reason |
|-----------|--------|
| Non-MC priced products | No Corr01 calculation |
| M_CORR01 = 0 | No correlation sensitivity |
| CRDI (plain credit indices) | Correlation implicit |
| Single-name CDS | No correlation |
| Banking book positions | Separate IRRBB/CSRBB process |

### 6.3 No CRDI Component

Unlike other CR feeds which include CRDI (credit index) positions via UNION with TBL_VESPA_SENSCI_REP, the CR Corr01 feed:

- Extracts **only from TBL_VESPA_SENS_REP** (non-CRDI)
- Credit index tranches with correlation sensitivity are captured as individual trades
- Plain credit indices do not have explicit correlation sensitivity (it's embedded in pricing)

---

## 7. Regional Coverage

### 7.1 Trading Regions

| Region | Code | Status | Primary Products |
|--------|------|--------|------------------|
| **London** | LN | Active | CDOs, CLNs, Basket CDS |
| **Hong Kong** | HK | Active | Asia structured credit |
| **New York** | NY | Active | US structured credit |
| **Singapore** | SP | Limited | Regional products |

### 7.2 Regional Processing

| Region | Market Data Set | Output File Pattern |
|--------|-----------------|---------------------|
| LN | LNCLOSE | MxMGB_MR_Credit_Corr01_LN_YYYYMMDD.csv |
| HK | HKCLOSE | MxMGB_MR_Credit_Corr01_HK_YYYYMMDD.csv |
| NY | NYCLOSE | MxMGB_MR_Credit_Corr01_NY_YYYYMMDD.csv |
| SP | SPCLOSE | MxMGB_MR_Credit_Corr01_SP_YYYYMMDD.csv |

---

## 8. Understanding Correlation Sensitivity

### 8.1 What is Corr01?

**Corr01** measures the P&L sensitivity of a credit product to changes in the correlation parameter used in Monte Carlo simulation.

```
Corr01 = dP&L / dCorrelation (for 1bp change)
```

### 8.2 Correlation in Credit Products

| Product | Correlation Impact |
|---------|-------------------|
| **Equity Tranche (0-3%)** | Long correlation - benefits from higher correlation |
| **Mezzanine Tranche (3-7%)** | Typically short correlation |
| **Senior Tranche (7-12%)** | Short correlation - benefits from lower correlation |
| **Super Senior (12%+)** | Strongly short correlation |
| **Basket CDS (FTD)** | Short correlation |

### 8.3 Why Two Credit Curves/Issuers?

Correlation products involve multiple reference entities. The feed captures the first two (alphabetically ordered by curve name) to provide:

- Primary concentration visibility
- Key reference entity identification
- Basis risk between names

For full constituent-level breakdown, use dedicated CDO/CLN composition feeds.

---

## 9. Exception Handling

### 9.1 Calculation Failures

| Exception | Handling | Escalation |
|-----------|----------|------------|
| MC valuation failed | Exclude position, flag as ERROR | L2 Support |
| Corr01 not calculated | Use T-1 value with flag | Risk Analytics |
| Credit curve unmapped | Flag for review | Market Data Control |

### 9.2 Data Quality Issues

| Exception | Handling | Escalation |
|-----------|----------|------------|
| CREDIT_CURVE1 null | Use INSTRUMENT as fallback | Credit Data Team |
| Issuer not found in curves table | Blank issuer, flag | Market Data Control |
| Outlier Corr01 (>1M) | Flag for review, include | RAV Team |
| CREDIT_CURVE2 null | Acceptable for single-underlying | N/A |

---

## 10. Change Management

### 10.1 Change Triggers

| Trigger | Process |
|---------|---------|
| New correlation product type | Update scope, validate MC pricing |
| Correlation model change | Update methodology documentation |
| New Monte Carlo engine version | Validate Corr01 calculation |
| Credit curve source change | Update curve mapping |

### 10.2 Approval Requirements

| Change Type | Approval |
|-------------|----------|
| Scope change | Head of Credit Risk Analytics |
| Model change | Model Risk + MLRC |
| Feed structure change | Risk Technology + RAV |
| SLA change | Risk Technology + Downstream |

---

## 11. Regulatory Requirements

### 11.1 IMA Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| Correlation risk capture | CRR Art. 367 | Corr01 metric |
| Daily calculation | CRR Art. 365 | Daily feed |
| Independent validation | CRR Art. 368 | Reconciliation controls |
| Stress testing | CRR Art. 370 | Correlation shocks |

### 11.2 Use in Risk Calculations

| Calculation | Usage |
|-------------|-------|
| VaR | Correlation as risk factor |
| Stressed VaR | Historical correlation scenarios |
| IRC | Correlation for migration |
| CRM | Comprehensive Risk Measure |
| Stress Testing | Correlation stress scenarios |

---

## 12. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |
| [CR Corr01 IT Config](./cr-corr01-config.md) | CR-CORR-CFG-001 | IT implementation |
| [CR Corr01 IDD](./cr-corr01-idd.md) | CR-CORR-IDD-001 | Interface specification |
| [CR Delta Zero BRD](../cr-delta-zero/cr-delta-zero-brd.md) | CR-DZ-BRD-001 | Related CR feed |
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
