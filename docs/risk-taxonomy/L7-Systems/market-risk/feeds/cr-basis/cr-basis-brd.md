---
# Document Metadata
document_id: CR-BAS-BRD-001
document_name: CR Basis Rate Feed - Business Requirements Document
version: 1.0
effective_date: 2025-01-02
next_review_date: 2026-01-02
owner: Head of Credit Risk Analytics
approving_committee: MLRC

# Parent Reference
parent_document: MR-L7-003  # Feeds Overview
feed_id: CR-BAS-001
---

# CR Basis Rate Feed - Business Requirements Document

**Meridian Global Bank**

| Document Control | |
|-----------------|---|
| **Document ID** | CR-BAS-BRD-001 |
| **Version** | 1.0 |
| **Effective Date** | 2 January 2025 |
| **Owner** | Head of Credit Risk Analytics |
| **Approver** | MLRC |

---

## 1. Executive Summary

This document specifies the business requirements for the CR Basis Rate Feed (Credit Risk Basis Sensitivity) from Murex to the downstream Market Risk and VESPA reporting systems. This feed is **one of 8 Credit Sensitivities feeds** that together provide comprehensive credit spread risk metrics.

The CR Basis Rate feed provides position-level sensitivity to the **recovery rate WITHOUT recovery rate propagation** (using M_RECOVERY1 - Recovery Rate 2 in Murex Simulation view) for:

- **Single-name credit instruments**: CDS, Bonds with credit risk, Credit-linked notes
- **Credit Index instruments**: iTraxx, CDX, and other credit indices (CRDI)

### 1.1 Credit Sensitivities Feed Suite

| Feed | File Name | Description |
|------|-----------|-------------|
| CR Delta Zero | MxMGB_MR_Credit_CS01_*.csv | CS01 based on zero/default spread curve |
| CR Delta Par | MxMGB_MR_Credit_CS01Par_*.csv | CS01 based on par spread curve |
| **CR Basis Rate** | MxMGB_MR_Credit_Basis_Rate_*.csv | Recovery rate sensitivity WITHOUT propagation (this document) |
| CR Par CDS Rate | MxMGB_MR_Credit_ParCDS_*.csv | Par CDS spread rate |
| CR Instrument Spread | MxMGB_MR_Credit_Spread_*.csv | Zero/instrument spread |
| CR Corr01 | MxMGB_MR_Credit_Corr01_*.csv | Correlation sensitivity (Monte Carlo) |
| CR RR01 | MxMGB_MR_Credit_RR01_*.csv | Recovery rate sensitivity (with propagation) |
| CR RR02 | MxMGB_MR_Credit_RR02_*.csv | Recovery rate sensitivity (without propagation) |

### 1.2 Purpose

The CR Basis Rate sensitivity measures the P&L impact of changes to the recovery rate **without propagating** the change through the credit spread curve. This "no-propagation" methodology is essential for:

- Understanding pure recovery rate exposure
- Isolating recovery rate risk from credit spread risk
- Stress testing recovery assumptions independently
- Credit risk limit monitoring
- Regulatory capital calculation (recovery rate scenarios)

### 1.3 Recovery Rate Sensitivity Types

| Sensitivity | Propagation | Source Field | Description |
|-------------|-------------|--------------|-------------|
| **BASIS** (this feed) | No | M_RECOVERY1 | Recovery rate 2 - changes recovery rate only |
| RR01 | Yes | M_RECOVERY | Recovery rate 1 - propagates to credit spreads |
| RR02 | No | M_RECOVERY1 | Alternative no-propagation calculation |

---

## 2. Business Objectives

### 2.1 Primary Objectives

| # | Objective | Priority |
|---|-----------|----------|
| 1 | Provide accurate position-level recovery rate sensitivities | Critical |
| 2 | Enable isolation of recovery rate risk from spread risk | Critical |
| 3 | Support regulatory stress testing (recovery rate scenarios) | Critical |
| 4 | Enable recovery rate limit monitoring | High |
| 5 | Support Jump-to-Default (JTD) scenario analysis | High |

### 2.2 Use Cases

| Use Case | Description | User |
|----------|-------------|------|
| **UC-001** | Stress test portfolio under recovery rate shock | Risk Engine (Plato) |
| **UC-002** | Aggregate recovery rate exposure by issuer | Credit Risk Analytics |
| **UC-003** | Monitor issuer-level recovery assumptions | Risk Management |
| **UC-004** | Calculate recovery-adjusted JTD exposure | Capital Calculation |
| **UC-005** | Attribute P&L to recovery rate changes | P&L Attribution |

---

## 3. Data Requirements

### 3.1 Sensitivity Type

#### 3.1.1 BASIS (Recovery Rate Sensitivity - No Propagation)

| Metric | Description | Unit |
|--------|-------------|------|
| **BASIS (Local Currency)** | P&L impact of recovery rate change (no propagation) | Trade currency |
| **BASIS (USD)** | BASIS converted to USD at COB FX rate | USD |

**Calculation Method**:
- Bump the issuer's recovery rate (M_RECOVERY1 / Recovery Rate 2)
- **Do NOT propagate** the change to credit spread curves
- Recalculate the position's mark-to-market value
- BASIS = New MTM - Original MTM

**Key Distinction**: Unlike RR01 which uses M_RECOVERY (Recovery Rate 1) and propagates to credit spreads, BASIS uses M_RECOVERY1 (Recovery Rate 2) and isolates the pure recovery rate impact.

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

BASIS sensitivities are reported at standard credit curve tenor pillars:

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
| BASIS (Local) | Recovery sensitivity in trade currency | Local currency risk |
| BASIS (USD) | Recovery sensitivity in USD | Aggregation currency |
| Currency | Trade/sensitivity currency | FX conversion |
| Maturity | Trade maturity date | Tenor classification |

**Note**: Unlike CR Delta Zero, this feed does **not** include CR01 fields, NOTIONAL, or MARKET fields.

---

## 4. Data Quality Requirements

### 4.1 Completeness

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| All credit positions must have BASIS sensitivities | 100% | 0% |
| Issuer field populated for non-CRDI trades | 100% | 0% |
| All hierarchy fields populated | 100% | 0% |
| BASIS (USD) calculated for all positions | 100% | 0% |

### 4.2 Accuracy

| Requirement | Target | Tolerance |
|-------------|--------|-----------|
| BASIS sign consistent with trade direction | 100% | 0% |
| BASIS values within valid range | 100% | 0% |
| FX conversion to USD correct | 100% | 0.01% |

### 4.3 Reconciliation

| Reconciliation | Frequency | Tolerance |
|----------------|-----------|-----------|
| Position count: CR Basis feed vs. Trade feed | Daily | 0% |
| Total BASIS (USD): Feed vs. Risk matrices | Daily | 0.1% |
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
| Credit curve calibration complete | 18:00 | Cannot calculate BASIS |
| Recovery rate updates | 17:00 | Stale recovery rates |
| Trade extraction complete | 19:00 | Missing positions |
| Valuation batch complete | 21:00 | Delayed sensitivities |

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
| **CIF/GLOBUS_ID** | Issuer identifiers | Set to 0/blank |
| **Country** | Issuer country | Blank (multi-country) |
| **ISIN** | Reference obligation ISIN | Blank |
| **Source Table** | TBL_VESPA_SENS_REP | TBL_VESPA_SENSCI_REP |

### 8.2 Index-Level Recovery Rates

For credit indices, recovery rate sensitivities are calculated at the index level rather than decomposed to constituent names. Index decomposition for regulatory purposes is handled by a separate process.

---

## 9. Exception Handling

### 9.1 Calculation Failures

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Credit curve missing | Use T-1 curve with flag | Market Data Control |
| Position cannot be valued | Flag as ERROR, exclude | L2 Support |
| BASIS calculation fails | Use T-1 sensitivity | L2 Support |
| FX rate missing | Use T-1 rate with flag | Market Data Control |

### 9.2 Data Quality Issues

| Exception | Handling | Escalation |
|-----------|----------|------------|
| Issuer unmapped | Flag for review | Credit Data Team |
| Recovery rate missing | Use sector default | Credit Risk |
| Hierarchy unmapped | Map to UNMAPPED node | Bookman Team |
| Outlier BASIS value | Flag for review, include | RAV Team |

---

## 10. Change Management

### 10.1 Change Triggers

| Trigger | Process |
|---------|---------|
| New credit product type | Update scope, add to extraction |
| New credit index | Add to CRDI extraction |
| Regulatory change | Update requirements, MLRC approval |
| Recovery rate methodology change | Update calculation, Model Validation |

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
| Capture recovery rate risk | CRR Art. 367 | BASIS sensitivities included |
| Issuer-level granularity | CRR Art. 367 | By issuer aggregation |
| Consistent with pricing | CRR Art. 367 | Same models as P&L |
| Daily calculation | CRR Art. 365 | Daily feed |

### 11.2 Stress Testing Requirements

| Requirement | Reference | Compliance |
|-------------|-----------|------------|
| Recovery rate stress scenarios | ICAAP/PRA SS3/21 | BASIS enables scenario analysis |
| Jump-to-Default calculation | CRR Art. 372 | Recovery sensitivity supports JTD |
| Correlation stress | CRR Art. 367 | Combined with CR Corr01 |

---

## 12. Related Documents

| Document | ID | Relationship |
|----------|-----|--------------|
| [Feeds Overview](../feeds-overview.md) | MR-L7-003 | Parent document |
| [Data Dictionary](../../data-dictionary.md) | MR-L7-002 | Field definitions |
| [CR Basis IT Config](./cr-basis-config.md) | CR-BAS-CFG-001 | IT implementation |
| [CR Basis IDD](./cr-basis-idd.md) | CR-BAS-IDD-001 | Interface specification |
| [CR Delta Zero BRD](../cr-delta-zero/cr-delta-zero-brd.md) | CR-DZ-BRD-001 | Related CR01 feed |
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
